"""Monitor CCF-A conferences & journals for new CFP / program / accepted papers.

Source order (asymmetric on purpose)
------------------------------------
``ccfddl``   CFP announcements. ccfddl.com's RSS states each deadline together
             with its CCF rank and official site — a *structured* signal, so it
             drives CFP detection instead of fragile scraping.
``homepage`` Program and accepted-paper lists, which exist nowhere else.

DBLP is deliberately **not** fetched: every dblp.org endpoint now answers with
an anti-bot interstitial. DBLP URLs are still stored and shown as a human
reference link (see :mod:`glean.venueparse`).

Scope
-----
This module owns only the *venue-specific* parts: ``ccf.md``, the catalogue
sync, the three sources, and the digest wording. The diff / baseline / push /
audit mechanics are shared with the researcher monitor and live in
:mod:`glean.monitor` — see :data:`_SPEC` for how this subsystem plugs in.

State model
-----------
``ccf.md`` (Markdown, checkbox list) is the source of truth for *which* venues
are checked — ticking/unticking is the supported way to subscribe and
unsubscribe. ``data/ccf_state.json`` holds only the fingerprints already seen,
which is what makes "new" well defined. A venue's **first** run seeds the
baseline silently instead of pushing its whole history (override with
``--force``).
"""

from __future__ import annotations

import re
from datetime import datetime
from typing import Any, Iterable

from glean import monitor
from glean.config import (
    CCF_DIGEST_MD,
    CCF_EVENTS,
    CCF_ITEM_KINDS,
    CCF_MAX_ITEMS,
    CCF_MD,
    CCF_STATE,
)
from glean.monitor import fingerprint, kind_of, slugify
from glean.venueparse import (
    fetch_crossref_issues,
    fetch_rss,
    parse_ccfddl,
    parse_venue_page,
)

KIND_ICONS = {
    "cfp": "\U0001f4e2",  # 📢
    "program": "\U0001f4c5",  # 📅
    "papers": "\U0001f4c4",  # 📄
    "other": "\U0001f517",  # 🔗
}

KIND_LABELS = {
    "cfp": "征稿 (CFP)",
    "program": "会议日程",
    "papers": "接收论文",
    "other": "其它",
}

CCF_DIGEST_HEADER = """# CCF-A 会议 / 期刊监控

> 自动生成，勿手工编辑正文（勾选名单请改 [`ccf.md`](ccf.md)）。
> 每次 `arxiv_daily.py ccf run` 只追加**新发现**的 CFP / Program / 接收论文列表。
> 用法与故障排查见 [docs/user-guide/ccf-watching.md](docs/user-guide/ccf-watching.md)。

"""

_SECTIONS = (
    ("conference", "## 会议", "<!-- 用 `ccf enable/disable <名称>` 或编辑本文件勾选。 -->"),
    ("journal", "## 期刊", "<!-- 期刊没有截稿站收录，条目来自人工整理（见 glean/ccf_catalog.py）。 -->"),
)

# 本子系统在共享引擎里的静态身份。
_SPEC = monitor.MonitorSpec(
    namespace="ccf",
    subject_field="venue",
    state_key="venues",
    digest_marker="CCF",
    item_noun="更新",
    max_items=CCF_MAX_ITEMS,
)


def _kind_of(value: str | None) -> str:
    return kind_of(value, CCF_ITEM_KINDS)


# ------------------------------------------------------------------
# ccf.md — parse / render / mutate
# ------------------------------------------------------------------

_ENTRY_RE = re.compile(r"^-\s+\[([ xX])\]\s+(.*)$")
_FIELD_RE = re.compile(r"^-\s*([A-Za-z]+):\s*(.*)$")


