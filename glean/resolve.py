"""Resolve *who* a researcher is from any one of four inputs.

Why this module exists
----------------------
Adding someone to ``watchlist.md`` used to require a hand-typed display name:
you had to already know the exact string before the tool could do anything —
even when you were holding their homepage URL or Semantic Scholar id. Identity
resolution is a different job from *work* collection (:mod:`glean.watch`) and it
has a different source ranking, so it lives here:

* :mod:`glean.watch` asks "what has this person published lately?" and ranks
  **homepage -> DBLP -> Semantic Scholar**.
* This module asks "which person is this?" and needs whichever source can answer
  first, accepting a name, a homepage, a DBLP id or an S2 id as the entry point.

What each source can actually answer (measured 2026-09-26)
---------------------------------------------------------
============================  =========  ==================================
input                         fetches?   fills
============================  =========  ==================================
personal homepage (HTML)      yes        name, plus any DBLP / S2 link the
                                         page itself exposes
Semantic Scholar id or name   yes        name, affiliations, DBLP author name
                                         (rate limited: plain 429s)
DBLP pid / URL / name         **no**     the value is recorded as a link and
                                         used as a name hint, never fetched
============================  =========  ==================================

DBLP sits behind an Anubis proof-of-work bot check that answers *every*
request with an HTML challenge — verified with a browser User-Agent, with the
project User-Agent, and on both the proxied and the direct route. So this module
deliberately never fetches DBLP and says so out loud instead of letting a failed
fetch look like "no such person". The same applies to the ``dblp`` fallback in
:mod:`glean.watch`: it has been silently returning ``[]`` for the same reason.

The result is a *proposal*, never a silent write: every field carries where it
came from, ambiguous name searches come back as ``alternates`` for the user to
choose between, and ``needs_review`` marks the cases where the name was inferred
rather than given.
"""

from __future__ import annotations

import json
import re
import urllib.parse
from typing import Any

from glean.config import WATCH_TIMEOUT
from glean.core import http_get_text

# --- endpoints -------------------------------------------------------------

S2_GRAPH = "https://api.semanticscholar.org/graph/v1"
S2_AUTHOR_FIELDS = "name,affiliations,homepage,paperCount,externalIds"
DBLP_AUTHOR_SEARCH = "https://dblp.org/search/author/api"

# Shown to the user whenever a DBLP value had to be taken on trust.
DBLP_UNFETCHABLE = (
    "DBLP 已启用反爬人机校验（Anubis），本机无法自动抓取："
    "该值只作为链接/姓名线索记录，不会用于解析。"
)

S2_RATE_LIMITED = "Semantic Scholar 返回 429（公共接口限流），本次未能补全姓名/机构。"

# --- homepage scraping -----------------------------------------------------
#
# Deliberately regex-based: we need three fields from one page, and pulling in an
# HTML parser dependency for that would break the project's stdlib-only rule for
# everything outside the Web extra (see glean/homeparse.py for the same call).

_TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
_H1_RE = re.compile(r"<h1[^>]*>(.*?)</h1>", re.S | re.I)
_HREF_RE = re.compile(r"""href\s*=\s*["']([^"']+)["']""", re.I)
_META_RE = re.compile(
    r"""<meta\s+[^>]*?(?:name|property)\s*=\s*["']([^"']+)["'][^>]*?"""
    r"""content\s*=\s*["']([^"']*)["']""",
    re.S | re.I,
)
_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"\s+")
_CJK_RE = re.compile(r"[\u3400-\u9fff]")

# Title decorations that are site furniture, not the person's name.
_TITLE_SUFFIXES = (
    "personal homepage", "personal home page", "home page", "homepage",
    "home", "个人主页", "主页", "的个人主页",
)
_NAMEY_META = ("author", "og:title", "citation_author", "dc.creator")


def _clean(text: str) -> str:
    """Strip tags, unescape entities, collapse whitespace."""
    import html as _html

    return _WS_RE.sub(" ", _html.unescape(_TAG_RE.sub(" ", text or ""))).strip()


def looks_like_person_name(text: str) -> bool:
    """Heuristic gate: could this string be one person's name?

    Biased towards rejecting. A homepage title like "Publications" or
    "SIGMOD 2026" must not become somebody's watchlist heading, while
    "Alexey Gotsman" and "魏恒峰" must.
    """
    core = _clean(re.sub(r"\([^()]*\)|\[[^\[\]]*\]", "", text or "")).strip(" ,.-—–|·")
    if not (2 <= len(core) <= 48):
        return False
    if any(ch.isdigit() for ch in core):
        return False
    if re.search(r"[|/·—–_@]", core):
        return False
    if _CJK_RE.fullmatch(core[0]) is not None and re.fullmatch(r"[\u3400-\u9fff]{2,4}", core):
        return True
    words = core.split()
    if not 1 <= len(words) <= 4:
        return False
    if len(words) == 1:
        # A lone Latin token ("Home", "Publications") is too ambiguous to accept.
        return bool(re.fullmatch(r"[\u3400-\u9fff]{2,4}", core))
    return all(_CJK_RE.search(w) or w[:1].isupper() for w in words)


