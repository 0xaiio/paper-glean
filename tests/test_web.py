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
