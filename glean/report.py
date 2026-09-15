"""Render a day's digest into a single, self-contained HTML file.

Why this exists
---------------
``arXiv-schedule.md`` is the source of truth, but a Markdown file is a poor
deliverable for a scheduled run: it has to be opened in an editor or a
Markdown viewer, and the recommended-paper tables render as raw pipes in most
mail clients. This module writes ``exports/arxiv-digest-<day>.html`` — one file
that opens straight from the filesystem (``file://``) in any browser.

Two snapshot families live here, and they share everything that is not domain
knowledge (:mod:`glean.htmlkit` owns the shell, the CSS and the behaviour):

``arxiv-digest-<day>.html``      the arXiv daily digest, rendered from
                                 ``data/<day>.json`` plus the read-back
                                 recommendation blocks.
``<namespace>-digest-<day>.html``  one day of a *monitor* run — researchers
                                 (``watch``) or CCF venues (``ccf``). The
                                 monitor renderer is domain-agnostic: wording,
                                 kind vocabulary and icons arrive in a
                                 :class:`MonitorView` supplied by the caller,
                                 so this module never imports the monitors.

Design constraints (deliberate, do not "simplify" them away)
------------------------------------------------------------
1. **Stdlib only.** ``dependencies = []`` in ``pyproject.toml``; Jinja2 lives
   in the ``web`` extra. Importing it here would break ``fetch``/``daily`` for
   a CLI-only install, so the HTML is assembled by hand and every interpolated
   value goes through :func:`glean.htmlkit.escape`.
2. **No CDN.** The web UI pulls Tailwind / htmx / Alpine from the network. A
   snapshot must stay readable offline and inside ``file://``, so the
   stylesheet and the behaviour are inlined.
3. **Readable without JavaScript.** Filtering/search/collapse are progressive
   enhancements; the full list, abstracts and links are static markup.
4. **Fully static means no feedback round-trip.** Rating buttons do not POST
   anywhere (there is no server behind a file). They copy the equivalent CLI
   command instead, which keeps the loop honest: the file never pretends to
   write to the profile.

The recommendation blocks are *not* recomputed here: they are read back out of
the digest so whatever the agent wrote (including judgement calls that keywords
cannot express) shows up verbatim. Only when the block is still the untouched
placeholder does this fall back to a score-ranked top-N.

A monitor snapshot additionally carries a **run report** (baseline / unchanged
/ push channels / fetch errors). That block exists because "no new work" is
ambiguous: either a genuinely quiet day, or a source that silently failed. A
page that only says "nothing new" cannot be told apart from a broken run, so
the run report states the evidence the run actually produced.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping

from glean import htmlkit
from glean.config import CATEGORIES, DIGEST_MD, EXPORT_DIR
from glean.core import load_day_data
from glean.htmlkit import escape

# Placeholder written by ``core.day_section`` until the agent fills the block.
_PENDING = "_待 agent 分析填写_"

# Markdown-table row of a recommendation block, e.g.
# | ★★★★★ | **Title** — [2609.12715](https://arxiv.org/abs/2609.12715) · [📄](#20260914-2609.12715) (cs.LO) | 理由 |
_ROW_TITLE_RE = re.compile(r"\*\*(.+?)\*\*")
_ROW_ID_RE = re.compile(r"\[(\d{4}\.\d{4,5})\]\(https://arxiv\.org/abs/")
_ROW_CAT_RE = re.compile(r"\(([a-z-]+\.[A-Za-z]{2})\)\s*$")


def _day_section_text(day: str) -> str:
    """Return the ``<!-- BEGIN day --> … <!-- END day -->`` block, or ''."""
    if not DIGEST_MD.exists():
        return ""
    content = DIGEST_MD.read_text(encoding="utf-8")
    begin, end = f"<!-- BEGIN {day} -->", f"<!-- END {day} -->"
    if begin not in content or end not in content:
        return ""
    i = content.index(begin)
    return content[i : content.index(end, i)]


def _parse_row(cells: list[str], symbol: str) -> dict[str, Any] | None:
    """Turn one markdown table row into a recommendation dict."""
    level_cell, paper_cell, reason_cell = (cells + ["", "", ""])[:3]
    level = level_cell.strip()
    if not level.startswith(symbol) or "推荐" in level_cell:
        return None  # header row (含「推荐」) 或无关行
    m_id = _ROW_ID_RE.search(paper_cell)
    m_title = _ROW_TITLE_RE.search(paper_cell)
    if not m_id and not m_title:
        return None
    m_cat = _ROW_CAT_RE.search(paper_cell.strip())
    return {
        "level": level,
        "count": level.count(symbol),
        "title": m_title.group(1).strip() if m_title else paper_cell.strip(),
        "id": m_id.group(1) if m_id else "",
        "category": m_cat.group(1) if m_cat else "",
        "reason": reason_cell.strip().replace("`", ""),
    }


def parse_recommendations(day: str) -> dict[str, list[dict[str, Any]]]:
    """Read the agent-written ★/🧐 blocks back out of the digest.

    Returns ``{"star": [...], "expand": [...]}``; a key is absent when its
    block is still the placeholder (or the day has no section at all).
    """
    sec = _day_section_text(day)
    out: dict[str, list[dict[str, Any]]] = {}
    if not sec:
        return out
    for symbol, heading, key in (
        ("★", "### 📌", "star"),
        ("🧐", "### 🧐", "expand"),
    ):
        i = sec.find(heading)
        if i == -1:
            continue
        j = sec.find("\n### ", i + 1)
        block = sec[i : j if j != -1 else len(sec)]
        if _PENDING in block:
            continue
        rows: list[dict[str, Any]] = []
        for line in block.splitlines():
            line = line.strip()
            if not line.startswith("|"):
                continue
            cells = [c.strip() for c in line.strip("|").split("|")]
            if set("".join(cells)) <= set("-: "):  # 分隔行
                continue
            rec = _parse_row(cells, symbol)
            if rec:
                rows.append(rec)
        if rows:
            out[key] = rows
    return out


def _fallback_recommendations(papers: list[dict[str, Any]], limit: int = 5) -> list[dict[str, Any]]:
    """Score-ranked top-N, used only when the digest block is still empty."""
    ranked = sorted(
        (p for p in papers if p.get("hits_star") or p.get("hits_expand")),
        key=lambda p: -(p.get("score_star", 0) + p.get("score_expand", 0)),
    )[:limit]
    out = []
    for p in ranked:
        bits = []
        if p.get("hits_star"):
            bits.append("★ " + ", ".join(p["hits_star"]))
        if p.get("hits_expand"):
            bits.append("🧐 " + ", ".join(p["hits_expand"]))
        out.append(
            {
                "level": "★" * min(5, max(1, (p.get("score_star", 0) + 1) // 2)),
                "count": 0,
                "title": p["title"],
                "id": p["id"],
                "category": p["primary"],
                "reason": "关键词命中(" + "；".join(bits) + ")，按权重和自动选取；agent 尚未填写人工判断",
            }
        )
    return out


def group_by_category(papers: list[dict[str, Any]]) -> list[tuple[str, list[dict[str, Any]]]]:
    """Group papers the same way the Markdown digest does (category → papers)."""
    by_cat: dict[str, list[dict[str, Any]]] = {}
    for p in papers:
        key = (
            p["primary"]
            if p["primary"] in CATEGORIES
            else next((c for c in p["categories"] if c in CATEGORIES), p["primary"])
        )
        by_cat.setdefault(key, []).append(p)
    order = CATEGORIES + sorted(set(by_cat) - set(CATEGORIES))
    return [
        (cat, sorted(by_cat[cat], key=lambda p: (-(p.get("score_star", 0) + p.get("score_expand", 0)), p["title"])))
        for cat in order
        if cat in by_cat
    ]


# ------------------------------------------------------------------
# arXiv digest
# ------------------------------------------------------------------


def _rec_items(rows: list[dict[str, Any]], cls: str) -> str:
    out = []
    for r in rows:
        jump = f'<a class="jump" href="#p-{escape(r["id"])}">↓ 全文</a>' if r["id"] else ""
        cat = f'<span class="cat">{escape(r["category"])}</span>' if r["category"] else ""
        title = (
            f'<a href="https://arxiv.org/abs/{escape(r["id"])}" target="_blank" rel="noopener">{escape(r["title"])}</a>'
            if r["id"]
            else escape(r["title"])
        )
        out.append(
            f'<li class="rec {cls}">'
            f'<div><span class="stars">{escape(r["level"])}</span>'
            f'<span class="title">{title}</span>{cat}{jump}</div>'
            f'<p class="why">{escape(r["reason"])}</p>'
            f"</li>"
        )
    return "\n".join(out)


def _paper_article(p: dict[str, Any]) -> str:
    pid = escape(p["id"])
    cross = [c for c in p.get("categories", []) if c != p.get("primary")]
    cross_s = " · cross: " + ", ".join(escape(c) for c in cross) if cross else ""
    badges = []
    for k in p.get("hits_star", []):
        badges.append(f'<span class="badge star">★ {escape(k)}</span>')
    for k in p.get("hits_expand", []):
        badges.append(f'<span class="badge expand">🧐 {escape(k)}</span>')
    total = p.get("score_star", 0) + p.get("score_expand", 0)
    if total:
        badges.append(f'<span class="badge">权重和 {total}</span>')
    authors = ", ".join(p.get("authors", [])[:8]) + (" et al." if len(p.get("authors", [])) > 8 else "")
    cmd = f"python -X utf8 arxiv_daily.py feedback {p['id']} --stars 4 --curiosity 3"
    search_blob = " ".join(
        [p.get("title", ""), " ".join(p.get("authors", [])), p.get("abstract", "")]
    ).lower()
    return (
        f'<article class="paper" data-item id="p-{pid}" data-cat="{escape(p.get("primary", ""))}" '
        f'data-flag="{1 if total else 0}" data-text="{escape(search_blob)}">'
        f'<h4><a href="{escape(p.get("abs_url", ""))}" target="_blank" rel="noopener">{escape(p.get("title", ""))}</a></h4>'
        f'<div class="pmeta">{pid}{escape(p.get("version", ""))} · {escape(p.get("primary", ""))}{cross_s}</div>'
        f'<div class="badges">{"".join(badges)}</div>'
        f'<div class="authors">{escape(authors)}</div>'
        f'<details><summary>摘要</summary><p>{escape(p.get("abstract", ""))}</p></details>'
        f'<div class="actions">'
        f'<a href="{escape(p.get("abs_url", ""))}" target="_blank" rel="noopener">Abstract</a>'
        f'<a href="{escape(p.get("pdf_url", ""))}" target="_blank" rel="noopener">PDF</a>'
        f'<button data-copy="{escape(cmd)}" title="复制命令到剪贴板，按需改星级">⧉ 复制打分命令</button>'
        f"</div>"
        f"</article>"
    )


def build_html(day: str) -> str | None:
    """Return the standalone HTML for ``day``, or ``None`` if it has no data."""
    data = load_day_data(day)
    if not data:
        return None
    papers: list[dict[str, Any]] = data.get("papers", [])
    window = data.get("window_utc") or ["", ""]
    n_star = sum(1 for p in papers if p.get("hits_star"))
    n_expand = sum(1 for p in papers if p.get("hits_expand"))

    recs = parse_recommendations(day)
    star_rows = recs.get("star")
    expand_rows = recs.get("expand")
    auto = star_rows is None and expand_rows is None
    if auto:
        star_rows = _fallback_recommendations(papers)
        expand_rows = []

    body: list[str] = []
    body.append("<h2>📌 重点关注 / 🧐 视野扩展</h2>")
    if auto:
        body.append(
            '<p class="note">digest 中的推荐小节仍是占位符，下面按「命中关键词的权重和」自动排序，'
            "供人工复核；agent 填写 <code>arXiv-schedule.md</code> 后重跑 "
            "<code>arxiv_daily.py html --date " + escape(day) + "</code> 即替换为人工判断。</p>"
        )
    if star_rows:
        body.append('<h3>📌 重点关注</h3><ol class="recs">' + _rec_items(star_rows, "star") + "</ol>")
    if expand_rows:
        body.append('<h3>🧐 视野扩展</h3><ol class="recs">' + _rec_items(expand_rows, "expand") + "</ol>")
    if not star_rows and not expand_rows:
        body.append('<p class="empty">本期没有关键词命中的论文。</p>')

    groups = group_by_category(papers)
    body.append(f"<h2>分类清单（共 {len(papers)} 篇）</h2>")
    for cat, ps in groups:
        body.append(f'<section data-group><h3>{escape(cat)}（{len(ps)}）</h3>')
        body.extend(_paper_article(p) for p in ps)
        body.append("</section>")

    cat_options = ['<option value="">全部类别</option>'] + [
        f'<option value="{escape(cat)}">{escape(cat)}（{len(ps)}）</option>' for cat, ps in groups
    ]
    day_fmt = f"{day[:4]}-{day[4:6]}-{day[6:]}"
    meta = (
        f"窗口(UTC): {str(window[0])[:16].replace('T', ' ')} → "
        f"{str(window[1])[:16].replace('T', ' ')} · 共 {len(papers)} 篇 · "
        f"★ 命中 {n_star} 篇 / 🧐 命中 {n_expand} 篇"
    )
    footer = (
        f"<p>由 paper-glean 生成于 {escape(datetime.now().strftime('%Y-%m-%d %H:%M'))}。"
        f"事实源：<code>data/{escape(day)}.json</code> 与 <code>arXiv-schedule.md</code>；"
        "本文件是派生产物（<code>exports/</code>，未纳入版本库）。"
        "打分请回到本地 Web 服务，或用上面复制的 CLI 命令——静态快照本身不回写画像。</p>"
    )
    return htmlkit.page(
        title=f"arXiv Daily Digest · {day_fmt}",
        meta=meta,
        body="\n".join(body),
        footer=footer,
        controls_html=htmlkit.controls(
            placeholder="搜索标题 / 作者 / 摘要…",
            cat_options=cat_options,
            flag_label="只看命中",
            total=len(papers),
        ),
    )


def render_day(day: str, out: Path | None = None) -> Path | None:
    """Write ``exports/arxiv-digest-<day>.html`` and return its path.

    Returns ``None`` when the day has no ``data/<day>.json`` — that is a normal
    outcome (e.g. a fetch that returned nothing), not an error.
    """
    html_text = build_html(day)
    if html_text is None:
        return None
    target = Path(out) if out else EXPORT_DIR / f"arxiv-digest-{day}.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html_text, encoding="utf-8")
    return target


def latest_export() -> Path | None:
    """Newest ``exports/arxiv-digest-*.html``, or ``None``."""
    if not EXPORT_DIR.exists():
        return None
    files = sorted(EXPORT_DIR.glob("arxiv-digest-*.html"), reverse=True)
    return files[0] if files else None


# ------------------------------------------------------------------
# Monitor digest (researchers / CCF venues)
#
# The two monitors differ only in wording and in their kind vocabulary, so the
# difference is carried by a :class:`MonitorView` instead of by a second
# renderer. Keeping the wording at the call site (``glean/cli.py``) is what
# lets this module stay ignorant of ``watch`` / ``ccf``.
# ------------------------------------------------------------------


@dataclass(frozen=True)
class MonitorView:
    """How one monitor's snapshot is presented.

    Attributes:
        namespace: ``watch`` / ``ccf`` — also the export filename prefix and the
            CLI entry point quoted in the footer.
        title: page heading.
        noun: item量词 (``新作`` / ``更新``), used in every count phrase.
        digest_name: Markdown fact source, quoted in the footer.
        kind_labels: ``kind`` → human label. Owned by the monitor module; the
            snapshot reuses it so the HTML and the digest cannot disagree.
        kind_icons: ``kind`` → emoji prefix.
    """

    namespace: str
    title: str
    noun: str
    digest_name: str
    kind_labels: Mapping[str, str] = field(default_factory=dict)
    kind_icons: Mapping[str, str] = field(default_factory=dict)


def monitor_export_path(namespace: str, day: str, out: Path | None = None) -> Path:
    """Where a monitor snapshot for ``day`` lives (or would live)."""
    return Path(out) if out else EXPORT_DIR / f"{namespace}-digest-{day}.html"


def _monitor_item(view: MonitorView, item: Mapping[str, Any]) -> str:
    kind = str(item.get("kind") or "other")
    icon = view.kind_icons.get(kind, "")
    label = view.kind_labels.get(kind, "其它")
    low_conf = (item.get("confidence") or 1.0) < 0.6

    meta = [f"{icon} {label}".strip()]
    for key in ("year", "venue"):
        if item.get(key):
            meta.append(str(item[key]))
    if item.get("deadline"):
        meta.append(f"截稿 {item['deadline']}")
    meta.append(f"来源 {item.get('source') or '?'}")

    title = str(item.get("title") or "")
    url = str(item.get("url") or "")
    head = (
        f'<a href="{escape(url)}" target="_blank" rel="noopener">{escape(title)}</a>'
        if url
        else escape(title)
    )
    warn = (
        '<div class="badges"><span class="badge warn">⚠️ 低置信，需人工确认</span></div>'
        if low_conf
        else ""
    )
    actions = (
        f'<div class="actions"><a href="{escape(url)}" target="_blank" rel="noopener">打开链接</a></div>'
        if url
        else ""
    )
    blob = " ".join([title, label, kind, str(item.get("venue") or ""), url]).lower()
    return (
        f'<article class="paper" data-item data-cat="{escape(kind)}" '
        f'data-flag="{1 if low_conf else 0}" data-text="{escape(blob)}">'
        f"<h4>{head}</h4>"
        f'<div class="pmeta">{" · ".join(escape(b) for b in meta)}</div>'
        f"{warn}{actions}</article>"
    )


def _blind_subjects(run: Mapping[str, Any]) -> list[str]:
    """条目本轮**一条内容都没取到**（0 指纹）——即「源不可达」的盲区。

    这是 ``watch`` / ``ccf`` 独有的失败模式：抓取是 fail-soft 的，主页挂掉只会
    让 ``collect`` 返回 ``[]``，于是「没有新作」与「完全没抓到」长得一模一样。
    ``run_monitor`` 因此单独记录 ``collected``（每个条目取回多少条），这里把它
    读成盲区清单。
    """
    collected = run.get("collected") or {}
    return [str(name) for name, n in collected.items() if not n]


def _monitor_notes(
    view: MonitorView, run: Mapping[str, Any], n_items: int, blind: list[str]
) -> list[str]:
    """把「本轮到底取到了什么」翻译成人话；0 条绝不等价于健康。"""
    errors = list(run.get("errors") or [])
    notes: list[str] = []
    if blind:
        notes.append(
            f'<p class="note">⚠️ 有 {len(blind)} 个条目<b>本轮一条内容都没取到</b>：'
            + escape("、".join(blind))
            + "。这通常是源不可达（主页挂掉且未配兜底源），而不是它真的没有新内容。"
            "分条证据见下方「本次运行」。</p>"
        )
    if errors:
        notes.append(
            f'<p class="note">⚠️ 抓取过程报了 {len(errors)} 个错误，明细见下方「本次运行」。</p>'
        )
    if not n_items and not blind and not errors:
        if run.get("baselined"):
            notes.append(
                "<p class=\"note\">本次是首次运行：只建立基线，不推送历史条目"
                "（加 <code>--force</code> 可强制推送）。从下一次起，"
                f"本页只出现真正新增的{escape(view.noun)}。</p>"
            )
        else:
            notes.append(
                f'<p class="note">本次运行没有发现{escape(view.noun)}。若连续多日如此，请核对下方'
                "「本次运行」的「各源取回」——「无新内容」与「抓取静默失败」在结果上是一样的。</p>"
            )
    return notes


def _monitor_run_report(
    day: str,
    run: Mapping[str, Any],
    n_items: int,
    n_subjects: int,
    scope: str | None,
    blind: list[str],
) -> str:
    """The evidence block: what was scanned, what failed, where it was pushed."""
    errors = list(run.get("errors") or [])
    collected = run.get("collected") or {}
    rows: list[tuple[str, str]] = [
        ("运行日期", escape(day)),
        ("运行编号", escape(run.get("run_id") or "—")),
        (
            "扫描范围",
            f"仅 <code>{escape(scope)}</code>（单条调试）" if scope else "全部启用条目",
        ),
        ("新增", f"{n_items} 条，涉及 {n_subjects} 个条目"),
    ]
    if collected:
        # 「各源取回」是判盲区的原始证据：0 条即该条目本轮完全失聪。
        detail = "；".join(
            f"{escape(name)} {n} 条" + ("（盲区）" if not n else "")
            for name, n in collected.items()
        )
        rows.append(("各源取回", detail))
    if run.get("baselined"):
        rows.append(("新建基线", escape("；".join(run["baselined"]))))
    if run.get("skipped"):
        rows.append(
            ("无变化", f"{len(run['skipped'])} 个条目：" + escape("、".join(run["skipped"])))
        )
    rows.append(
        (
            "推送通道",
            escape(", ".join(run.get("pushed_to") or [])) or "无（仅落盘 digest）",
        )
    )
    rows.append(
        (
            "抓取错误",
            f'<span class="err">{escape("；".join(errors))}</span>' if errors else "无",
        )
    )
    cells = "".join(f"<tr><th>{escape(k)}</th><td>{v}</td></tr>" for k, v in rows)
    return f'<h2>本次运行</h2><table class="run">{cells}</table>'


def build_monitor_html(
    view: MonitorView,
    day: str,
    grouped: Mapping[str, list[dict[str, Any]]] | None,
    *,
    run: Mapping[str, Any] | None = None,
    scope: str | None = None,
) -> str:
    """Return the standalone HTML for one monitor day.

    ``grouped`` maps a subject (researcher name / venue name) to its new items;
    an empty mapping is a legitimate outcome and still yields a page, because
    the run report is the point on a quiet day.
    """
    run = dict(run or {})
    groups = {name: list(items) for name, items in (grouped or {}).items()}
    n_items = sum(len(v) for v in groups.values())

    body: list[str] = []
    blind = _blind_subjects(run)
    body.extend(_monitor_notes(view, run, n_items, blind))
    if groups:
        body.append(f"<h2>本期新增（{n_items} 条 / {len(groups)} 个条目）</h2>")
    for name, items in groups.items():
        body.append(
            f'<section data-group><h3>{escape(name)}'
            f'<span class="badge">{len(items)} 条{escape(view.noun)}</span></h3>'
        )
        body.extend(_monitor_item(view, it) for it in items)
        body.append("</section>")
    body.append(_monitor_run_report(day, run, n_items, len(groups), scope, blind))

    kinds: dict[str, int] = {}
    for items in groups.values():
        for it in items:
            k = str(it.get("kind") or "other")
            kinds[k] = kinds.get(k, 0) + 1
    cat_options = ['<option value="">全部类型</option>'] + [
        f'<option value="{escape(k)}">'
        f'{escape((view.kind_icons.get(k, "") + " " + view.kind_labels.get(k, "其它")).strip())}（{n}）</option>'
        for k, n in kinds.items()
    ]

    meta = f"运行日期 {day} · 新增 {n_items} 条 · 涉及 {len(groups)} 个条目"
    footer = (
        f"<p>由 paper-glean 生成于 {escape(datetime.now().strftime('%Y-%m-%d %H:%M'))}。"
        f"事实源：<code>{escape(view.digest_name)}</code>（本文件是派生产物，"
        "<code>exports/</code> 未纳入版本库）。"
        f"重跑：<code>python -X utf8 arxiv_daily.py {escape(view.namespace)} run</code>。"
        "「无新内容」不等于「抓取正常」——请对照上方「本次运行」的抓取错误。</p>"
    )
    return htmlkit.page(
        title=f"{view.title} · {day}",
        meta=meta,
        body="\n".join(body),
        footer=footer,
        controls_html=htmlkit.controls(
            placeholder="搜索标题 / 来源 / 链接…",
            cat_options=cat_options,
            flag_label="只看低置信",
            total=n_items,
        ),
    )


def render_monitor_day(
    view: MonitorView,
    day: str,
    grouped: Mapping[str, list[dict[str, Any]]] | None,
    *,
    run: Mapping[str, Any] | None = None,
    scope: str | None = None,
    out: Path | None = None,
) -> Path:
    """Write ``exports/<namespace>-digest-<day>.html`` and return its path.

    Unlike :func:`render_day` there is no ``None`` outcome: a monitor day with
    zero new items still produces a snapshot, because proving "the scan ran and
    returned nothing" is exactly what a quiet day needs.
    """
    target = monitor_export_path(view.namespace, day, out)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        build_monitor_html(view, day, grouped, run=run, scope=scope), encoding="utf-8"
    )
    return target


def latest_monitor_export(namespace: str) -> Path | None:
    """Newest ``exports/<namespace>-digest-*.html``, or ``None``."""
    if not EXPORT_DIR.exists():
        return None
    files = sorted(EXPORT_DIR.glob(f"{namespace}-digest-*.html"), reverse=True)
    return files[0] if files else None


__all__ = [
    "MonitorView",
    "build_html",
    "build_monitor_html",
    "escape",
    "group_by_category",
    "latest_export",
    "latest_monitor_export",
    "monitor_export_path",
    "parse_recommendations",
    "render_day",
    "render_monitor_day",
]
