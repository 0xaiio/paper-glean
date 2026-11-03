"""One-off: normalize the 🧐 rating column to 🧐 glyphs inside one digest day block.

glean/report.py::_parse_row matches rows by the leading glyph of the rating cell
(symbol "★" for the 重点关注 block, "🧐" for the 视野扩展 block). Rows in the 🧐
block that carry "★" glyphs are silently dropped when rendering the HTML snapshot.
"""

import sys

BEGIN = "<!-- BEGIN %s -->"
END = "<!-- END %s -->"
MAP = [
    ("| ★★★★★ ", "| 🧐🧐🧐🧐🧐 "),
    ("| ★★★★☆ ", "| 🧐🧐🧐🧐 "),
    ("| ★★★☆☆ ", "| 🧐🧐🧐 "),
]


def main(day: str) -> int:
    path = "arXiv-schedule.md"
    text = open(path, encoding="utf-8").read()
    b, e = BEGIN % day, END % day
    if b not in text or e not in text:
        print("[ERR] day section not found:", day)
        return 1
    i = text.index(b)
    j = text.index(e, i)
    sec = text[i:j]

    k = sec.find("### 🧐")
    if k == -1:
        print("[ERR] no 🧐 heading in", day)
        return 1
    head, block = sec[:k], sec[k:]

    fixed, n = block, 0
    for old, new in MAP:
        c = fixed.count("\n" + old)
        n += c
        fixed = fixed.replace("\n" + old, "\n" + new)

    out = text[:i] + head + fixed + text[j:]
    if out == text:
        print("[OK] no change")
        return 0
    open(path, "w", encoding="utf-8").write(out)
    print("[OK] replaced %d 🧐 rating cells in %s" % (n, day))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
