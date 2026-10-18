import main as scope
from fastapi.testclient import TestClient


def test_fallback_requirements_keep_evidence():
    requirements = scope.fallback_requirements("We need a city filter.\nWe also need a profile contact form.")
    assert len(requirements) == 2
    assert all(item["evidence"] == item["text"] for item in requirements)
    assert all(item["status"] == "needs_review" for item in requirements)


def test_health_endpoint():
    with TestClient(scope.app) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_unknown_baseline_returns_404(tmp_path, monkeypatch):
    monkeypatch.setattr(scope, "DB_PATH", str(tmp_path / "meetings.db"))
    with TestClient(scope.app) as client:
        response = client.post("/v1/meetings/compare", json={
            "baseline_id": "not-a-real-id",
            "followup_transcript": "The client wants an additional membership filter."
        })
    assert response.status_code == 404
