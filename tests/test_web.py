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


# ------------------------------------------------------------------
# /ccf + /api/ccf/* (isolated — never touch the real ccf.md /
# data/ccf_new.json of the working repo)
# ------------------------------------------------------------------

_CCF_SAMPLE = """# CCF-A 会议 / 期刊监控

## 会议

- [x] **SIGMOD** — ACM SIGMOD Conference
  - area: 数据库/数据挖掘/内容检索
  - homepage: https://sigmod.org
  - ccf: A

- [ ] **STOC** — ACM Symposium on Theory of Computing
  - area: 计算机科学理论
  - homepage: https://acm-stoc.org
  - ccf: A

## 期刊

- [x] **TODS** — ACM Transactions on Database Systems
  - area: 数据库/数据挖掘/内容检索
  - homepage: https://dl.acm.org/journal/tods
  - issn: 0362-5915
  - ccf: A
"""


@pytest.fixture
def isolated_ccf(tmp_path, monkeypatch):
    from glean import ccf, notify

    md = tmp_path / "ccf.md"
    md.write_text(_CCF_SAMPLE, encoding="utf-8")
    monkeypatch.setattr(ccf, "CCF_MD", md)
    monkeypatch.setattr(ccf, "CCF_STATE", tmp_path / "ccf_state.json")
    monkeypatch.setattr(ccf, "CCF_EVENTS", tmp_path / "ccf_events.jsonl")
    monkeypatch.setattr(ccf, "CCF_DIGEST_MD", tmp_path / "CCF-digest.md")
    monkeypatch.setattr(notify, "CCF_NEW", tmp_path / "ccf_new.json")
    return tmp_path


def test_ccf_page(client):
    response = client.get("/ccf")
    assert response.status_code == 200
    assert "CCF" in response.text


def test_api_ccf_venues(client, isolated_ccf):
    rows = client.get("/api/ccf/venues").json()
    assert {r["name"] for r in rows} == {"SIGMOD", "STOC", "TODS"}
    # area / enabled filters
    only_conf = client.get("/api/ccf/venues?enabled=true").json()
    assert {r["name"] for r in only_conf} == {"SIGMOD", "TODS"}


def test_api_ccf_new_and_events(client, isolated_ccf):
    assert client.get("/api/ccf/new").json()["count"] == 0
    assert isinstance(client.get("/api/ccf/events").json(), list)


def test_api_ccf_add_then_toggle_then_remove(client, isolated_ccf):
    added = client.post(
        "/api/ccf/venues",
        data={
            "name": "EuroSys",
            "homepage": "https://www.eurosys.org",
            "kind": "conference",
            "area": "系统软件",
            "ccf": "A",
        },
    )
    assert added.status_code == 200
    body = added.json()
    assert body["success"] is True
    assert body["venue"]["name"] == "EuroSys"
    key = body["venue"]["key"]

    assert "EuroSys" in [v["name"] for v in client.get("/api/ccf/venues").json()]

    toggled = client.post(f"/api/ccf/venues/{key}/toggle?enabled=false")
    assert toggled.status_code == 200
    assert toggled.json()["enabled"] is False
    after = {v["key"]: v for v in client.get("/api/ccf/venues").json()}
    assert after[key]["enabled"] is False

    removed = client.delete(f"/api/ccf/venues/{key}")
    assert removed.status_code == 200
    assert removed.json()["success"] is True
    assert "EuroSys" not in [v["name"] for v in client.get("/api/ccf/venues").json()]


def test_api_ccf_add_duplicate_is_conflict(client, isolated_ccf):
    dup = client.post(
        "/api/ccf/venues",
        data={"name": "SIGMOD", "homepage": "https://sigmod.org"},
    )
    assert dup.status_code == 409


def test_api_ccf_add_without_homepage_is_rejected(client, isolated_ccf):
    # FastAPI's required-Field guard rejects a truly empty value with 422…
    empty = client.post("/api/ccf/venues", data={"name": "NoHome", "homepage": ""})
    assert empty.status_code == 422
    # …while a whitespace-only homepage reaches the handler and is a 409 there.
    blank = client.post("/api/ccf/venues", data={"name": "NoHome", "homepage": "   "})
    assert blank.status_code == 409


def test_api_ccf_remove_unknown_is_404(client, isolated_ccf):
    assert client.delete("/api/ccf/venues/no-such-key").status_code == 404


def test_api_ccf_toggle_area_is_bulk(client, isolated_ccf):
    resp = client.post(
        "/api/ccf/venues/toggle-area",
        data={"area": "数据库", "enabled": "false"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["count"] == 2  # SIGMOD + TODS
    enabled = {v["name"]: v["enabled"] for v in client.get("/api/ccf/venues").json()}
    assert enabled["SIGMOD"] is False and enabled["TODS"] is False
    assert enabled["STOC"] is False  # untouched


def test_api_ccf_ack_clears_only_ccf_badge(client, isolated_ccf):
    from glean import notify

    notify.CCF_NEW.parent.mkdir(parents=True, exist_ok=True)
    notify.CCF_NEW.write_text(
        '{"day": "2026-09-14", "items": [{"title": "SIGMOD 2027 CFP", "kind": "cfp"}]}',
        encoding="utf-8",
    )
    assert client.get("/api/ccf/new").json()["count"] == 1

    acked = client.post("/api/ccf/ack")
    assert acked.status_code == 200
    assert acked.json()["cleared"] == 1
    assert client.get("/api/ccf/new").json()["count"] == 0
