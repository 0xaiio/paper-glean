"""Monitor researchers for new work and emit push events.

Source order (user-decided): **homepage -> DBLP -> Semantic Scholar**.

* The homepage is authoritative for *ordering* and for non-paper output:
  videos, technical reports and talks exist nowhere else.
* ``dblp`` / ``s2`` are consulted as fallback when the homepage yields nothing,
  and are **merged in when explicitly configured** (deduped by normalised
  title, homepage version wins) — if you bothered to record an id, you want it
  used.
* Semantic Scholar alone can also enrich an item with abstract/venue.

State model
-----------
``watchlist.md`` (Markdown) is the source of truth for *who* is watched.
``data/watch_state.json`` holds only the fingerprints already seen, which is
what makes "new" well defined. A researcher's **first** run seeds the baseline
silently instead of pushing their entire back catalogue (override with
``--force``); every later run pushes only genuinely unseen items.
"""

from __future__ import annotations

import hashlib
import json
import re
import time
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from typing import Any, Iterable

from glean.config import (
    WATCH_DIGEST_MD,
    WATCH_EVENTS,
    WATCH_ITEM_KINDS,
    WATCH_LOOKBACK_YEARS,
    WATCH_MAX_ITEMS,
    WATCH_STATE,
    WATCH_TIMEOUT,
    WATCHLIST_MD,
)
from glean.core import http_get
from glean.homeparse import parse_homepage

KIND_ICONS = {
    "paper": "\U0001f4c4",  # 📄
    "video": "\U0001f3a5",  # 🎥
    "report": "\U0001f4d5",  # 📕
    "talk": "\U0001f3a4",  # 🎤
    "other": "\U0001f517",  # 🔗
}

DBLP_SEARCH = "https://dblp.org/search/publ/api"
DBLP_PID = "https://dblp.org/pid/{pid}.xml"
S2_AUTHOR_PAPERS = "https://api.semanticscholar.org/graph/v1/author/{aid}/papers"

WATCH_DIGEST_HEADER = """# 学者监控 · 新作推送

> 自动生成，勿手工编辑正文（名单请改 [`watchlist.md`](watchlist.md)）。
> 每次 `arxiv_daily.py watch run` 只追加**新发现**的条目；已推送过的不会再出现。
> 用法与故障排查见 [docs/user-guide/watching.md](docs/user-guide/watching.md)。

"""


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

def slugify(name: str) -> str:
    """Stable key for a researcher: lower-cased, ascii-ish, dash separated."""
    s = name.strip().lower()
    s = re.sub(r"[^0-9a-z\u4e00-\u9fff]+", "-", s)
    return s.strip("-") or "researcher"


def _norm_title(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (title or "").lower())[:100]


def fingerprint(item: dict[str, Any]) -> str:
    """Stable identity for an item, used for diffing across runs.

    Title carries the identity; URL disambiguates same-title/different-host
    cases (preprint vs published version) only when it is a real link.
    """
    basis = _norm_title(item.get("title", ""))
    url = (item.get("url") or "").split("?")[0].rstrip("/").lower()
    if url and not url.startswith(("http://www.", "https://www.")):
        basis = basis + "|" + hashlib.sha1(url.encode("utf-8")).hexdigest()[:8]
    return hashlib.sha1(basis.encode("utf-8")).hexdigest()[:16]


def _kind_of(value: str | None) -> str:
    v = (value or "").strip().lower()
    return v if v in WATCH_ITEM_KINDS else "other"


def _year_of(value: Any) -> int | None:
    try:
        y = int(str(value).strip()[:4])
    except (TypeError, ValueError):
        return None
    return y if 1900 <= y <= 2100 else None


# ------------------------------------------------------------------
# watchlist.md — parse / render / mutate
# ------------------------------------------------------------------

