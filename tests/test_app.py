"""Integration tests for Flask application routes."""

import json
from unittest.mock import patch, MagicMock
import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_route(client):
    res = client.get("/")
    assert res.status_code == 200
    assert b"Velo" in res.data


def test_sw_js_route(client):
    res = client.get("/sw.js")
    assert res.status_code == 200
    assert res.headers["Service-Worker-Allowed"] == "/"


def test_manifest_route(client):
    res = client.get("/static/manifest.json")
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data["short_name"] == "Velo"
    assert "share_target" in data


@patch("app._dl.download_subtitles")
def test_subtitles_endpoint(mock_sub, client):
    mock_sub.return_value = "tests/test_app.py"
    res = client.post("/api/subtitles/download", json={"url": "https://youtube.com/watch?v=fake", "lang": "es", "fmt": "srt"})
    assert res.status_code == 200


@patch("app._dl.download_batch")
def test_batch_start_endpoint(mock_batch, client):
    mock_batch.return_value = "/tmp/batch.zip"
    res = client.post("/api/batch/start", json={"urls": ["https://youtube.com/v1", "https://youtube.com/v2"], "format_id": "best"})
    assert res.status_code == 200
    data = json.loads(res.data)
    assert "download_id" in data
    assert data["download_id"].startswith("batch_")