def _parse_ccf_md(text: str) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    kind = "conference"
    cur: dict[str, Any] | None = None

    for raw in text.splitlines():
        stripped = raw.strip()
        if stripped.startswith("## "):
            heading = stripped[3:].strip()
            kind = "journal" if "期刊" in heading else "conference"
            continue

        m = _ENTRY_RE.match(stripped)
        if m:
            rest = re.sub(r"^\*\*(.+?)\*\*", r"\1", m.group(2).strip())
            name, sep, full = rest.partition("—")
            if not sep:
                name, sep, full = rest.partition(" - ")
            name = name.strip()
            cur = {
                "name": name,
                "key": slugify(name),
                "kind": kind,
                "full": (full.strip() if sep else "") or name,
                "area": "",
                "homepage": "",
                "dblp": "",
                "ccf": "A",
                "issn": "",
                "enabled": m.group(1).lower() == "x",
            }
            entries.append(cur)
            continue

        if cur is not None and raw[:1] in (" ", "\t"):
            fm = _FIELD_RE.match(stripped)
            if fm and fm.group(1).lower() in (
                "area", "homepage", "dblp", "ccf", "full", "name", "issn"
            ):
                cur[fm.group(1).lower()] = fm.group(2).strip()
    return entries


def load_venues() -> list[dict[str, Any]]:
    """Parse ccf.md; returns [] when the file is absent."""
    if not CCF_MD.exists():
        return []
    return _parse_ccf_md(CCF_MD.read_text(encoding="utf-8"))


def _preamble() -> str:
    if not CCF_MD.exists():
        return (
            "# CCF-A 会议 / 期刊监控名单\n\n"
            "> 勾选（`[x]`）即监控；取消勾选（`[ ]`）即暂停，不会发起任何网络请求。\n"
            "> 目录来源：ccfddl.com RSS + 人工补充（见 `glean/ccf_catalog.py`）。\n"
            "> 用法见 [docs/user-guide/ccf-watching.md](docs/user-guide/ccf-watching.md)。\n"
        )
    text = CCF_MD.read_text(encoding="utf-8")
    for i, line in enumerate(text.splitlines()):
        if line.strip().startswith("## "):
            return "\n".join(text.splitlines()[:i]).rstrip() + "\n"
    return ""


def _write_ccf_md(entries: Iterable[dict[str, Any]], preamble: str) -> None:
    parts = [preamble.rstrip(), ""]
    for kind, heading, hint in _SECTIONS:
        parts += [heading, ""]
        rows = [e for e in entries if e.get("kind", "conference") == kind]
        if not rows:
            parts += [hint, ""]
            continue
        for e in rows:
            box = "x" if e.get("enabled", True) else " "
            label = f"- [{box}] **{e['name']}**"
            if e.get("full") and e["full"] != e["name"]:
                label += f" — {e['full']}"
            parts.append(label)
            for field in ("area", "homepage", "dblp", "ccf", "issn"):
                if e.get(field):
                    parts.append(f"  - {field}: {e[field]}")
            parts.append("")
    CCF_MD.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")


def _save(entries: list[dict[str, Any]]) -> None:
    _write_ccf_md(entries, _preamble())


def _blank(
    name: str,
    kind: str = "conference",
    full: str = "",
    area: str = "",
    homepage: str = "",
    dblp: str = "",
    ccf: str = "A",
    enabled: bool = True,
    issn: str = "",
) -> dict[str, Any]:
    return {
        "name": name.strip(),
        "key": slugify(name),
        "kind": kind,
        "full": full or name.strip(),
        "area": area,
        "homepage": homepage,
        "dblp": dblp,
        "ccf": ccf,
        "issn": issn,
        "enabled": enabled,
    }


def add_venue(
    name: str,
    kind: str = "conference",
    full: str = "",
    area: str = "",
    homepage: str = "",
    dblp: str = "",
    ccf: str = "A",
    issn: str = "",
    enabled: bool = True,
) -> dict[str, Any]:
    """Append a venue to ccf.md. Raises if the name already exists."""
    name = (name or "").strip()
    homepage = (homepage or "").strip()
    if not name:
        raise ValueError("必须提供名称")
    entries = load_venues()
    key = slugify(name)
    if any(e["key"] == key for e in entries):
        raise ValueError(f"已存在同名监控对象: {name}")
    if not homepage:
        raise ValueError("必须提供 homepage（监控只能基于公开主页，没有主页无从扫描）")
    entry = _blank(name, kind, full, area, homepage, dblp, ccf, enabled, issn)
    entries.append(entry)
    _save(entries)
    return entry