def _parse_watchlist(text: str) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    section = "active"
    cur: dict[str, Any] | None = None
    note: list[str] = []

    def flush() -> None:
        if cur is not None:
            cur["note"] = " ".join(note).strip()
            entries.append(cur)

    for raw in text.splitlines():
        s = raw.strip()
        if s.startswith("## "):
            flush()
            cur, note = None, []
            section = "paused" if "已暂停" in s or "暂停" in s else "active"
        elif s.startswith("### ") and s[4:].strip():
            flush()
            note = []
            cur = {
                "name": s[4:].strip(),
                "key": slugify(s[4:]),
                "homepage": None,
                "dblp": None,
                "s2": None,
                "tags": [],
                "enabled": section == "active",
                "note": "",
            }
        elif cur is not None and s.startswith("- "):
            low = s[2:].lower()
            for field in ("homepage", "dblp", "s2", "tags"):
                if low.startswith(field + ":"):
                    value = s.split(":", 1)[1].strip()
                    if field == "tags":
                        cur["tags"] = [t.strip() for t in value.split(";") if t.strip()]
                    else:
                        cur[field] = value or None
                    break
            else:
                if low.startswith("enabled:"):
                    cur["enabled"] = "true" in low
                elif not low.startswith("enabled") and s[2:].strip():
                    note.append(s[2:].strip())
        elif cur is not None and s and not s.startswith("<!--") and not s.startswith("#"):
            note.append(s)
    flush()
    return entries


def load_watchlist() -> list[dict[str, Any]]:
    """Parse watchlist.md; returns [] when the file is absent."""
    if not WATCHLIST_MD.exists():
        return []
    return _parse_watchlist(WATCHLIST_MD.read_text(encoding="utf-8"))


def _entry_block(entry: dict[str, Any], heading: str = "###") -> str:
    lines = [f"{heading} {entry['name']}"]
    if entry.get("homepage"):
        lines.append(f"- homepage: {entry['homepage']}")
    if entry.get("dblp"):
        lines.append(f"- dblp: {entry['dblp']}")
    if entry.get("s2"):
        lines.append(f"- s2: {entry['s2']}")
    if entry.get("tags"):
        lines.append("- tags: " + "; ".join(entry["tags"]))
    lines.append(f"- enabled: {'true' if entry.get('enabled', True) else 'false'}")
    if entry.get("note"):
        lines.append(f"- {entry['note']}")
    return "\n".join(lines)


def _split_sections(text: str) -> tuple[str, str]:
    """Return (preamble, body) — preamble is everything before the first '## '."""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.strip().startswith("## "):
            return "\n".join(lines[:i]).rstrip() + "\n", ""
    return "", text


def _write_watchlist(entries: Iterable[dict[str, Any]], preamble: str) -> None:
    active = [e for e in entries if e.get("enabled", True)]
    paused = [e for e in entries if not e.get("enabled", True)]
    parts = [preamble.rstrip(), "", "## 监控中", ""]
    if active:
        parts.append("\n\n".join(_entry_block(e) for e in active))
        parts.append("")
    else:
        parts.append("<!-- 还没有监控对象；用 `arxiv_daily.py watch add <姓名> --homepage <URL>` 添加。 -->")
        parts.append("")
    parts += ["## 已暂停", ""]
    if paused:
        parts.append("\n\n".join(_entry_block(e) for e in paused))
        parts.append("")
    else:
        parts.append("<!-- 暂停的条目会被移到这里；`enabled: false` 的条目不会被 `watch run` 扫描。 -->")
        parts.append("")
    WATCHLIST_MD.write_text("\n".join(parts), encoding="utf-8")


def _save_entries(entries: list[dict[str, Any]]) -> None:
    preamble = ""
    if WATCHLIST_MD.exists():
        preamble, _ = _split_sections(WATCHLIST_MD.read_text(encoding="utf-8"))
    _write_watchlist(entries, preamble)


def add_researcher(
    name: str,
    homepage: str | None = None,
    dblp: str | None = None,
    s2: str | None = None,
    tags: list[str] | None = None,
    enabled: bool = True,
) -> dict[str, Any]:
    """Append a researcher to watchlist.md. Raises if the name already exists."""
    entries = load_watchlist()
    key = slugify(name)
    if any(e["key"] == key for e in entries):
        raise ValueError(f"已存在同名监控对象: {name}")
    entry = {
        "name": name.strip(),
        "key": key,
        "homepage": homepage or None,
        "dblp": dblp or None,
        "s2": s2 or None,
        "tags": tags or [],
        "enabled": enabled,
        "note": "",
    }
    entries.append(entry)
    _save_entries(entries)
    return entry


def remove_researcher(name: str) -> bool:
    """Remove a researcher (and forget their seen-state). Returns True if removed."""
    entries = load_watchlist()
    key = slugify(name)
    kept = [e for e in entries if e["key"] != key]
    if len(kept) == len(entries):
        return False
    _save_entries(kept)
    state = load_state()
    if key in state.get("researchers", {}):
        state["researchers"].pop(key)
        save_state(state)
    return True


