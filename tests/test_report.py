"""Tests for glean/report.py — the standalone HTML snapshot."""

from __future__ import annotations

import json

import pytest

from glean import core, report

DAY = "20260914"

PAPERS = [
    {
        "id": "2609.12715",
        "version": "v1",
        "title": "Supermartingale Certificates <script>alert(1)</script>",
        "authors": ["A. Author", "B. Author"],
        "abstract": "We study formal verification of parametric MDPs.",
        "primary": "cs.LO",
        "categories": ["cs.LO", "cs.SE"],
        "published": "2026-09-14T00:00:00+00:00",
        "abs_url": "https://arxiv.org/abs/2609.12715",
        "pdf_url": "https://arxiv.org/pdf/2609.12715",
        "hits_star": ["formal verification"],
        "hits_expand": [],
        "score_star": 3,
        "score_expand": 0,
    },
    {
        "id": "2609.12239",
        "version": "v1",
        "title": "Specifying Paxos",
        "authors": ["C. Author"],
        "abstract": "Executable specs for consensus.",
        "primary": "cs.DC",
        "categories": ["cs.DC"],
        "published": "2026-09-14T00:00:00+00:00",
        "abs_url": "https://arxiv.org/abs/2609.12239",
        "pdf_url": "https://arxiv.org/pdf/2609.12239",
        "hits_star": ["consensus", "Paxos"],
        "hits_expand": [],
        "score_star": 6,
        "score_expand": 0,
    },
]

FILLED_SECTION = f"""<!-- BEGIN {DAY} -->
## {DAY}

### 📌 重点关注(基于研究兴趣, agent 填写)

| 推荐 | 论文 | 理由 |
|------|------|------|
| ★★★★★ | **Specifying Paxos** — [2609.12239](https://arxiv.org/abs/2609.12239) · [📄](#{DAY}-2609.12239) (cs.DC) | 命中 `consensus` 与 `Paxos` 两条关键词 |

### 🧐 视野扩展(agent 填写)

| 推荐 | 论文 | 理由 |
|------|------|------|
| 🧐🧐🧐 | **Supermartingale** — [2609.12715](https://arxiv.org/abs/2609.12715) · [📄](#{DAY}-2609.12715) (cs.LO) | 机器验证的下界 |

### 分类清单
<!-- END {DAY} -->
"""

EMPTY_SECTION = f"""<!-- BEGIN {DAY} -->
## {DAY}

### 📌 重点关注(基于研究兴趣, agent 填写)

_待 agent 分析填写_

### 🧐 视野扩展(agent 填写)

_待 agent 分析填写_
<!-- END {DAY} -->
"""


@pytest.fixture
def isolated(tmp_path, monkeypatch):
    """data/ + arXiv-schedule.md + exports/ redirected into tmp_path."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    (data_dir / f"{DAY}.json").write_text(
        json.dumps(
            {
                "day": DAY,
                "window_utc": ["2026-09-14T00:00:00+00:00", "2026-09-15T00:00:00+00:00"],
                "papers": PAPERS,
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    digest = tmp_path / "arXiv-schedule.md"
    digest.write_text(EMPTY_SECTION, encoding="utf-8")
    exports = tmp_path / "exports"

    monkeypatch.setattr(core, "DATA_DIR", data_dir)
    monkeypatch.setattr(report, "DIGEST_MD", digest)
    monkeypatch.setattr(report, "EXPORT_DIR", exports)
    return {"data": data_dir, "digest": digest, "exports": exports}


def test_build_html_lists_every_paper(isolated):
    html = report.build_html(DAY)

    assert html is not None
    for p in PAPERS:
        assert p["id"] in html
        assert f'id="p-{p["id"]}"' in html
        assert p["abs_url"] in html


def test_snapshot_is_self_contained(isolated):
    """A file:// snapshot must not depend on a CDN or a running server."""
    html = report.build_html(DAY)

    assert "<script src" not in html
    assert "<link rel=\"stylesheet\"" not in html
    assert "cdn." not in html
    assert "http://127.0.0.1" not in html


def test_titles_are_escaped(isolated):
    html = report.build_html(DAY)

    assert "<script>alert(1)</script>" not in html
    assert "&lt;script&gt;" in html


def test_recommendations_come_from_the_digest(isolated):
    isolated["digest"].write_text(FILLED_SECTION, encoding="utf-8")

    recs = report.parse_recommendations(DAY)

    assert [r["id"] for r in recs["star"]] == ["2609.12239"]
    assert recs["star"][0]["count"] == 5
    assert recs["star"][0]["category"] == "cs.DC"
    assert "consensus" in recs["star"][0]["reason"]
    assert [r["id"] for r in recs["expand"]] == ["2609.12715"]


def test_filled_recommendations_render_verbatim(isolated):
    isolated["digest"].write_text(FILLED_SECTION, encoding="utf-8")

    html = report.build_html(DAY)

    assert "命中 consensus 与 Paxos 两条关键词" in html
    assert "占位符" not in html


def test_placeholder_block_falls_back_to_score_ranking(isolated):
    html = report.build_html(DAY)

    assert "占位符" in html
    # 权重和最高的排在前面
    assert html.index("2609.12239") < html.index("2609.12715")


def test_render_day_writes_into_exports(isolated):
    path = report.render_day(DAY)

    assert path is not None
    assert path.exists()
    assert path.name == f"arxiv-digest-{DAY}.html"
    assert report.latest_export() == path


def test_render_day_without_data_is_none(isolated):
    assert report.render_day("19990101") is None


def test_group_by_category_orders_like_the_digest():
    groups = report.group_by_category(PAPERS)

    assert [cat for cat, _ in groups] == ["cs.DC", "cs.LO"]
    assert [p["id"] for p in groups[1][1]] == ["2609.12715"]
