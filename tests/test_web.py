"""Tests for the web API."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from glean.web.main import create_app


@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)


def test_root_redirect(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "redirect" in response.text.lower() or "/digest" in response.text


def test_digest_page(client):
    response = client.get("/digest")
    assert response.status_code == 200
    assert "Paper-Glean" in response.text


def test_profile_page(client):
    response = client.get("/profile")
    assert response.status_code == 200
    assert "Interest Profile" in response.text


def test_archive_page(client):
    response = client.get("/archive")
    assert response.status_code == 200
    assert "Archive Library" in response.text


def test_api_days(client):
    response = client.get("/api/days")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_api_ping(client):
    """Liveness endpoint used by the daily scheduler's service probe."""
    response = client.get("/api/ping")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "paper-glean"
    assert "version" in data
    assert "time" in data


def test_api_papers(client):
    response = client.get("/api/papers")
    assert response.status_code == 200
    data = response.json()
    assert "papers" in data
    assert "total" in data


def test_api_paper_detail(client):
    response = client.get("/api/papers/2607.25916")
    assert response.status_code in (200, 404)


def test_api_interests(client):
    response = client.get("/api/interests")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_htmx_paper_list(client):
    response = client.get("/htmx/paper-list")
    assert response.status_code == 200


def test_watch_page(client):
    response = client.get("/watch")
    assert response.status_code == 200
    assert "学者监控" in response.text


def test_api_watch_researchers(client):
    response = client.get("/api/watch/researchers")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_api_watch_new(client):
    response = client.get("/api/watch/new")
    assert response.status_code == 200
    data = response.json()
    assert "count" in data
    assert isinstance(data["items"], list)


def test_api_watch_events(client):
    response = client.get("/api/watch/events")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ------------------------------------------------------------------
# /api/watch/* mutation endpoints (isolated — never touch the real
# watchlist.md / data/watch_new.json of the working repo)
# ------------------------------------------------------------------

_WATCH_SAMPLE = """# 学者监控名单

## 监控中

### 魏恒峰 Hengfeng Wei
- homepage: https://hengxin.github.io
- enabled: true

## 已暂停
"""


@pytest.fixture
def isolated_watch(tmp_path, monkeypatch):
    from glean import notify, watch

    wl = tmp_path / "watchlist.md"
    wl.write_text(_WATCH_SAMPLE, encoding="utf-8")
    monkeypatch.setattr(watch, "WATCHLIST_MD", wl)
    monkeypatch.setattr(watch, "WATCH_STATE", tmp_path / "watch_state.json")
    monkeypatch.setattr(watch, "WATCH_EVENTS", tmp_path / "watch_events.jsonl")
    monkeypatch.setattr(watch, "WATCH_DIGEST_MD", tmp_path / "WATCH-digest.md")
    monkeypatch.setattr(notify, "WATCH_NEW", tmp_path / "watch_new.json")
    return tmp_path


def test_api_watch_add_then_toggle_then_remove(client, isolated_watch):
    added = client.post(
        "/api/watch/researchers",
        data={
            "name": "Test Person",
            "homepage": "https://example.edu/~tp",
            "tags": "db; formal",
        },
    )
    assert added.status_code == 200
    body = added.json()
    assert body["success"] is True
    assert body["researcher"]["name"] == "Test Person"
    assert body["researcher"]["tags"] == ["db", "formal"]
    key = body["researcher"]["key"]

    listed = client.get("/api/watch/researchers").json()
    assert "Test Person" in [r["name"] for r in listed]

    toggled = client.post(f"/api/watch/researchers/{key}/toggle?enabled=false")
    assert toggled.status_code == 200
    assert toggled.json()["enabled"] is False
    after_toggle = {r["key"]: r for r in client.get("/api/watch/researchers").json()}
    assert after_toggle[key]["enabled"] is False

    removed = client.delete(f"/api/watch/researchers/{key}")
    assert removed.status_code == 200
    assert removed.json()["success"] is True
    assert "Test Person" not in [
        r["name"] for r in client.get("/api/watch/researchers").json()
    ]


def test_api_watch_add_duplicate_is_conflict(client, isolated_watch):
    first = client.post(
        "/api/watch/researchers",
        data={"name": "魏恒峰 Hengfeng Wei", "homepage": "https://hengxin.github.io"},
    )
    assert first.status_code == 409


def test_api_watch_remove_unknown_is_404(client, isolated_watch):
    response = client.delete("/api/watch/researchers/no-such-key")
    assert response.status_code == 404


def test_api_watch_ack_clears_badge(client, isolated_watch):
    from glean import notify

    notify.WATCH_NEW.parent.mkdir(parents=True, exist_ok=True)
    notify.WATCH_NEW.write_text(
        '{"day": "2026-09-14", "items": [{"title": "A New Paper", "kind": "paper"}]}',
        encoding="utf-8",
    )
    assert client.get("/api/watch/new").json()["count"] == 1

    acked = client.post("/api/watch/ack")
    assert acked.status_code == 200
    assert acked.json()["cleared"] == 1
    assert client.get("/api/watch/new").json()["count"] == 0
