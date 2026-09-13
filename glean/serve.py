"""Local web service helpers for the daily pipeline.

The scheduled pipeline needs a guarantee that the paper-glean web app is
reachable at the end of a run, so that the digest can be presented directly
from the local server (same-origin ``/api/*`` calls, so ratings and downloads
work) instead of a static file preview.

This module keeps that logic in one place:

* :func:`probe` — is the app already answering ``/api/ping``?
* :func:`start_background` — spawn ``python -m glean.web`` detached, logging to ``logs/``
* :func:`ensure` — probe, and only start when needed; then wait until online

Environment gotchas baked in:

* Loopback probes **must bypass** ``HTTP_PROXY`` / ``HTTPS_PROXY``. This
  workstation injects a proxy that would otherwise turn ``127.0.0.1`` requests
  into ``502 CONNECT tunnel failed``. All probe traffic uses an opener with an
  empty ``ProxyHandler``.
* On Windows the child is started with ``DETACHED_PROCESS`` so it survives the
  parent (the scheduled task) exiting.
"""

from __future__ import annotations

import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from glean.config import REPO_DIR

DEFAULT_HOST = os.environ.get("HOST", "127.0.0.1")
DEFAULT_PORT = int(os.environ.get("PORT", "8000"))

PING_PATH = "/api/ping"
LOG_DIR = REPO_DIR / "logs"


def base_url(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> str:
    """Return the root URL of the local web app."""
    return f"http://{host}:{port}"


def ping_url(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> str:
    """Return the liveness-probe URL."""
    return base_url(host, port) + PING_PATH


def _no_proxy_opener() -> urllib.request.OpenerDirector:
    """An opener that never routes requests through ``*_PROXY`` env vars."""
    return urllib.request.build_opener(urllib.request.ProxyHandler({}))


def probe(
    host: str = DEFAULT_HOST,
    port: int = DEFAULT_PORT,
    timeout: float = 2.0,
    opener: urllib.request.OpenerDirector | None = None,
) -> bool:
    """Return ``True`` if the web app answers ``/api/ping`` with HTTP 200."""
    op = opener or _no_proxy_opener()
    try:
        with op.open(ping_url(host, port), timeout=timeout) as resp:
            return int(getattr(resp, "status", 200)) == 200
    except (urllib.error.URLError, OSError, ValueError):
        return False


def log_path(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> Path:
    """Path of the detached-server log file (created on demand)."""
    return LOG_DIR / f"serve-{host}-{port}.log"


def start_background(
    host: str = DEFAULT_HOST,
    port: int = DEFAULT_PORT,
    log_file: Path | None = None,
) -> subprocess.Popen:
    """Spawn ``python -m glean.web`` detached from the current process.

    The child keeps running after the caller (e.g. a scheduled task) exits.
    Its stdout/stderr are appended to ``logs/serve-<host>-<port>.log`` so a
    failed start can be diagnosed after the fact.
    """
    target = log_file or log_path(host, port)
    target.parent.mkdir(parents=True, exist_ok=True)
    handle = open(target, "a", encoding="utf-8", errors="replace")  # noqa: SIM115 - kept open for child lifetime
    handle.write(f"\n=== start {time.strftime('%Y-%m-%d %H:%M:%S')} -> {host}:{port} ===\n")
    handle.flush()

    kwargs: dict = {
        "cwd": str(REPO_DIR),
        "stdout": handle,
        "stderr": subprocess.STDOUT,
        "stdin": subprocess.DEVNULL,
    }
    if os.name == "nt":  # pragma: no cover - platform specific
        kwargs["creationflags"] = (
            subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS
        )
    else:  # pragma: no cover - platform specific
        kwargs["start_new_session"] = True

    return subprocess.Popen(
        [sys.executable, "-m", "glean.web", "--host", host, "--port", str(port)],
        **kwargs,
    )


def ensure(
    host: str = DEFAULT_HOST,
    port: int = DEFAULT_PORT,
    wait: float = 15.0,
    log_file: Path | None = None,
) -> tuple[bool, bool]:
    """Make sure the web app is online.

    Returns ``(online, started)`` where ``started`` says whether this call had
    to spawn a new server process. Probing is cheap, so an already-running
    instance is reused and never duplicated.
    """
    if probe(host, port):
        return True, False

    try:
        start_background(host, port, log_file=log_file)
    except OSError:
        return False, False

    deadline = time.monotonic() + max(wait, 0.0)
    while time.monotonic() < deadline:
        if probe(host, port):
            return True, True
        time.sleep(0.4)
    return False, True
