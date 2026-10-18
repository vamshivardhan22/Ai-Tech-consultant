import hashlib
import main as kb
from fastapi.testclient import TestClient


def test_terms_normalizes_and_ignores_generic_words():
    assert kb.terms("How to use API v2 settings") == {"api", "settings"}


def test_seeded_demo_answer_is_cited_and_disclosed(tmp_path, monkeypatch):
    monkeypatch.setattr(kb, "DB_PATH", str(tmp_path / "knowledge.db"))
    kb.init_db()
    kb.seed_demo_docs()
    with TestClient(kb.app) as client:
        response = client.post("/v1/answers", json={"question": "How do I use the dashboard settings?"})
    assert response.status_code == 200
    data = response.json()
    assert data["citations"]
    assert data["abstained"] is False
    assert "demo fixture" in data["citations"][0]["title"].lower()


def test_unknown_question_abstains_and_escalates(tmp_path, monkeypatch):
    monkeypatch.setattr(kb, "DB_PATH", str(tmp_path / "knowledge.db"))
    kb.init_db()
    kb.seed_demo_docs()
    with TestClient(kb.app) as client:
        response = client.post("/v1/answers", json={"question": "What is the orbital plasma fermentation policy?"})
    assert response.status_code == 200
    data = response.json()
    assert data["abstained"] is True
    assert data["escalation_id"] is not None
    assert data["citations"] == []


def test_hash_is_stable():
    content = "stable content"
    assert hashlib.sha256(content.encode()).hexdigest() == hashlib.sha256(content.encode()).hexdigest()
