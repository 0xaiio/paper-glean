"""Render a day's digest into a single, self-contained HTML file.

Why this exists
---------------
``arXiv-schedule.md`` is the source of truth, but a Markdown file is a poor
deliverable for a scheduled run: it has to be opened in an editor or a
Markdown viewer, and the recommended-paper tables render as raw pipes in most
mail clients. This module writes ``exports/arxiv-digest-<day>.html`` — one file
that opens straight from the filesystem (``file://``) in any browser.

Design constraints (deliberate, do not "simplify" them away)
------------------------------------------------------------
1. **Stdlib only.** ``dependencies = []`` in ``pyproject.toml``; Jinja2 lives
   in the ``web`` extra. Importing it here would break ``fetch``/``daily`` for
   a CLI-only install, so the HTML is assembled by hand and every interpolated
   value goes through :func:`html.escape`.
2. **No CDN.** The web UI pulls Tailwind / htmx / Alpine from the network.
   A snapshot must stay readable offline and inside ``file://``, so the
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
"""

from __future__ import annotations

import html
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from glean.config import CATEGORIES, DIGEST_MD, EXPORT_DIR
from glean.core import load_day_data

# Placeholder written by ``core.day_section`` until the agent fills the block.
_PENDING = "_待 agent 分析填写_"

# Markdown-table row of a recommendation block, e.g.
# | ★★★★★ | **Title** — [2609.12715](https://arxiv.org/abs/2609.12715) · [📄](#20260914-2609.12715) (cs.LO) | 理由 |
_ROW_TITLE_RE = re.compile(r"\*\*(.+?)\*\*")
_ROW_ID_RE = re.compile(r"\[(\d{4}\.\d{4,5})\]\(https://arxiv\.org/abs/")
_ROW_CAT_RE = re.compile(r"\(([a-z-]+\.[A-Za-z]{2})\)\s*$")


def escape(value: Any) -> str:
    """Escape any value for safe interpolation into HTML text/attributes."""
    return html.escape("" if value is None else str(value), quote=True)


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
# HTML fragments
#
# Assembled with ``str.replace`` on explicit tokens rather than a template
# engine: the CSS/JS below is full of braces, and ``str.format``/f-strings
# would have to escape every one of them.
# ------------------------------------------------------------------