def set_enabled(name: str, enabled: bool) -> bool:
    """Pause/resume a researcher. Returns True if found."""
    entries = load_watchlist()
    key = slugify(name)
    hit = False
    for e in entries:
        if e["key"] == key:
            e["enabled"] = enabled
            hit = True
    if hit:
        _save_entries(entries)
    return hit


# ------------------------------------------------------------------
# Remote sources
# ------------------------------------------------------------------

def fetch_dblp(value: str, timeout: int = WATCH_TIMEOUT) -> list[dict[str, Any]]:
    """Fetch publications from DBLP by author name or by ``pid/...``.

    Returns [] on any failure — DBLP is a fallback source, never fatal.
    """
    items: list[dict[str, Any]] = []
    try:
        if value.startswith("pid/"):
            url = DBLP_PID.format(pid=value)
            root = ET.fromstring(http_get(url, timeout=timeout))
            for node in root.iter():
                title = year = ee = None
                authors: list[str] = []
                for child in node:
                    tag = child.tag.rsplit("}", 1)[-1]
                    if tag == "title" and child.text:
                        title = child.text.strip()
                    elif tag == "year" and child.text:
                        year = child.text.strip()
                    elif tag == "ee" and child.text:
                        ee = child.text.strip()
                    elif tag == "author" and child.text:
                        authors.append(child.text.strip())
                if title and year:
                    items.append(
                        {
                            "title": title.rstrip("."),
                            "url": ee or "",
                            "kind": "paper",
                            "year": _year_of(year),
                            "venue": "",
                            "authors": authors,
                            "abstract": "",
                            "source": "dblp",
                            "confidence": 0.95,
                        }
                    )
        else:
            query = urllib.parse.quote(f"{value}:")
            url = f"{DBLP_SEARCH}?author={query}&format=json&h=100"
            data = json.loads(http_get(url, timeout=timeout).decode("utf-8"))
            for hit in data.get("result", {}).get("hits", {}).get("hit", []):
                info = hit.get("info", {})
                authors = info.get("authors", {}).get("author", [])
                if isinstance(authors, dict):
                    authors = [authors]
                items.append(
                    {
                        "title": (info.get("title") or "").rstrip("."),
                        "url": info.get("ee") or info.get("url") or "",
                        "kind": "paper",
                        "year": _year_of(info.get("year")),
                        "venue": info.get("venue") or "",
                        "authors": [a.get("text", "") for a in authors if isinstance(a, dict)],
                        "abstract": "",
                        "source": "dblp",
                        "confidence": 0.9,
                    }
                )
    except Exception:
        return items
    return items


def fetch_s2(author_id: str, timeout: int = WATCH_TIMEOUT) -> list[dict[str, Any]]:
    """Fetch an author's papers from Semantic Scholar. Returns [] on failure.

    The public endpoint is rate limited (429); callers must tolerate an empty
    result rather than treating it as "no publications".
    """
    fields = "title,year,venue,abstract,externalIds,url,authors"
    url = (
        f"{S2_AUTHOR_PAPERS.format(aid=urllib.parse.quote(author_id))}"
        f"?fields={fields}&limit=100"
    )
    try:
        data = json.loads(http_get(url, timeout=timeout).decode("utf-8"))
    except Exception:
        return []
    items: list[dict[str, Any]] = []
    for p in data.get("data", []) or []:
        ext = p.get("externalIds") or {}
        url_out = p.get("url") or ""
        if ext.get("ArXiv"):
            url_out = f"https://arxiv.org/abs/{ext['ArXiv']}"
        elif ext.get("DOI"):
            url_out = f"https://doi.org/{ext['DOI']}"
        items.append(
            {
                "title": (p.get("title") or "").strip(),
                "url": url_out,
                "kind": "paper",
                "year": _year_of(p.get("year")),
                "venue": p.get("venue") or "",
                "authors": [a.get("name", "") for a in (p.get("authors") or [])],
                "abstract": (p.get("abstract") or "")[:600],
                "source": "s2",
                "confidence": 0.9,
            }
        )
    return items


