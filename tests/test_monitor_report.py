"""Tests for the monitor HTML snapshots (``watch`` / ``ccf`` digests)."""

from __future__ import annotations

import pytest

from glean import report
from glean.ccf import KIND_ICONS as CCF_ICONS
from glean.ccf import KIND_LABELS as CCF_LABELS
from glean.watch import KIND_ICONS as WATCH_ICONS
from glean.watch import KIND_LABELS as WATCH_LABELS

DAY = "2026-09-15"

WATCH_VIEW = report.MonitorView(
    namespace="watch",
    title="学者监控 · 新作推送",
    noun="新作",
    digest_name="WATCH-digest.md",
    kind_labels=WATCH_LABELS,
    kind_icons=WATCH_ICONS,
)

CCF_VIEW = report.MonitorView(
    namespace="ccf",
    title="CCF-A 会议 / 期刊监控",
    noun="更新",
    digest_name="CCF-digest.md",
    kind_labels=CCF_LABELS,
    kind_icons=CCF_ICONS,
)

GROUPED = {
    "魏恒峰 Hengfeng Wei": [
        {
            "title": "Executable Specification <script>alert(1)</script>",
            "kind": "paper",
            "url": "https://arxiv.org/abs/2301.07313",
            "year": 2023,
            "source": "homepage",
            "fingerprint": "aaa",
        },
        {"title": "Video at bilibili", "kind": "video", "url": "", "source": "homepage"},
    ],
    "Alexey Gotsman": [
        {
            "title": "Sparse CFP",
            "kind": "cfp",
            "url": "https://example.org/cfp",
            "deadline": "2026-10-14 23:59:59",
            "venue": "PODS",
            "source": "homepage",
            "confidence": 0.4,
        }
    ],
}

RUN = {
    "run_id": "20260915T010000Z",
    "day": DAY,
    "new_items": [{"title": "x"}],
    "baselined": ["Hagit Attiya（0 条基线）"],
    "skipped": ["Shafi Goldwasser"],
    "errors": [],
    "pushed_to": ["file", "desktop"],
}


@pytest.fixture
def isolated(tmp_path, monkeypatch):
    """``exports/`` redirected into tmp_path."""
    exports = tmp_path / "exports"
    monkeypatch.setattr(report, "EXPORT_DIR", exports)
    return exports


def test_snapshot_is_self_contained(isolated):
    """A file:// snapshot must not depend on a CDN or a running server."""
    html = report.build_monitor_html(WATCH_VIEW, DAY, GROUPED, run=RUN)

    assert "<script src" not in html
    assert "<link rel=\"stylesheet\"" not in html
    assert "cdn." not in html
    assert "http://127.0.0.1" not in html


def test_dark_mode_is_opt_in(isolated):
    """Dark stays opt-in — the bug is ``!== 'false'``, which flips with no key."""
    html = report.build_monitor_html(WATCH_VIEW, DAY, GROUPED, run=RUN)

    assert "localStorage.getItem('darkMode') === 'true'" in html
    assert "darkMode') !== 'false'" not in html


def test_titles_are_escaped(isolated):
    html = report.build_monitor_html(WATCH_VIEW, DAY, GROUPED, run=RUN)

    assert "<script>alert(1)</script>" not in html
    assert "&lt;script&gt;" in html


def test_subjects_and_items_are_listed(isolated):
    html = report.build_monitor_html(WATCH_VIEW, DAY, GROUPED, run=RUN)

    for subject in GROUPED:
        assert subject in html
    assert "https://arxiv.org/abs/2301.07313" in html
    assert "论文" in html and "视频" in html
    assert 'data-group' in html and 'data-item' in html


def test_low_confidence_item_is_flagged(isolated):
    html = report.build_monitor_html(CCF_VIEW, DAY, GROUPED, run=RUN)

    assert "低置信" in html
    assert 'data-flag="1"' in html
    assert 'data-flag="0"' in html  # 只有低置信条目被打标，其余不受影响


def test_run_report_states_the_evidence(isolated):
    html = report.build_monitor_html(WATCH_VIEW, DAY, GROUPED, run=RUN)

    assert "本次运行" in html
    assert "20260915T010000Z" in html
    assert "Hagit Attiya" in html
    assert "Shafi Goldwasser" in html
    assert "file, desktop" in html


def test_zero_items_with_errors_reports_them(isolated):
    html = report.build_monitor_html(
        WATCH_VIEW, DAY, {}, run={"run_id": "r", "errors": ["Hagit Attiya: URLError: timed out"]}
    )

    assert "报了 1 个错误" in html
    assert "URLError" in html


def test_blind_subject_is_flagged_not_called_healthy(isolated):
    """0 指纹（源不可达）必须报出来——抓取是 fail-soft 的，errors 也可能是空的。"""
    html = report.build_monitor_html(
        WATCH_VIEW,
        DAY,
        {},
        run={"run_id": "r", "collected": {"魏恒峰": 0, "Alexey Gotsman": 0, "Hagit Attiya": 0}},
    )

    assert "一条内容都没取到" in html
    assert "源不可达" in html
    assert "盲区" in html
    # 关键：不能退化成「本次是首次运行」这种听起来正常的说法
    assert "首次运行" not in html


def test_partly_blind_run_still_lists_what_was_found(isolated):
    """部分失聪时：既要报盲区，也要照常列出真正抓到的新内容。"""
    html = report.build_monitor_html(
        WATCH_VIEW,
        DAY,
        {"魏恒峰 Hengfeng Wei": GROUPED["魏恒峰 Hengfeng Wei"]},
        run={"run_id": "r", "collected": {"魏恒峰 Hengfeng Wei": 2, "Hagit Attiya": 0}},
    )

    assert "一条内容都没取到" in html
    assert "Hagit Attiya" in html
    assert "Executable Specification" in html


def test_zero_items_without_errors_is_honest(isolated):
    html = report.build_monitor_html(WATCH_VIEW, DAY, {}, run={"run_id": "r", "errors": []})

    assert "本次运行没有发现新作" in html
    assert "静默失败" in html


def test_scoped_run_says_so(isolated):
    """``--only X`` renders a page that admits it is a partial scan."""
    html = report.build_monitor_html(WATCH_VIEW, DAY, GROUPED, run=RUN, scope="魏恒峰")

    assert "单条调试" in html
    assert "魏恒峰" in html


def test_render_monitor_day_writes_into_exports(isolated):
    path = report.render_monitor_day(WATCH_VIEW, DAY, GROUPED, run=RUN)

    assert path.exists()
    assert path.name == f"watch-digest-{DAY}.html"
    assert report.latest_monitor_export("watch") == path


def test_empty_day_still_produces_a_snapshot(isolated):
    """零新增也出页面：空转的证据本身就是交付物。"""
    path = report.render_monitor_day(CCF_VIEW, DAY, {}, run={"run_id": "r"})

    assert path.exists()
    assert "本次运行" in path.read_text(encoding="utf-8")


def test_monitor_and_arxiv_snapshots_do_not_collide(isolated):
    watch = report.render_monitor_day(WATCH_VIEW, DAY, GROUPED, run=RUN)
    ccf = report.render_monitor_day(CCF_VIEW, DAY, GROUPED, run=RUN)

    assert watch != ccf
    assert {watch.name, ccf.name} == {f"watch-digest-{DAY}.html", f"ccf-digest-{DAY}.html"}
    assert report.latest_monitor_export("watch") == watch
    assert report.latest_monitor_export("ccf") == ccf