_STYLE = """
:root{
  --bg:#f8fafc; --panel:#ffffff; --ink:#0f172a; --muted:#64748b;
  --line:#e2e8f0; --accent:#2563eb; --star:#b45309; --expand:#0f766e;
  --chip:#f1f5f9;
}
html.dark{
  --bg:#0b1120; --panel:#111827; --ink:#e5e7eb; --muted:#94a3b8;
  --line:#1f2937; --accent:#60a5fa; --star:#fbbf24; --expand:#5eead4;
  --chip:#1f2937;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
  font:15px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans CJK SC","Microsoft YaHei",sans-serif}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
.wrap{max-width:1100px;margin:0 auto;padding:0 20px}
header.topbar{background:var(--panel);border-bottom:1px solid var(--line);position:sticky;top:0;z-index:10}
header.topbar h1{font-size:19px;margin:0;padding:14px 0 2px}
header.topbar .meta{color:var(--muted);font-size:13px;margin:0 0 10px}
.controls{display:flex;flex-wrap:wrap;gap:10px;align-items:center;padding-bottom:12px}
.controls input[type=search]{flex:1 1 220px;min-width:180px;padding:7px 10px;border:1px solid var(--line);
  border-radius:8px;background:var(--bg);color:var(--ink)}
.controls select,.controls button{padding:7px 10px;border:1px solid var(--line);border-radius:8px;
  background:var(--chip);color:var(--ink);cursor:pointer;font-size:13px}
.controls label{font-size:13px;color:var(--muted);display:flex;align-items:center;gap:5px}
h2{font-size:17px;margin:26px 0 10px;padding-bottom:6px;border-bottom:1px solid var(--line)}
h3{font-size:15px;margin:22px 0 8px;color:var(--muted)}
ol.recs{list-style:none;padding:0;margin:0;display:grid;gap:10px}
li.rec{background:var(--panel);border:1px solid var(--line);border-left:4px solid var(--accent);
  border-radius:10px;padding:12px 14px}
li.rec .stars{color:var(--star);letter-spacing:1px;margin-right:6px}
li.rec.expand{border-left-color:var(--expand)}
li.rec.expand .stars{color:var(--expand)}
li.rec .title{font-weight:600}
li.rec .cat{font-size:12px;color:var(--muted);border:1px solid var(--line);
  border-radius:999px;padding:1px 8px;margin-left:6px;white-space:nowrap}
li.rec .why{margin:6px 0 0;color:var(--ink);opacity:.9;font-size:14px}
li.rec .jump{font-size:12px;margin-left:8px}
article.paper{background:var(--panel);border:1px solid var(--line);border-radius:10px;
  padding:12px 14px;margin-bottom:10px}
article.paper h4{margin:0 0 4px;font-size:15px;font-weight:600}
.pmeta{font-size:12px;color:var(--muted);margin-bottom:6px}
.badges{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:6px}
.badge{font-size:12px;background:var(--chip);border-radius:999px;padding:2px 9px;color:var(--ink)}
.badge.star{background:rgba(180,83,9,.13);color:var(--star)}
.badge.expand{background:rgba(15,118,110,.13);color:var(--expand)}
.authors{font-size:13px;color:var(--muted);margin-bottom:6px}
details summary{cursor:pointer;font-size:13px;color:var(--accent)}
details p{margin:8px 0 0;font-size:14px;color:var(--ink);opacity:.92}
.actions{margin-top:8px;display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.actions a,.actions button{font-size:12px;padding:3px 9px;border:1px solid var(--line);
  border-radius:999px;background:var(--chip);color:var(--ink);cursor:pointer}
.empty{color:var(--muted);font-size:14px}
footer{padding:24px 0 40px;color:var(--muted);font-size:12px}
.note{background:var(--panel);border:1px dashed var(--line);border-radius:10px;
  padding:10px 14px;font-size:13px;color:var(--muted);margin:14px 0}
@media print{
  header.topbar{position:static} .controls{display:none}
  article.paper,li.rec{break-inside:avoid} details{display:block}
}
"""

_SCRIPT = """
(function () {
  var dark = localStorage.getItem('darkMode') === 'true';
  if (dark) document.documentElement.classList.add('dark');

  var toggle = document.getElementById('toggle-dark');
  if (toggle) {
    toggle.addEventListener('click', function () {
      dark = !dark;
      document.documentElement.classList.toggle('dark', dark);
      localStorage.setItem('darkMode', dark ? 'true' : 'false');
    });
  }

  var q = document.getElementById('q');
  var cat = document.getElementById('cat');
  var onlyHit = document.getElementById('only-hit');
  var counter = document.getElementById('shown');
  var papers = [].slice.call(document.querySelectorAll('article.paper'));
  var sections = [].slice.call(document.querySelectorAll('section.cat'));

  function apply() {
    var needle = (q && q.value || '').toLowerCase();
    var want = cat && cat.value || '';
    var hitOnly = !!(onlyHit && onlyHit.checked);
    var shown = 0;
    papers.forEach(function (el) {
      var ok = (!want || el.getAttribute('data-cat') === want)
        && (!hitOnly || el.getAttribute('data-hit') === '1')
        && (!needle || (el.getAttribute('data-text') || '').indexOf(needle) !== -1
            || el.textContent.toLowerCase().indexOf(needle) !== -1);
      el.style.display = ok ? '' : 'none';
      if (ok) shown++;
    });
    sections.forEach(function (sec) {
      var any = [].slice.call(sec.querySelectorAll('article.paper'))
        .some(function (el) { return el.style.display !== 'none'; });
      sec.style.display = any ? '' : 'none';
    });
    if (counter) counter.textContent = shown + ' / ' + papers.length;
  }

  if (q) q.addEventListener('input', apply);
  if (cat) cat.addEventListener('change', apply);
  if (onlyHit) onlyHit.addEventListener('change', apply);

  // 静态快照没有后端：按钮不 POST，只把等价的 CLI 命令复制到剪贴板。
  document.addEventListener('click', function (ev) {
    var btn = ev.target.closest ? ev.target.closest('[data-copy]') : null;
    if (!btn) return;
    var text = btn.getAttribute('data-copy');
    var done = function () {
      var old = btn.textContent;
      btn.textContent = '已复制';
      setTimeout(function () { btn.textContent = old; }, 1200);
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done, function () { window.prompt('复制这条命令:', text); });
    } else {
      window.prompt('复制这条命令:', text);
    }
  });
})();
"""