def remove_venue(name: str) -> bool:
    """Remove a venue and forget its seen-state. Returns True if removed."""
    entries = load_venues()
    key = slugify(name)
    kept = [e for e in entries if e["key"] != key]
    if len(kept) == len(entries):
        return False
    _save(kept)
    state = load_state()
    if key in state.get("venues", {}):
        state["venues"].pop(key)
        save_state(state)
    return True


def set_enabled(name: str, enabled: bool) -> bool:
    """Tick / untick one venue. Returns True if found."""
    entries = load_venues()
    key = slugify(name)
    hit = False
    for e in entries:
        if e["key"] == key:
            e["enabled"] = enabled
            hit = True
    if hit:
        _save(entries)
    return hit


def set_enabled_area(area: str, enabled: bool) -> list[str]:
    """Bulk tick / untick every venue whose ``area`` contains ``area``."""
    needle = (area or "").strip().lower()
    entries = load_venues()
    touched: list[str] = []
    for e in entries:
        if needle and needle in (e.get("area") or "").lower():
            e["enabled"] = enabled
            touched.append(e["name"])
    if touched:
        _save(entries)
    return touched


def sync_catalog(default_enabled: bool = True) -> tuple[int, int]:
    """Merge ``glean.ccf_catalog`` into ccf.md.

    Existing entries keep their tick state (that is the user's decision);
    only metadata is refreshed and genuinely new venues are appended.
    Returns ``(added, updated)``.
    """
    from glean.ccf_catalog import CCF_A_CONFERENCES, CCF_A_JOURNALS

    existing = {e["key"]: e for e in load_venues()}
    added = updated = 0
    for kind, rows in (("conference", CCF_A_CONFERENCES), ("journal", CCF_A_JOURNALS)):
        for row in rows:
            key = slugify(row["name"])
            cur = existing.get(key)
            if cur is None:
                existing[key] = _blank(
                    row["name"], kind, row.get("full", ""), row.get("area", ""),
                    row.get("homepage", ""), row.get("dblp", ""),
                    row.get("ccf", "A"), default_enabled, row.get("issn", ""),
                )
                added += 1
                continue
            for field in ("full", "area", "homepage", "dblp", "ccf", "issn"):
                value = row.get(field, "")
                if value and cur.get(field) != value:
                    cur[field] = value
                    updated += 1
    _save(existing.values())
    return added, updated


# ------------------------------------------------------------------
# Collection
# ------------------------------------------------------------------

def collect_items(
    entry: dict[str, Any],
    *,
    use_network: bool = True,
    rss_text: str | None = None,
) -> list[dict[str, Any]]:
    """Gather a venue's CFP / program / accepted-paper items.

    ccfddl comes first so its structured CFP entries win duplicates; the
    homepage adds whatever else it exposes. Deduped by fingerprint.
    """
    if not use_network:
        return []

    items: list[dict[str, Any]] = []
    if entry.get("kind", "conference") == "conference" and rss_text:
        items.extend(
            parse_ccfddl(
                rss_text,
                entry["name"],
                min_year=datetime.now().year - 1,
            )
        )
    elif entry.get("kind") == "journal" and entry.get("issn"):
        # Journals have no CFP and their publisher pages are JS-rendered, so
        # Crossref's volume/issue index is the only usable "what's new" signal.
        items.extend(
            fetch_crossref_issues(
                entry["issn"], entry["name"], entry.get("homepage", "")
            )
        )
    if entry.get("homepage"):
        items.extend(parse_venue_page(entry["homepage"]))

    out: list[dict[str, Any]] = []
    seen: set[str] = set()
    for it in items:
        it["kind"] = _kind_of(it.get("kind"))
        it["venue"] = it.get("venue") or entry["name"]
        it["fingerprint"] = fingerprint(it)
        if not it.get("title") or it["fingerprint"] in seen:
            continue
        seen.add(it["fingerprint"])
        out.append(it)
    return out