def collect_items(entry: dict[str, Any], *, use_network: bool = True) -> list[dict[str, Any]]:
    """Gather an researcher's works: homepage first, DBLP/S2 as fallback + merge.

    Homepage items come first so they set the ordering and win title conflicts.
    Configured ``dblp``/``s2`` ids are merged in (deduped by normalised title).
    """
    if not use_network:
        return []

    items: list[dict[str, Any]] = []
    if entry.get("homepage"):
        items.extend(parse_homepage(entry["homepage"]))

    fallback: list[dict[str, Any]] = []
    if entry.get("dblp"):
        fallback.extend(fetch_dblp(entry["dblp"]))
    if entry.get("s2"):
        fallback.extend(fetch_s2(entry["s2"]))

    if not items:  # homepage unusable -> fallbacks become authoritative
        items = fallback
    elif fallback:  # homepage fine -> merge, homepage wins on conflicts
        seen = {_norm_title(i["title"]) for i in items}
        for f in fallback:
            key = _norm_title(f["title"])
            if key and key not in seen:
                seen.add(key)
                items.append(f)

    for it in items:
        it["kind"] = _kind_of(it.get("kind"))
    return [i for i in items if i.get("title")]


# ------------------------------------------------------------------
# State + events
# ------------------------------------------------------------------

def load_state() -> dict[str, Any]:
    if not WATCH_STATE.exists():
        return {"version": 1, "researchers": {}}
    try:
        return json.loads(WATCH_STATE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"version": 1, "researchers": {}}


