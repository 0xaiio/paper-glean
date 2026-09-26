"""Tests for :mod:`glean.notify` — the push channels.

Nothing here opens a socket or pops a window: paths go to ``tmp_path`` and the
webhook transport is either disabled or monkeypatched. The display surface is
the HTML page, so there is deliberately no pop-up channel left to test.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from glean import notify

ITEMS = [
    {
        "title": "VeriStrong",
        "url": "https://x/a.pdf",
        "kind": "paper",
        "year": 2026,
        "researcher": "魏恒峰 Hengfeng Wei",
        "source": "homepage",
        "fingerprint": "aaa",
    },
    {
        "title": "Talk at Bilibili",
        "url": "https://www.bilibili.com/video/BV1",
        "kind": "video",
        "researcher": "Alexey Gotsman",
        "source": "homepage",
        "fingerprint": "bbb",
    },
]


@pytest.fixture
def isolated(tmp_path, monkeypatch):
    monkeypatch.setattr(notify, "WATCH_NEW", tmp_path / "watch_new.json")
    monkeypatch.delenv("PAPER_GLEAN_WEBHOOK_URL", raising=False)
    return tmp_path


# ------------------------------------------------------------------
# file channel (the NEW-badge backing store)
# ------------------------------------------------------------------

def test_file_channel_writes_and_dedups(isolated):
    assert notify._file_channel(ITEMS, "2026-09-14") is True
    assert len(notify.load_new()) == 2

    # pushing the same fingerprints again must not duplicate
    notify._file_channel(ITEMS, "2026-09-14")
    assert len(notify.load_new()) == 2

    third = [dict(ITEMS[0], title="Another", fingerprint="ccc")]
    notify._file_channel(third, "2026-09-14")
    assert len(notify.load_new()) == 3


def test_load_new_tolerates_missing_and_corrupt(isolated):
    assert notify.load_new() == []
    notify.WATCH_NEW.write_text("{not json", encoding="utf-8")
    assert notify.load_new() == []


def test_ack_all_clears(isolated):
    notify._file_channel(ITEMS, "2026-09-14")
    assert notify.ack_all() == 2
    assert notify.load_new() == []
    assert notify.ack_all() == 0


def test_summary_groups_by_researcher():
    text = notify._summary(ITEMS, "2026-09-14")
    assert "2 条更新" in text
    assert "魏恒峰 Hengfeng Wei 1 条" in text
    assert "Alexey Gotsman 1 条" in text


def test_summary_falls_back_to_venue_and_labels_namespace():
    """CCF items carry `venue`, not `researcher`, and say which monitor fired."""
    items = [{"venue": "SIGMOD", "title": "SIGMOD 2027 CFP", "kind": "cfp"}]
    text = notify._summary(items, "2026-09-14", "ccf")
    assert "CCF 监控" in text
    assert "SIGMOD 1 条" in text


def test_namespaces_keep_separate_unread_sets(isolated, tmp_path, monkeypatch):
    monkeypatch.setattr(notify, "CCF_NEW", tmp_path / "ccf_new.json")
    notify._file_channel(ITEMS, "2026-09-14", "ccf")
    assert len(notify.load_new("ccf")) == 2
    assert notify.load_new("watch") == []
    assert notify.ack_all("ccf") == 2
    assert notify.load_new("watch") == []


def test_unknown_namespace_is_rejected():
    with pytest.raises(ValueError):
        notify.load_new("nope")


# ------------------------------------------------------------------
# no pop-up channel (the display surface is HTML)
# ------------------------------------------------------------------

def test_notify_has_no_shell_out_surface():
    """No pop-up channel may come back.

    The removed desktop channel worked by shelling out to PowerShell and asking
    WinForms for a balloon tip. Checking the source (not just behaviour) makes
    that reintroduction a test failure instead of something to notice by hand.
    """
    src = Path(notify.__file__).read_text(encoding="utf-8")
    for banned in ("subprocess", "platform.system", "BalloonTip", "NotifyIcon"):
        assert banned not in src, f"{banned!r} would bring a pop-up channel back"


def test_push_reaches_only_the_page_channels(isolated, monkeypatch):
    """A real push writes the page's unread set and nothing else."""
    monkeypatch.setenv("PAPER_GLEAN_WEBHOOK_URL", "")  # webhook stays opt-in
    assert notify.push(ITEMS, "2026-09-14") == ["file"]
    assert len(notify.load_new()) == 2


# ------------------------------------------------------------------
# webhook
# ------------------------------------------------------------------

def test_webhook_off_without_url(isolated):
    assert notify._webhook_channel(ITEMS, "2026-09-14") is False


def test_webhook_payload_shapes(isolated, monkeypatch):
    monkeypatch.setenv("PAPER_GLEAN_WEBHOOK_FORMAT", "feishu")
    p = notify._payload(ITEMS, "2026-09-14")
    assert p["msg_type"] == "text" and "VeriStrong" in p["content"]["text"]

    monkeypatch.setenv("PAPER_GLEAN_WEBHOOK_FORMAT", "wecom")
    p = notify._payload(ITEMS, "2026-09-14")
    assert p["msgtype"] == "text" and "VeriStrong" in p["text"]["content"]

    monkeypatch.setenv("PAPER_GLEAN_WEBHOOK_FORMAT", "generic")
    p = notify._payload(ITEMS, "2026-09-14")
    assert p["count"] == 2 and len(p["items"]) == 2
    assert p["items"][0]["kind"] == "paper"


def test_webhook_posts_when_configured(isolated, monkeypatch):
    monkeypatch.setenv("PAPER_GLEAN_WEBHOOK_URL", "https://example.invalid/hook")
    captured = {}

    class _Resp:
        status = 200

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

    def fake_urlopen(req, timeout=None):
        captured["url"] = req.full_url
        captured["body"] = json.loads(req.data.decode("utf-8"))
        return _Resp()

    monkeypatch.setattr(notify.urllib.request, "urlopen", fake_urlopen)
    assert notify._webhook_channel(ITEMS, "2026-09-14") is True
    assert captured["url"] == "https://example.invalid/hook"
    assert captured["body"]["count"] == 2


def test_webhook_failure_is_swallowed(isolated, monkeypatch):
    monkeypatch.setenv("PAPER_GLEAN_WEBHOOK_URL", "https://example.invalid/hook")

    def boom(req, timeout=None):
        raise OSError("network down")

    monkeypatch.setattr(notify.urllib.request, "urlopen", boom)
    assert notify._webhook_channel(ITEMS, "2026-09-14") is False


# ------------------------------------------------------------------
# orchestration
# ------------------------------------------------------------------

def test_push_runs_enabled_channels_only(isolated):
    done = notify.push(ITEMS, day="2026-09-14")
    assert done == ["file"]  # desktop off, no webhook url


def test_push_no_items_is_noop(isolated):
    assert notify.push([], day="2026-09-14") == []
    assert notify.load_new() == []


def test_enabled_channels_report(isolated, monkeypatch):
    """Exactly two channels: `file` (feeds the HTML pages) and `webhook` (opt-in).

    Asserted as an exact dict so that re-adding a pop-up channel — the removed
    PowerShell balloon was one — has to break a test rather than slip back in.
    """
    states = notify.enabled_channels()
    assert states == {"file": True, "webhook": False}

    monkeypatch.setenv("PAPER_GLEAN_WEBHOOK_URL", "https://example.invalid/hook")
    assert notify.enabled_channels() == {"file": True, "webhook": True}