# ------------------------------------------------------------------
# State · events · digest — delegated to the shared engine
# ------------------------------------------------------------------

def load_state() -> dict[str, Any]:
    """Read ``data/ccf_state.json`` (the already-seen fingerprints)."""
    return monitor.load_state(CCF_STATE, _SPEC.state_key)


def save_state(state: dict[str, Any]) -> None:
    """Write ``data/ccf_state.json`` back to disk."""
    monitor.save_state(CCF_STATE, state)


def append_events(items: list[dict[str, Any]], pushed_to: list[str], run_id: str) -> None:
    """Append one JSON line per new item to ``ccf_events.jsonl``."""
    monitor.append_events(CCF_EVENTS, items, pushed_to, run_id, _SPEC.subject_field)


def load_events(limit: int = 200) -> list[dict[str, Any]]:
    """Most recent CCF events, newest first."""
    return monitor.load_events(CCF_EVENTS, limit)


# ------------------------------------------------------------------
# Digest
# ------------------------------------------------------------------

def _item_line(item: dict[str, Any]) -> str:
    icon = KIND_ICONS.get(item.get("kind", "other"), KIND_ICONS["other"])
    bits = [f"{icon} **{item['title']}**"]
    meta = [KIND_LABELS.get(item.get("kind", "other"), "其它")]
    if item.get("year"):
        meta.append(str(item["year"]))
    if item.get("deadline"):
        meta.append(f"截稿 {item['deadline']}")
    bits.append(" — " + " · ".join(meta))
    if item.get("url"):
        bits.append(f" — [链接]({item['url']})")
    bits.append(f" · 来源 {item.get('source', '?')}")
    if (item.get("confidence") or 1.0) < 0.6:
        bits.append(" · ⚠️ 低置信")
    return "".join(bits)


def render_section(day: str, grouped: dict[str, list[dict[str, Any]]]) -> str:
    """Render one day's digest section wrapped in ``<!-- BEGIN CCF <day> -->``."""
    return monitor.render_section(_SPEC, day, grouped, _item_line)


def upsert_ccf_digest(day: str, section: str) -> None:
    """Insert/replace the day's section, newest first."""
    monitor.upsert_digest(
        CCF_DIGEST_MD, CCF_DIGEST_HEADER, _SPEC.digest_marker, day, section
    )


# ------------------------------------------------------------------
# Run
# ------------------------------------------------------------------

def _prepare() -> tuple[list[str], str]:
    """Download the ccfddl RSS **once per run**, not once per venue."""
    try:
        return [], fetch_rss()
    except Exception as exc:
        return [f"ccfddl: {type(exc).__name__}: {exc}"], ""


def _job() -> monitor.MonitorJob:
    """Build the engine job from the *current* module globals.

    Reading the globals here (rather than at import time) is what lets tests
    redirect every path into ``tmp_path`` via ``monkeypatch.setattr``.
    """
    return monitor.MonitorJob(
        spec=_SPEC,
        entries=load_venues,
        state_path=CCF_STATE,
        events_path=CCF_EVENTS,
        digest_path=CCF_DIGEST_MD,
        digest_header=CCF_DIGEST_HEADER,
        render_item=_item_line,
        prepare=_prepare,
        collect=lambda entry, use_network, rss_text: collect_items(
            entry, use_network=use_network, rss_text=rss_text
        ),
    )


def run(
    only: str | None = None,
    *,
    use_network: bool = True,
    force: bool = False,
    push: bool = True,
    request_interval: float | None = None,
) -> dict[str, Any]:
    """Scan every ticked venue and return what is new.

    Returns ``{"run_id", "day", "new_items", "grouped", "baselined", "skipped",
    "errors", "pushed_to"}``.
    """
    from glean.config import CCF_REQUEST_INTERVAL

    delay = CCF_REQUEST_INTERVAL if request_interval is None else request_interval
    return monitor.run_monitor(
        _job(),
        only=only,
        use_network=use_network,
        force=force,
        push=push,
        delay=delay,
    )
