"""Push channels for newly detected work.

Display contract: the result is always an HTML page
---------------------------------------------------
Nothing here (and nothing in the scheduled pipeline) pops up a window or a
system notification. A run leaves its result behind as HTML, and the scheduled
task is what makes those pages exist:

* ``exports/<namespace>-digest-<YYYYMMDD>.html`` — a self-contained snapshot
  written on every run (see :mod:`glean.report`); opens straight from the file
  system, no server and no network needed. **零新增也会出页面**，因为「跑过且
  什么都没发现」本身就是要留下的证据。
* the local web app — ``/watch`` / ``/ccf`` / ``/digest``. The scheduled task
  keeps it online (``glean.serve.ensure``), and this module's ``file`` channel
  is what feeds its NEW badges.

So "did anything happen" is answered by *reading a page*, never by a toast that
is gone the moment you look away. The ``PAPER_GLEAN_DESKTOP`` environment
variable and the PowerShell balloon channel were removed for exactly this
reason (they were the only non-HTML surface).

Channels (all best-effort — a failing channel never fails the run)
-----------------------------------------------------------------
``file``     Always on. Writes the unacknowledged "new" set to
             ``data/watch_new.json``; the Web UI badges these as NEW.
             (The human-readable ``WATCH-digest.md`` is written by
             :func:`glean.watch.run`, not here.)
``webhook``  HTTP POST to ``PAPER_GLEAN_WEBHOOK_URL``. Off unless the variable
             is set — the only channel that leaves the machine, and opt-in.
             Payload shape selected with ``PAPER_GLEAN_WEBHOOK_FORMAT``
             (``generic`` | ``feishu`` | ``wecom``).

**Secrets never live in tracked files.** The webhook URL is a credential — it is
read from the environment only, so it can never be committed by accident.

Namespaces
----------
Two independent monitors share these channels, each with its own
"unacknowledged" set so that *mark read* on one never clears the other:

``watch``  researcher monitoring -> ``data/watch_new.json``
``ccf``    CCF-A venue monitoring -> ``data/ccf_new.json``
"""

from __future__ import annotations

import json
import os
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from glean.config import CCF_NEW, WATCH_NEW
from glean.kinds import KIND_LABELS as _KIND_LABEL

# A push target is a *namespace*: researchers and CCF venues keep separate
# unacknowledged sets so that "mark read" on one page never clears the other.
_NEW_PATHS = {"watch": "WATCH_NEW", "ccf": "CCF_NEW"}
NS_LABEL = {"watch": "监控", "ccf": "CCF 监控"}


def _new_path(namespace: str) -> Path:
    """Resolve the unacknowledged-set file for ``namespace`` (late-bound so
    tests can ``monkeypatch`` the module global)."""
    try:
        return globals()[_NEW_PATHS[namespace]]
    except KeyError:
        raise ValueError(f"unknown notify namespace: {namespace!r}") from None


def _subject(item: dict[str, Any]) -> str:
    """Who/ what an item is about: a researcher, or a venue."""
    return item.get("researcher") or item.get("venue") or "?"


def _summary(items: list[dict[str, Any]], day: str, namespace: str = "watch") -> str:
    by_person: dict[str, int] = {}
    for it in items:
        key = _subject(it)
        by_person[key] = by_person.get(key, 0) + 1
    detail = "、".join(f"{k} {v} 条" for k, v in by_person.items())
    return f"paper-glean {NS_LABEL.get(namespace, namespace)}：{day} 发现 {len(items)} 条更新（{detail}）"


def _kind(item: dict[str, Any]) -> str:
    return _KIND_LABEL.get(item.get("kind", "other"), "其它")


# ------------------------------------------------------------------
# file — unacknowledged set for the Web UI
# ------------------------------------------------------------------

def load_new(namespace: str = "watch") -> list[dict[str, Any]]:
    """Unacknowledged new items (what the Web UI badges as NEW)."""
    path = _new_path(namespace)
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    return data.get("items", []) if isinstance(data, dict) else []


def _file_channel(items: list[dict[str, Any]], day: str, namespace: str = "watch") -> bool:
    path = _new_path(namespace)
    existing = load_new(namespace)
    known = {(i.get("fingerprint"), i.get("key")) for i in existing}
    for it in items:
        marker = (it.get("fingerprint"), it.get("key"))
        if marker not in known:
            known.add(marker)
            existing.append(it)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {"updated": datetime.now(timezone.utc).isoformat(), "day": day, "items": existing},
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return True


def ack_all(namespace: str = "watch") -> int:
    """Mark every new item as read. Returns how many were cleared."""
    path = _new_path(namespace)
    n = len(load_new(namespace))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
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
# webhook — generic / feishu / wecom
# ------------------------------------------------------------------

def _payload(items: list[dict[str, Any]], day: str, namespace: str = "watch") -> dict[str, Any]:
    fmt = os.environ.get("PAPER_GLEAN_WEBHOOK_FORMAT", "generic").lower()
    text = _summary(items, day, namespace)
    for it in items:
        text += f"\n· [{_kind(it)}] {_subject(it)} — {it.get('title', '')}"
        if it.get("url"):
            text += f"\n  {it['url']}"
    if fmt == "feishu":
        return {"msg_type": "text", "content": {"text": text}}
    if fmt == "wecom":
        return {"msgtype": "text", "text": {"content": text}}
    return {
        "text": text,
        "namespace": namespace,
        "day": day,
        "count": len(items),
        "items": [
            {
                "researcher": it.get("researcher"),
                "venue": it.get("venue"),
                "title": it.get("title"),
                "kind": it.get("kind"),
                "year": it.get("year"),
                "deadline": it.get("deadline"),
                "url": it.get("url"),
                "source": it.get("source"),
            }
            for it in items
        ],
    }


def _webhook_channel(items: list[dict[str, Any]], day: str, namespace: str = "watch") -> bool:
    url = os.environ.get("PAPER_GLEAN_WEBHOOK_URL", "").strip()
    if not url:
        return False
    body = json.dumps(_payload(items, day, namespace), ensure_ascii=False).encode("utf-8")
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

def push(
    items: list[dict[str, Any]],
    day: str | None = None,
    namespace: str = "watch",
) -> list[str]:
    """Deliver ``items`` through every enabled channel. Returns names that ran.

    Only two channels exist on purpose: ``file`` hands the items to the HTML
    pages, ``webhook`` is opt-in and off the machine. Nothing opens a window.
    """
    if not items:
        return []
    day = day or datetime.now().strftime("%Y-%m-%d")
    done: list[str] = []
    if _file_channel(items, day, namespace):
        done.append("file")
    if _webhook_channel(items, day, namespace):
        done.append("webhook")
    return done


def enabled_channels() -> dict[str, bool]:
    """Report which channels would fire (used by ``watch push-test``)."""
    return {
        "file": True,
        "webhook": bool(os.environ.get("PAPER_GLEAN_WEBHOOK_URL", "").strip()),
    }