def save_state(state: dict[str, Any]) -> None:
    WATCH_STATE.parent.mkdir(parents=True, exist_ok=True)
    WATCH_STATE.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def append_events(items: list[dict[str, Any]], pushed_to: list[str], run_id: str) -> None:
    """Append one JSON line per new item to watch_events.jsonl."""
    if not items:
        return
    WATCH_EVENTS.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat()
    with open(WATCH_EVENTS, "a", encoding="utf-8") as fh:
        for it in items:
            fh.write(
                json.dumps(
                    {
                        "time": now,
                        "run_id": run_id,
                        "key": it.get("key"),
                        "researcher": it.get("researcher"),
                        "item": {k: v for k, v in it.items() if k not in ("key", "researcher")},
                        "pushed_to": pushed_to,
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )


def load_events(limit: int = 200) -> list[dict[str, Any]]:
    """Most recent watch events, newest first."""
    if not WATCH_EVENTS.exists():
        return []
    lines = WATCH_EVENTS.read_text(encoding="utf-8").splitlines()
    out: list[dict[str, Any]] = []
    for line in reversed(lines[-limit:]):
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


# ------------------------------------------------------------------
# Digest
# ------------------------------------------------------------------

def _item_line(item: dict[str, Any]) -> str:
    icon = KIND_ICONS.get(item.get("kind", "other"), KIND_ICONS["other"])
    bits = [f"{icon} **{item['title']}**"]
    meta = []
    if item.get("year"):
        meta.append(str(item["year"]))
    if item.get("venue"):
        meta.append(item["venue"])
    if meta:
        bits.append(" — " + " · ".join(meta))
    if item.get("url"):
        bits.append(f" — [链接]({item['url']})")
    bits.append(f" · 来源 {item.get('source', '?')}")
    if (item.get("confidence") or 1.0) < 0.6:
        bits.append(" · ⚠️ 低置信")
    return "".join(bits)


def render_section(day: str, grouped: dict[str, list[dict[str, Any]]]) -> str:
    """Render one day's digest section wrapped in idempotency markers."""
    lines = [f"<!-- BEGIN WATCH {day} -->", "", f"## {day}", ""]
    if not grouped:
        lines += ["_本次运行没有发现新作。_", ""]
    for name, items in grouped.items():
        lines.append(f"### {name}　`{len(items)} 条新作`")
        lines.append("")
        lines.extend("- " + _item_line(i) for i in items)
        lines.append("")
    lines.append(f"<!-- END WATCH {day} -->")
    return "\n".join(lines)


def upsert_watch_digest(day: str, section: str) -> None:
    """Insert/replace the day's section, newest first (same convention as core.upsert_digest)."""
    if WATCH_DIGEST_MD.exists():
        content = WATCH_DIGEST_MD.read_text(encoding="utf-8")
    else:
        content = WATCH_DIGEST_HEADER
    begin, endm = f"<!-- BEGIN WATCH {day} -->", f"<!-- END WATCH {day} -->"
    if begin in content and endm in content:
        pre = content[: content.index(begin)]
        post = content[content.index(endm) + len(endm) :].lstrip("\n")
        content = pre + section + "\n" + post
    elif "<!-- BEGIN WATCH " in content:
        idx = content.index("<!-- BEGIN WATCH ")
        content = content[:idx] + section + "\n" + content[idx:]
    else:
        content = content.rstrip("\n") + "\n\n" + section
    WATCH_DIGEST_MD.write_text(content, encoding="utf-8")


# ------------------------------------------------------------------
# Run
# ------------------------------------------------------------------

def run(
    only: str | None = None,
    *,
    use_network: bool = True,
    force: bool = False,
    push: bool = True,
    request_interval: float | None = None,
) -> dict[str, Any]:
    """Scan every enabled researcher and return what is new.

    Returns ``{"run_id", "day", "new_items", "grouped", "baselined", "skipped",
    "errors", "pushed_to"}``.
    """
    from glean.config import WATCH_REQUEST_INTERVAL

    delay = WATCH_REQUEST_INTERVAL if request_interval is None else request_interval
    state = load_state()
    researchers = state.setdefault("researchers", {})

    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    day = datetime.now().strftime("%Y-%m-%d")

    new_items: list[dict[str, Any]] = []
    grouped: dict[str, list[dict[str, Any]]] = {}
    baselined: list[str] = []
    skipped: list[str] = []
    errors: list[str] = []

    entries = [e for e in load_watchlist() if e.get("enabled", True)]
    if only:
        entries = [e for e in entries if e["key"] == slugify(only)]

    for i, entry in enumerate(entries):
        if i and delay:
            time.sleep(delay)
        key = entry["key"]
        try:
            items = collect_items(entry, use_network=use_network)
        except Exception as exc:  # never let one bad page abort the whole run
            errors.append(f"{entry['name']}: {type(exc).__name__}: {exc}")
            continue

        for it in items:
            it["fingerprint"] = fingerprint(it)
        # keep only recent items when seeding, to bound state growth
        if entry.get("homepage"):
            cutoff = datetime.now().year - WATCH_LOOKBACK_YEARS
            items = [it for it in items if (it.get("year") or cutoff + 1) >= cutoff]

        rec = researchers.get(key)
        if rec is None:
            researchers[key] = {
                "name": entry["name"],
                "baseline": True,
                "last_checked": datetime.now(timezone.utc).isoformat(),
                "fingerprints": [it["fingerprint"] for it in items][-WATCH_MAX_ITEMS:],
                "sources": sorted({it.get("source", "?") for it in items}),
            }
            baselined.append(f"{entry['name']}（{len(items)} 条基线）")
            if not force:
                continue
            fresh = items
        else:
            seen = set(rec.get("fingerprints", []))
            fresh = [it for it in items if it["fingerprint"] not in seen]
            rec["last_checked"] = datetime.now(timezone.utc).isoformat()
            rec["fingerprints"] = (
                rec.get("fingerprints", []) + [it["fingerprint"] for it in fresh]
            )[-WATCH_MAX_ITEMS:]
            rec["sources"] = sorted(set(rec.get("sources", [])) | {it.get("source", "?") for it in fresh})
            if not fresh:
                skipped.append(entry["name"])

        for it in fresh:
            enriched = dict(it)
            enriched["key"] = key
            enriched["researcher"] = entry["name"]
            new_items.append(enriched)
        if fresh:
            grouped.setdefault(entry["name"], []).extend(fresh)

    save_state(state)

    pushed_to: list[str] = []
    if new_items:
        upsert_watch_digest(day, render_section(day, grouped))
        if push:
            try:
                from glean import notify

                pushed_to = notify.push(new_items, day=day) or []
            except Exception as exc:
                errors.append(f"push: {type(exc).__name__}: {exc}")
        # log after pushing so the audit trail records where each item landed
        append_events(new_items, pushed_to, run_id)
    else:
        upsert_watch_digest(day, render_section(day, {}))

    return {
        "run_id": run_id,
        "day": day,
        "new_items": new_items,
        "grouped": grouped,
        "baselined": baselined,
        "skipped": skipped,
        "errors": errors,
        "pushed_to": pushed_to,
    }