def name_from_title(title: str) -> str | None:
    """Turn a homepage ``<title>`` into a display name, or ``None``.

    Handles the two shapes real homepages use::

        Hengfeng Wei (魏恒峰)          -> unchanged
        Alexey Gotsman's Home Page    -> Alexey Gotsman
        Alice Lin | University of X   -> Alice Lin
    """
    text = _clean(title)
    if not text:
        return None
    for sep in ("|", "·", "—", "–", " :: "):
        if sep in text:
            left = text.split(sep, 1)[0].strip()
            if looks_like_person_name(left):
                text = left
                break
    text = re.sub(r"['’]s\b.*$", "", text).strip()
    low = text.lower()
    for suffix in _TITLE_SUFFIXES:
        if low.endswith(suffix):
            text = text[: len(text) - len(suffix)].strip(" ,.-—–|·:")
            low = text.lower()
    return text if looks_like_person_name(text) else None


def links_from_homepage(raw_html: str, base_url: str) -> dict[str, str]:
    """Pick the DBLP pid / S2 author id a homepage links out to, if any.

    A link is *not* fetched either — it is the person's own declaration of
    identity, which is exactly the kind of corroboration a proposal needs.
    """
    found: dict[str, str] = {}
    for href in _HREF_RE.findall(raw_html or ""):
        url = urllib.parse.urljoin(base_url, href)
        if "dblp" not in found:
            m = re.search(r"dblp\.org/pid/([0-9a-z/]+?)(?:\.html)?$", url, re.I)
            if m:
                found["dblp"] = f"pid/{m.group(1).strip('/')}"
        if "s2" not in found:
            m = _S2_ID_IN_URL_RE.search(url)
            if m:
                found["s2"] = m.group(1)
    return found


def name_from_homepage(raw_html: str) -> tuple[str | None, str]:
    """Best name on a homepage plus which element it came from."""
    for label, pattern in (("h1", _H1_RE), ("title", _TITLE_RE)):
        for m in pattern.finditer(raw_html or ""):
            name = name_from_title(m.group(1))
            if name:
                return name, label
    metas = {k.lower(): v for k, v in _META_RE.findall(raw_html or "")}
    for key in _NAMEY_META:
        if key in metas:
            name = name_from_title(metas[key])
            if name:
                return name, f"meta[{key}]"
    return None, ""


# --- input normalisation ---------------------------------------------------

_DBLP_PID_RE = re.compile(r"(?:^|/)(pid/[0-9a-z][0-9a-z/]*?)(?:\.html|\.xml)?$", re.I)
# An S2 author URL is ``/author/<Name-Slug>/<numericId>``; the id is the trailing
# numeric segment, *not* the slug — grabbing the first alphanumeric run yields
# "Hengfeng" (the name) instead of the id, which then 404s against the API.
_S2_ID_IN_URL_RE = re.compile(r"semanticscholar\.org/author/(?:[^/?#\s]+/)?(\d+)", re.I)


def normalize_dblp(value: str) -> str | None:
    """Return a ``pid/...`` if the input is one, else ``None`` (it is a name)."""
    text = (value or "").strip()
    if not text:
        return None
    m = _DBLP_PID_RE.search(text if text.startswith("pid/") else "/" + text)
    if m:
        return m.group(1).strip("/")
    if re.fullmatch(r"[0-9]{2}/[0-9]{4}(?:-[0-9]+)?", text):
        return f"pid/{text}"
    return None


def normalize_s2(value: str) -> tuple[str | None, str | None]:
    """Split an S2 input into ``(author_id, query)`` — exactly one is set."""
    text = (value or "").strip()
    if not text:
        return None, None
    m = _S2_ID_IN_URL_RE.search(text)
    if m:
        return m.group(1), None
    if re.fullmatch(r"\d{4,}", text):
        return text, None
    return None, text


# --- Semantic Scholar -----------------------------------------------------

def _s2_get(path: str, timeout: int) -> dict[str, Any]:
    raw = http_get_text(f"{S2_GRAPH}{path}", timeout=timeout)
    data = json.loads(raw)
    return data if isinstance(data, dict) else {}


