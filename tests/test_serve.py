"""Tests for :mod:`glean.serve` — the local web service keeper.

These tests never leave a stray server behind: ``probe``/``start_background``
are driven through fake openers or monkeypatched, except for one end-to-end
check against a loopback HTTP server bound to an ephemeral port.
"""

from __future__ import annotations

import threading
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest

from glean import serve


class _PingHandler(BaseHTTPRequestHandler):
    """Answers any GET with 200 + a JSON body, like ``/api/ping`` does."""

    def do_GET(self):  # noqa: N802 - http.server naming
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"status": "ok"}')

    def log_message(self, *args):  # silence test output
        pass


@pytest.fixture
def live_server():
    """A throwaway loopback server; yields its ephemeral port."""
    srv = ThreadingHTTPServer(("127.0.0.1", 0), _PingHandler)
    thread = threading.Thread(target=srv.serve_forever, daemon=True)
    thread.start()
    try:
        yield srv.server_address[1]
    finally:
        srv.shutdown()
        srv.server_close()


def test_base_url_and_ping_url():
    assert serve.base_url("127.0.0.1", 8000) == "http://127.0.0.1:8000"
    assert serve.ping_url("127.0.0.1", 8000) == "http://127.0.0.1:8000/api/ping"


def test_no_proxy_opener_carries_no_active_proxy(monkeypatch):
    """The opener must never consult ``*_PROXY`` for loopback requests.

    ``build_opener(ProxyHandler({}))`` ends up with no *active* proxy handler
    (an empty dict yields no dynamic ``*_open`` methods), which is precisely
    why the loopback probe does not get hijacked. Assert the invariant, not
    the mechanism: no proxy handler may carry non-empty proxies.
    """
    monkeypatch.setenv("HTTP_PROXY", "http://127.0.0.1:52314")
    monkeypatch.setenv("HTTPS_PROXY", "http://127.0.0.1:52314")

    op = serve._no_proxy_opener()
    active = [
        h
        for h in op.handlers
        if isinstance(h, urllib.request.ProxyHandler) and h.proxies
    ]
    assert active == [], "an active ProxyHandler would route loopback via the env proxy"


def test_probe_reaches_loopback_despite_bogus_env_proxy(monkeypatch, live_server):
    """End-to-end guard for the 502-on-loopback regression."""
    monkeypatch.setenv("HTTP_PROXY", "http://127.0.0.1:1")
    monkeypatch.setenv("HTTPS_PROXY", "http://127.0.0.1:1")
    monkeypatch.setenv("NO_PROXY", "")

    assert serve.probe("127.0.0.1", live_server, timeout=3.0) is True


def test_probe_hits_ping_path():
    calls: dict = {}

    class _Resp:
        status = 200

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

    class _Opener:
        def open(self, url, timeout=None):
            calls["url"] = url
            calls["timeout"] = timeout
            return _Resp()

    assert serve.probe("127.0.0.1", 8000, timeout=1.0, opener=_Opener()) is True
    assert calls["url"] == "http://127.0.0.1:8000/api/ping"
    assert calls["timeout"] == 1.0


def test_probe_false_on_error():
    class _Opener:
        def open(self, url, timeout=None):
            raise urllib.error.URLError("connection refused")

    assert serve.probe(opener=_Opener()) is False


def test_log_path_lives_under_logs():
    path = serve.log_path("127.0.0.1", 8000)
    assert path.name == "serve-127.0.0.1-8000.log"
    assert path.parent.name == "logs"


def test_ensure_reuses_online_instance(monkeypatch):
    monkeypatch.setattr(serve, "probe", lambda *a, **k: True)
    online, started = serve.ensure("127.0.0.1", 8000)
    assert online is True
    assert started is False


def test_ensure_reports_failure_when_spawn_fails(monkeypatch):
    monkeypatch.setattr(serve, "probe", lambda *a, **k: False)

    def _boom(*a, **k):
        raise OSError("cannot spawn")

    monkeypatch.setattr(serve, "start_background", _boom)
    online, started = serve.ensure("127.0.0.1", 8000, wait=0)
    assert online is False
    assert started is False
