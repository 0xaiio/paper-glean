"""Push channels for newly detected work.

Channels (all best-effort — a failing channel never fails the run)
-----------------------------------------------------------------
``file``     Always on. Writes the unacknowledged "new" set to
             ``data/watch_new.json``; the Web UI badges these as NEW.
             (The human-readable ``WATCH-digest.md`` is written by
             :func:`glean.watch.run`, not here.)
``desktop``  Windows balloon toast via PowerShell. On by default on Windows,
             off with ``PAPER_GLEAN_DESKTOP=0``.
``webhook``  HTTP POST to ``PAPER_GLEAN_WEBHOOK_URL``. Off unless the variable
             is set. Payload shape selected with ``PAPER_GLEAN_WEBHOOK_FORMAT``
             (``generic`` | ``feishu`` | ``wecom``).

**Secrets never live in tracked files.** The webhook URL is a credential — it is
read from the environment only, so it can never be committed by accident.
"""

from __future__ import annotations

import json
import os
import platform
import subprocess
import urllib.request
from datetime import datetime, timezone
from typing import Any

from glean.config import WATCH_NEW

CHANNELS = ("file", "desktop", "webhook")

_KIND_LABEL = {
    "paper": "论文",
    "video": "视频",
    "report": "技术报告",
    "talk": "报告/演讲",
    "other": "其它",
}


def _summary(items: list[dict[str, Any]], day: str) -> str:
    by_person: dict[str, int] = {}
    for it in items:
        by_person[it.get("researcher", "?")] = by_person.get(it.get("researcher", "?"), 0) + 1
    detail = "、".join(f"{k} {v} 条" for k, v in by_person.items())
    return f"paper-glean 监控：{day} 发现 {len(items)} 条新作（{detail}）"


def _kind(item: dict[str, Any]) -> str:
    return _KIND_LABEL.get(item.get("kind", "other"), "其它")


# ------------------------------------------------------------------
# file — unacknowledged set for the Web UI
# ------------------------------------------------------------------

def load_new() -> list[dict[str, Any]]:
    """Unacknowledged new items (what the Web UI badges as NEW)."""
    if not WATCH_NEW.exists():
        return []
    try:
        data = json.loads(WATCH_NEW.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    return data.get("items", []) if isinstance(data, dict) else []


def _file_channel(items: list[dict[str, Any]], day: str) -> bool:
    existing = load_new()
    known = {(i.get("fingerprint"), i.get("key")) for i in existing}
    for it in items:
        marker = (it.get("fingerprint"), it.get("key"))
        if marker not in known:
            known.add(marker)
            existing.append(it)
    WATCH_NEW.parent.mkdir(parents=True, exist_ok=True)
    WATCH_NEW.write_text(
        json.dumps(
            {"updated": datetime.now(timezone.utc).isoformat(), "day": day, "items": existing},
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return True


def ack_all() -> int:
    """Mark every new item as read. Returns how many were cleared."""
    n = len(load_new())
    WATCH_NEW.parent.mkdir(parents=True, exist_ok=True)
    WATCH_NEW.write_text(
        json.dumps(
            {"updated": datetime.now(timezone.utc).isoformat(), "day": None, "items": []},
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return n


# ------------------------------------------------------------------
# desktop — Windows balloon toast
# ------------------------------------------------------------------

def _desktop_enabled() -> bool:
    return os.environ.get("PAPER_GLEAN_DESKTOP", "1").lower() not in ("0", "false", "no")


def _desktop_channel(items: list[dict[str, Any]], day: str) -> bool:
    if not _desktop_enabled() or platform.system() != "Windows":
        return False
    title = "paper-glean 新作提醒"
    text = _summary(items, day)
    if items:
        first = items[0]
        text += f"\n{first.get('researcher', '')}｜{_kind(first)}｜{first.get('title', '')[:60]}"
    # WinForms NotifyIcon: no extra module needed, degrades silently.
    ps = (
        "Add-Type -AssemblyName System.Windows.Forms;"
        "$n = New-Object System.Windows.Forms.NotifyIcon;"
        "$n.Icon = [System.Drawing.SystemIcons]::Information;"
        f"$n.BalloonTipTitle = '{title}';"
        f"$n.BalloonTipText = '{text}';"
        "$n.Visible = $true;"
        "$n.ShowBalloonTip(8000);"
        "Start-Sleep -Seconds 4;"
        "$n.Dispose()"
    )
    try:
        subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps],
            timeout=30,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        return True
    except Exception:
        return False


# ------------------------------------------------------------------
# webhook — generic / feishu / wecom
# ------------------------------------------------------------------

def _payload(items: list[dict[str, Any]], day: str) -> dict[str, Any]:
    fmt = os.environ.get("PAPER_GLEAN_WEBHOOK_FORMAT", "generic").lower()
    text = _summary(items, day)
    for it in items:
        text += f"\n· [{_kind(it)}] {it.get('researcher', '')} — {it.get('title', '')}"
        if it.get("url"):
            text += f"\n  {it['url']}"
    if fmt == "feishu":
        return {"msg_type": "text", "content": {"text": text}}
    if fmt == "wecom":
        return {"msgtype": "text", "text": {"content": text}}
    return {
        "text": text,
        "day": day,
        "count": len(items),
        "items": [
            {
                "researcher": it.get("researcher"),
                "title": it.get("title"),
                "kind": it.get("kind"),
                "year": it.get("year"),
                "venue": it.get("venue"),
                "url": it.get("url"),
                "source": it.get("source"),
            }
            for it in items
        ],
    }


def _webhook_channel(items: list[dict[str, Any]], day: str) -> bool:
    url = os.environ.get("PAPER_GLEAN_WEBHOOK_URL", "").strip()
    if not url:
        return False
    body = json.dumps(_payload(items, day), ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json", "User-Agent": "paper-glean/0.1.0"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return 200 <= int(getattr(resp, "status", 200)) < 300
    except Exception:
        return False


# ------------------------------------------------------------------
# entry point
# ------------------------------------------------------------------

def push(items: list[dict[str, Any]], day: str | None = None) -> list[str]:
    """Deliver ``items`` through every enabled channel. Returns names that ran."""
    if not items:
        return []
    day = day or datetime.now().strftime("%Y-%m-%d")
    done: list[str] = []
    if _file_channel(items, day):
        done.append("file")
    if _desktop_channel(items, day):
        done.append("desktop")
    if _webhook_channel(items, day):
        done.append("webhook")
    return done


def enabled_channels() -> dict[str, bool]:
    """Report which channels would fire (used by ``watch push-test``)."""
    return {
        "file": True,
        "desktop": _desktop_enabled() and platform.system() == "Windows",
        "webhook": bool(os.environ.get("PAPER_GLEAN_WEBHOOK_URL", "").strip()),
    }