_SHELL = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>arXiv Digest <!--DAY--> — paper-glean</title>
<script>
  if (localStorage.getItem('darkMode') === 'true') {
    document.documentElement.classList.add('dark');
  }
</script>
<style><!--STYLE--></style>
</head>
<body>
<header class="topbar">
  <div class="wrap">
    <h1>arXiv Daily Digest <span style="color:var(--muted)"><!--DAY-FMT--></span></h1>
    <p class="meta"><!--META--></p>
    <div class="controls">
      <input id="q" type="search" placeholder="搜索标题 / 作者 / 摘要…">
      <select id="cat"><!--CAT-OPTIONS--></select>
      <label><input id="only-hit" type="checkbox"> 只看命中</label>
      <span class="meta">显示 <span id="shown"><!--TOTAL--> / <!--TOTAL--></span></span>
      <button id="toggle-dark">🌙 暗色</button>
      <button onclick="window.print()">🖨 打印 / 存 PDF</button>
    </div>
  </div>
</header>
<main class="wrap">
<!--BODY-->
</main>
<footer class="wrap">
  <p>由 paper-glean 生成于 <!--GENERATED-->。事实源：<code>data/<!--DAY-->.json</code> 与
  <code>arXiv-schedule.md</code>；本文件是派生产物（<code>exports/</code>，未纳入版本库）。
  打分请回到本地 Web 服务，或用上面复制的 CLI 命令——静态快照本身不回写画像。</p>
</footer>
<script><!--SCRIPT--></script>
</body>
</html>
"""


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
        f'<article class="paper" id="p-{pid}" data-cat="{escape(p.get("primary", ""))}" '
        f'data-hit="{1 if total else 0}" data-text="{escape(search_blob)}">'
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
        body.append(f'<section class="cat"><h3>{escape(cat)}（{len(ps)}）</h3>')
        body.extend(_paper_article(p) for p in ps)
        body.append("</section>")

    cat_options = ['<option value="">全部类别</option>'] + [
        f'<option value="{escape(cat)}">{escape(cat)}（{len(ps)}）</option>' for cat, ps in groups
    ]
    meta = (
        f"窗口(UTC): {escape(str(window[0])[:16].replace('T', ' '))} → "
        f"{escape(str(window[1])[:16].replace('T', ' '))} · 共 {len(papers)} 篇 · "
        f"★ 命中 {n_star} 篇 / 🧐 命中 {n_expand} 篇"
    )
    return (
        _SHELL.replace("<!--STYLE-->", _STYLE)
        .replace("<!--SCRIPT-->", _SCRIPT)
        .replace("<!--DAY-->", escape(day))
        .replace("<!--DAY-FMT-->", f"{day[:4]}-{day[4:6]}-{day[6:]}")
        .replace("<!--META-->", meta)
        .replace("<!--CAT-OPTIONS-->", "\n".join(cat_options))
        .replace("<!--TOTAL-->", str(len(papers)))
        .replace("<!--BODY-->", "\n".join(body))
        .replace("<!--GENERATED-->", datetime.now().strftime("%Y-%m-%d %H:%M"))
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


__all__ = [
    "build_html",
    "escape",
    "group_by_category",
    "latest_export",
    "parse_recommendations",
    "render_day",
]