def s2_author(author_id: str, timeout: int = WATCH_TIMEOUT) -> dict[str, Any] | None:
    """Fetch one S2 author by id. Returns ``None`` on any failure."""
    try:
        data = _s2_get(
            f"/author/{urllib.parse.quote(author_id)}?fields={S2_AUTHOR_FIELDS}",
            timeout,
        )
    except Exception:  # noqa: BLE001 - fallback source, never fatal
        return None
    return data or None


def s2_search(query: str, limit: int = 5, timeout: int = WATCH_TIMEOUT) -> tuple[list[dict], str | None]:
    """Search S2 authors by name. Returns ``(candidates, warning)``.

    A 429 is reported as a warning rather than an empty list: "the limiter said
    no" and "nobody by that name" must not look the same to the caller.
    """
    url = (
        f"{S2_GRAPH}/author/search?query={urllib.parse.quote(query)}"
        f"&fields={S2_AUTHOR_FIELDS}&limit={limit}"
    )
    try:
        data = json.loads(http_get_text(url, timeout=timeout))
    except Exception as exc:  # noqa: BLE001
        code = getattr(exc, "code", None)
        if code == 429 or "429" in str(exc):
            return [], S2_RATE_LIMITED
        return [], f"Semantic Scholar 检索失败（{type(exc).__name__}），未做补全。"
    out: list[dict] = []
    for row in (data.get("data") or []) if isinstance(data, dict) else []:
        ext = (row.get("externalIds") or {})
        dblp = ext.get("DBLP")
        if isinstance(dblp, list):
            dblp = dblp[0] if dblp else None
        out.append(
            {
                "name": (row.get("name") or "").strip(),
                "s2": str(row.get("authorId") or ""),
                "affiliations": [a for a in (row.get("affiliations") or []) if a],
                "paper_count": int(row.get("paperCount") or 0),
                "homepage": row.get("homepage") or None,
                "dblp_name": dblp,
            }
        )
    return out, None


# --- the resolver ---------------------------------------------------------

def dblp_search_url(name: str) -> str:
    """A human-clickable DBLP author search link (we cannot fetch it ourselves)."""
    return f"{DBLP_AUTHOR_SEARCH}?q={urllib.parse.quote(name)}"


