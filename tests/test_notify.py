"""Tests for :mod:`glean.notify` — the four push channels.

Nothing here opens a socket or pops a toast: paths go to ``tmp_path`` and the
desktop/webhook transports are either disabled or monkeypatched.
"""

from __future__ import annotations

import json

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
    monkeypatch.setenv("PAPER_GLEAN_DESKTOP", "0")
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
    assert "2 条新作" in text
    assert "魏恒峰 Hengfeng Wei 1 条" in text
    assert "Alexey Gotsman 1 条" in text


# ------------------------------------------------------------------
# desktop
# ------------------------------------------------------------------

def test_desktop_disabled_by_env(isolated):
    assert notify._desktop_enabled() is False
    assert notify._desktop_channel(ITEMS, "2026-09-14") is False


def test_desktop_skipped_off_windows(isolated, monkeypatch):
    monkeypatch.setenv("PAPER_GLEAN_DESKTOP", "1")
    monkeypatch.setattr(notify.platform, "system", lambda: "Linux")
    assert notify._desktop_channel(ITEMS, "2026-09-14") is False


def test_desktop_shells_out_on_windows(isolated, monkeypatch):
    monkeypatch.setenv("PAPER_GLEAN_DESKTOP", "1")
    monkeypatch.setattr(notify.platform, "system", lambda: "Windows")
    calls = {}

    def fake_run(cmd, **kw):
        calls["cmd"] = cmd
        return None

    monkeypatch.setattr(notify.subprocess, "run", fake_run)
    assert notify._desktop_channel(ITEMS, "2026-09-14") is True
    assert "powershell" in calls["cmd"][0].lower()


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
    states = notify.enabled_channels()
    assert states["file"] is True
    assert states["webhook"] is False
    assert states["desktop"] is False  # PAPER_GLEAN_DESKTOP=0 in fixture

    monkeypatch.setenv("PAPER_GLEAN_WEBHOOK_URL", "https://example.invalid/hook")
    assert notify.enabled_channels()["webhook"] is True
