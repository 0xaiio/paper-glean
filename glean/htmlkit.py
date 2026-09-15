"""Shared building blocks for the standalone HTML snapshots.

Why a separate module
---------------------
Two renderers write browser-openable snapshots: :mod:`glean.report` for the
arXiv daily digest, and the monitor renderer for the researcher / venue
digests. Both must honour the *same* contract, and that contract has four parts
that are easy to break one renderer at a time:

1. **Stdlib only.** ``dependencies = []`` in ``pyproject.toml`` and Jinja2
   lives in the ``web`` extra, so importing it here would break ``fetch`` /
   ``daily`` for a CLI-only install. The document is assembled by hand, with
   ``str.replace`` on explicit tokens — not ``str.format`` / f-strings, because
   the CSS below is full of braces.
2. **No CDN.** The web UI pulls Tailwind / htmx / Alpine from the network. A
   snapshot must stay readable offline and inside ``file://``, so the
   stylesheet and the behaviour are inlined.
3. **Light by default.** Dark is opt-in via ``localStorage.darkMode ===
   'true'`` — never ``!== 'false'`` (an absent key would then land in the truthy
   branch). See ``tests/test_web.py::test_default_theme_is_light`` for the
   regression this encodes, and ``tests/test_report.py`` for the snapshot twin.
4. **Readable without JavaScript.** Filtering / collapsing are progressive
   enhancements; the full content is static markup.

Everything here is presentation-only: no knowledge of papers, researchers or
venues. Renderers hand in already-escaped fragments; :func:`page` only glues
them together.

Layout of a snapshot
--------------------
``page()`` produces a header (title / meta line / control strip), a body and a
footer. The behaviour script is driven by **data attributes**, not by CSS
classes, so a renderer is free to use its own semantic markup:

``[data-item]``   one content card; optional ``data-cat``, ``data-flag``,
                  ``data-text`` (lower-cased search blob)
``[data-group]``  a section that wraps items and hides when all of them do
"""

from __future__ import annotations

import html
from typing import Any

# ------------------------------------------------------------------
# CSS — shared by every snapshot
# ------------------------------------------------------------------

STYLE = """
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
.badge.warn{background:rgba(180,83,9,.13);color:var(--star)}
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
/* run report block — answers "did the scan actually work?" (see monitor.py) */
table.run{background:var(--panel);border:1px solid var(--line);border-radius:10px;border-collapse:separate;
  border-spacing:0;width:100%;font-size:13px}
table.run th{text-align:left;color:var(--muted);font-weight:500;padding:7px 12px;width:9em;
  border-bottom:1px solid var(--line);vertical-align:top}
table.run td{padding:7px 12px;border-bottom:1px solid var(--line)}
table.run tr:last-child th,table.run tr:last-child td{border-bottom:none}
.err{color:var(--star);font-family:ui-monospace,Consolas,monospace;font-size:12px}
@media print{
  header.topbar{position:static} .controls{display:none}
  article.paper,li.rec{break-inside:avoid} details{display:block}
}
"""

# ------------------------------------------------------------------
# JS — dark-mode default, live filtering, copy-to-clipboard
# ------------------------------------------------------------------

SCRIPT = """
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
  var flagOnly = document.getElementById('only-flag');
  var counter = document.getElementById('shown');
  var items = [].slice.call(document.querySelectorAll('[data-item]'));
  var groups = [].slice.call(document.querySelectorAll('[data-group]'));

  function apply() {
    var needle = (q && q.value || '').toLowerCase();
    var want = cat && cat.value || '';
    var flagged = !!(flagOnly && flagOnly.checked);
    var shown = 0;
    items.forEach(function (el) {
      var ok = (!want || el.getAttribute('data-cat') === want)
        && (!flagged || el.getAttribute('data-flag') === '1')
        && (!needle || (el.getAttribute('data-text') || '').indexOf(needle) !== -1
            || el.textContent.toLowerCase().indexOf(needle) !== -1);
      el.style.display = ok ? '' : 'none';
      if (ok) shown++;
    });
    groups.forEach(function (sec) {
      var any = [].slice.call(sec.querySelectorAll('[data-item]'))
        .some(function (el) { return el.style.display !== 'none'; });
      sec.style.display = any ? '' : 'none';
    });
    if (counter) counter.textContent = shown + ' / ' + items.length;
  }

  if (q) q.addEventListener('input', apply);
  if (cat) cat.addEventListener('change', apply);
  if (flagOnly) flagOnly.addEventListener('change', apply);

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

# ------------------------------------------------------------------
# Document shell
# ------------------------------------------------------------------

_DOC = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><!--TITLE--> — paper-glean</title>
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
    <h1><!--TITLE--></h1>
    <p class="meta"><!--META--></p>
    <div class="controls"><!--CONTROLS--></div>
  </div>
</header>
<main class="wrap">
<!--BODY-->
</main>
<footer class="wrap">
  <!--FOOTER-->
</footer>
<script><!--SCRIPT--></script>
</body>
</html>
"""

# Standard control strip: live search + group filter + flag filter + dark / print.
_CONTROLS = """<input id="q" type="search" placeholder="<!--PLACEHOLDER-->">
      <select id="cat"><!--CAT-OPTIONS--></select>
      <label><input id="only-flag" type="checkbox"> <!--FLAG-LABEL--></label>
      <span class="meta">显示 <span id="shown"><!--TOTAL--> / <!--TOTAL--></span></span>
      <button id="toggle-dark">🌙 暗色</button>
      <button onclick="window.print()">🖨 打印 / 存 PDF</button>"""


def escape(value: Any) -> str:
    """Escape any value for safe interpolation into HTML text/attributes."""
    return html.escape("" if value is None else str(value), quote=True)


def controls(
    *,
    placeholder: str,
    cat_options: list[str],
    flag_label: str,
    total: int,
) -> str:
    """Render the standard control strip (search / filter / dark / print)."""
    return (
        _CONTROLS.replace("<!--PLACEHOLDER-->", escape(placeholder))
        .replace("<!--CAT-OPTIONS-->", "\n".join(cat_options))
        .replace("<!--FLAG-LABEL-->", escape(flag_label))
        .replace("<!--TOTAL-->", str(total))
    )


def page(
    *,
    title: str,
    meta: str,
    body: str,
    footer: str,
    controls_html: str = "",
) -> str:
    """Assemble a self-contained snapshot.

    ``title`` and ``meta`` are escaped here. ``body``, ``footer`` and
    ``controls_html`` are *trusted* fragments: they carry markup (``<code>``,
    links, tables), so each renderer escapes its own interpolated values —
    which it must, since those values come from fetched pages.
    """
    return (
        _DOC.replace("<!--STYLE-->", STYLE)
        .replace("<!--SCRIPT-->", SCRIPT)
        .replace("<!--TITLE-->", escape(title))
        .replace("<!--META-->", escape(meta))
        .replace("<!--CONTROLS-->", controls_html)
        .replace("<!--BODY-->", body)
        .replace("<!--FOOTER-->", footer)
    )


__all__ = ["SCRIPT", "STYLE", "controls", "escape", "page"]