def resolve(
    name: str = "",
    homepage: str = "",
    dblp: str = "",
    s2: str = "",
    *,
    timeout: int = WATCH_TIMEOUT,
) -> dict[str, Any]:
    """Propose a full watchlist identity from any subset of the four inputs.

    Never raises for network reasons — every source degrades into a ``warnings``
    entry, because the caller is a form handler that must still be able to say
    *why* nothing was filled in.
    """
    given = {
        "name": (name or "").strip(),
        "homepage": (homepage or "").strip(),
        "dblp": (dblp or "").strip(),
        "s2": (s2 or "").strip(),
    }
    resolved: dict[str, Any] = {
        "name": given["name"],
        "homepage": given["homepage"] or None,
        "dblp": None,
        "s2": None,
    }
    evidence: list[dict[str, str]] = []
    warnings: list[str] = []
    alternates: list[dict] = []
    name_hint = given["name"]
    name_source = "输入" if given["name"] else ""

    def note(field: str, value: str, source: str, extra: str = "") -> None:
        evidence.append({"field": field, "value": value, "source": source, "note": extra})

    # 1) DBLP: normalise, never fetch -------------------------------------
    if given["dblp"]:
        pid = normalize_dblp(given["dblp"])
        if pid:
            resolved["dblp"] = pid
            note("dblp", pid, "输入", "规整为 DBLP pid")
        else:
            resolved["dblp"] = given["dblp"]
            note("dblp", given["dblp"], "输入", "非 pid，按姓名线索使用")
            if not name_hint:
                name_hint, name_source = given["dblp"], "DBLP 输入"
        warnings.append(DBLP_UNFETCHABLE)

    # 2) S2 id: the most reliable machine source --------------------------
    s2_id, s2_query = normalize_s2(given["s2"])
    if s2_id:
        author = s2_author(s2_id, timeout=timeout)
        if author:
            resolved["s2"] = str(author.get("authorId") or s2_id)
            note("s2", resolved["s2"], "Semantic Scholar",
                 f"{author.get('paperCount', 0)} 篇论文")
            if author.get("name"):
                resolved["name"] = author["name"].strip()
                name_source = "Semantic Scholar"
                note("name", resolved["name"], "Semantic Scholar", "按 author id 取回")
            if author.get("homepage") and not resolved["homepage"]:
                resolved["homepage"] = author["homepage"]
                note("homepage", author["homepage"], "Semantic Scholar", "S2 记录的 homepage")
            ext_dblp = (author.get("externalIds") or {}).get("DBLP")
            if isinstance(ext_dblp, list):
                ext_dblp = ext_dblp[0] if ext_dblp else None
            if ext_dblp and not resolved["dblp"]:
                resolved["dblp"] = ext_dblp
                note("dblp", ext_dblp, "Semantic Scholar", "DBLP 作者名（非 pid）")
        else:
            resolved["s2"] = s2_id
            note("s2", s2_id, "输入", "未取到详情")
            warnings.append("Semantic Scholar 未返回该 author id 的详情（限流或 id 有误）。")
    elif s2_query and not name_hint:
        name_hint, name_source = s2_query, "Semantic Scholar 输入"

    # 3) homepage: name + the ids the page itself links to ----------------
    if resolved["homepage"]:
        try:
            raw = http_get_text(resolved["homepage"], timeout=timeout)
        except Exception as exc:  # noqa: BLE001
            warnings.append(
                f"个人主页抓取失败（{type(exc).__name__}）：未能从页面提取姓名；"
                "网络/代理不通时属正常，可稍后重试或直接手填姓名。"
            )
        else:
            found_name, where = name_from_homepage(raw)
            if found_name:
                resolved["name"] = found_name
                name_source = f"主页 {where}"
                note("name", found_name, "个人主页", f"取自 <{where}>")
            else:
                warnings.append("主页可访问，但标题/h1 里没有识别出人名，请自行核对姓名。")
            links = links_from_homepage(raw, resolved["homepage"])
            if links.get("dblp") and not resolved["dblp"]:
                resolved["dblp"] = links["dblp"]
                note("dblp", links["dblp"], "个人主页", "页面上的 DBLP 链接")
            if links.get("s2") and not resolved["s2"]:
                resolved["s2"] = links["s2"]
                note("s2", links["s2"], "个人主页", "页面上的 S2 链接")

    # 4) name: last resort is a lookup by whatever we know ----------------
    if not resolved["name"] and name_hint:
        resolved["name"] = name_hint
        note("name", name_hint, name_source or "推断")

    need_search = (not resolved["s2"] and bool(name_hint)) or not resolved["name"]
    ambiguous = False
    if need_search and name_hint:
        candidates, warning = s2_search(name_hint, timeout=timeout)
        if warning:
            warnings.append(warning)
        # Most prolific first: for a name search the person you want to monitor
        # is usually — not always — the one with a publication record. The list is
        # only a proposal, and the caller shows every entry for a human to pick.
        alternates = sorted(candidates, key=lambda c: -c["paper_count"])
        # Auto-fill only when the search is unambiguous. With two same-named
        # candidates, silently taking the first is how monitoring ends up
        # pointing at the wrong person's publication list.
        if len(candidates) == 1:
            one = candidates[0]
            if not resolved["name"] and one["name"]:
                resolved["name"] = one["name"]
                note("name", one["name"], "Semantic Scholar", "姓名检索唯一命中")
            if not resolved["s2"] and one["s2"]:
                resolved["s2"] = one["s2"]
                note("s2", one["s2"], "Semantic Scholar", "姓名检索唯一命中")
        elif len(candidates) > 1:
            ambiguous = True
            warnings.append(
                f"姓名检索到 {len(candidates)} 位同名候选，未自动选用："
                "请在下方候选中点选目标学者（或直接手填 Semantic Scholar id）。"
            )

    if not resolved["name"]:
        warnings.append(
            "未能推断出姓名：请直接手填姓名，或换一个可抓取的个人主页 / Semantic Scholar id。"
        )
    else:
        resolved["name"] = resolved["name"].strip()

    if name_hint:
        note("DBLP 检索链接", dblp_search_url(name_hint), "生成",
             "DBLP 人工核对入口（本机不可抓取）")

    # "Review me" means: something here was inferred rather than given, or the
    # search was ambiguous, or we ended up with no name at all. Adding without
    # looking is exactly the mistake this flag exists to prevent.
    inferred = (
        not given["name"]
        or resolved["name"] != given["name"]
        or (resolved["s2"] and not given["s2"])
        or (resolved["dblp"] and not given["dblp"])
        or (resolved["homepage"] and not given["homepage"])
    )
    return {
        "query": given,
        "resolved": resolved,
        "evidence": evidence,
        "alternates": alternates,
        "warnings": warnings,
        "needs_review": bool(inferred or ambiguous or not resolved["name"]),
    }
