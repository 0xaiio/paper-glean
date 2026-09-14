"""Persistent launcher for the paper-glean web app (used at Windows logon).

Why this file exists
--------------------
A ``subprocess.Popen(..., DETACHED_PROCESS)`` child is killed together with the
tool call that spawned it, so the daily automation cannot keep the web app
alive that way. A logon auto-start entry (or a Task Scheduler task) runs
outside that job and survives.

``pythonw.exe`` has no console (``sys.stdout`` / ``sys.stderr`` are ``None``),
so they are pointed at ``logs/web-task.log`` before uvicorn configures logging;
otherwise logs would be silently dropped.
"""

from __future__ import annotations

import os
import sys

HOST = os.environ.get("PAPER_GLEAN_HOST", "127.0.0.1")
PORT = int(os.environ.get("PAPER_GLEAN_PORT", "8011"))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

LOG_DIR = os.path.join(ROOT, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

if getattr(sys, "stdout", None) is None or getattr(sys, "stderr", None) is None:
    stream = open(os.path.join(LOG_DIR, "web-task.log"), "a", encoding="utf-8", buffering=1)
    sys.stdout = stream
    sys.stderr = stream

import uvicorn  # noqa: E402  (imported after the stream redirection)

from glean.web.main import create_app  # noqa: E402


def main() -> None:
    print(f"[web_task] starting on {HOST}:{PORT} (pid={os.getpid()})", flush=True)
    uvicorn.run(create_app(), host=HOST, port=PORT)


if __name__ == "__main__":
    main()
