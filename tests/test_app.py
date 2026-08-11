"""Integration tests for Flask application routes."""

import json
import time
from unittest.mock import patch, MagicMock
import pytest
import app as app_module
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


def test_runtime_mode_is_explicitly_validated():
    assert app_module.get_runtime_mode("local") == "local"
    assert app_module.get_runtime_mode("render") == "render"
    with pytest.raises(ValueError):
        app_module.get_runtime_mode("other")


def test_api_responses_are_not_cached(client):
    res = client.get("/api/health")
    assert res.headers["Cache-Control"] == "no-store, max-age=0"
    assert res.headers["Pragma"] == "no-cache"


def test_service_worker_rotates_cache_and_refreshes_app_script(client):
    source = client.get("/sw.js").get_data(as_text=True)

    assert "velo-v3.0.1" in source
    assert "requestPath === '/static/app.js'" in source
    assert "fetch(event.request).then" in source
    assert "catch(() => caches.match(event.request))" in source
    assert "requestPath.startsWith('/api/')" in source


@patch("app.threading.Thread")
@patch("app._dl.download")
def test_download_exception_transitions_to_pollable_error(mock_download, mock_thread, client, monkeypatch):
    downloads = {}
    monkeypatch.setattr("app._downloads", downloads)
    mock_download.side_effect = RuntimeError("upstream download failed")

    res = client.post(
        "/api/download/start",
        json={"url": "https://example.com/video", "format_id": "best"},
    )
    assert res.status_code == 200

    download_id = res.get_json()["download_id"]
    worker = mock_thread.call_args.kwargs["target"]
    worker()

    status = client.get(f"/api/download/status/{download_id}")
    assert status.status_code == 200
    assert status.get_json()["status"] == "error"
    assert status.get_json()["error"] == "upstream download failed"


def test_render_file_cleanup_happens_when_response_closes(monkeypatch, tmp_path):
    job_dir = tmp_path / "job"
    job_dir.mkdir()
    file_path = job_dir / "video.mp4"
    file_path.write_bytes(b"video")
    downloads = {
        "job1": {"status": "done", "filepath": str(file_path), "created_at": time.time(), "job_dir": str(job_dir)}
    }
    monkeypatch.setattr(app_module, "_RUNTIME_MODE", "render")
    monkeypatch.setattr(app_module, "_downloads", downloads)

    with app.test_request_context("/api/download/file/job1"):
        response = app_module.download_file("job1")
        assert file_path.exists()
        response.close()

    assert not job_dir.exists()
    assert "job1" not in downloads


def test_render_error_cleanup_removes_job_state(monkeypatch):
    downloads = {}
    monkeypatch.setattr(app_module, "_RUNTIME_MODE", "render")
    monkeypatch.setattr(app_module, "_downloads", downloads)
    monkeypatch.setattr(app_module, "_dl", MagicMock())
    app_module._dl.download.side_effect = RuntimeError("failed")

    with patch("app.threading.Thread") as mock_thread, app.test_client() as client:
        response = client.post(
            "/api/download/start",
            json={"url": "https://example.com/video", "format_id": "best"},
        )
        assert response.status_code == 200
        mock_thread.call_args.kwargs["target"]()

    assert downloads == {}


def test_render_expiry_removes_state_and_files(monkeypatch, tmp_path):
    job_dir = tmp_path / "expired"
    job_dir.mkdir()
    (job_dir / "partial.part").write_text("partial")
    downloads = {
        "expired": {
            "status": "downloading",
            "created_at": time.time() - 120,
            "job_dir": str(job_dir),
        }
    }
    monkeypatch.setattr(app_module, "_RUNTIME_MODE", "render")
    monkeypatch.setattr(app_module, "_RENDER_JOB_TTL_SECONDS", 60)
    monkeypatch.setattr(app_module, "_downloads", downloads)

    assert app_module._expire_job_if_needed("expired", downloads["expired"])
    assert not job_dir.exists()
    assert downloads == {}


def test_download_output_does_not_choose_arbitrary_file(tmp_path):
    (tmp_path / "video.mp4").write_bytes(b"video")
    (tmp_path / "video.info.json").write_text("metadata")
    with pytest.raises(ValueError, match="identified safely"):
        app_module._resolve_download_file("", str(tmp_path))


def test_manifest_route(client):
    res = client.get("/static/manifest.json")
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data["short_name"] == "Velo"
    assert "share_target" in data


@patch("app.get_runtime_status")
def test_health_route_exposes_safe_runtime_status(mock_status, client):
    mock_status.return_value = {"node": True, "ffmpeg": True, "youtube_cookies": False}

    res = client.get("/api/health")
    data = json.loads(res.data)

    assert res.status_code == 200
    assert data["status"] == "ok"
    assert data["runtime"] == {"node": True, "ffmpeg": True}
    assert data["youtube"]["cookies_configured"] is False


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
