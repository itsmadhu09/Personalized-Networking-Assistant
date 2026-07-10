"""
test_main.py
--------------
Automated compliance/testing suite: unit tests for each backend module
plus end-to-end API tests against the FastAPI app.

Run with:
    pytest tests/test_main.py -v
"""

from fastapi.testclient import TestClient

from backend.main import app
from backend.event_analyzer import extract_themes
from backend.topic_generator import generate_starters, _clean_starters, _build_prompt
from backend.fact_checker import check_fact

client = TestClient(app)


# ---------------------------------------------------------------------------
# event_analyzer.py
# ---------------------------------------------------------------------------
def test_extract_themes_returns_expected_count():
    themes = extract_themes("AI for Sustainable Cities", top_k=3)
    assert len(themes) == 3


def test_extract_themes_returns_label_score_pairs():
    themes = extract_themes("A conference on blockchain in healthcare")
    for label, score in themes:
        assert isinstance(label, str)
        assert 0.0 <= score <= 1.0


# ---------------------------------------------------------------------------
# topic_generator.py
# ---------------------------------------------------------------------------
def test_generate_starters_returns_requested_count():
    starters = generate_starters(["AI", "sustainability"], ["climate change"], n=3)
    assert 1 <= len(starters) <= 3
    assert all(isinstance(s, str) and s.strip() for s in starters)


def test_clean_starters_strips_prompt_and_splits():
    prompt = _build_prompt(["AI"], ["healthcare"])
    raw = prompt + " What drew you to AI in healthcare?\n2. How do you see it evolving?"
    cleaned = _clean_starters(raw, prompt, n=2)
    assert len(cleaned) <= 2
    assert all(prompt not in c for c in cleaned)


# ---------------------------------------------------------------------------
# fact_checker.py
# ---------------------------------------------------------------------------
def test_check_fact_found_returns_summary():
    result = check_fact("Blockchain")
    assert result["found"] is True
    assert len(result["summary"]) > 0
    assert result["source_url"].startswith("http")


def test_check_fact_not_found_returns_friendly_message():
    result = check_fact("asdkjqwoeiuqwoeqwoeasdkqjwoe12345nonsense")
    assert result["found"] is False
    assert "No Wikipedia page found" in result["summary"]


# ---------------------------------------------------------------------------
# API endpoints (main.py)
# ---------------------------------------------------------------------------
def test_root_health_check():
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_analyze_event_endpoint():
    resp = client.post("/analyze-event", json={
        "event_description": "AI for Sustainable Cities",
        "interests": ["climate change"],
    })
    assert resp.status_code == 200
    assert len(resp.json()["themes"]) > 0


def test_generate_conversation_endpoint():
    resp = client.post("/generate-conversation", json={
        "event_description": "AI for Sustainable Cities",
        "interests": ["climate change", "urban planning"],
    })
    assert resp.status_code == 200
    body = resp.json()
    assert "starters" in body
    assert "history_id" in body


def test_fact_check_endpoint():
    resp = client.post("/fact-check", json={"query": "Blockchain"})
    assert resp.status_code == 200
    assert resp.json()["found"] is True


def test_history_endpoint_after_generation():
    client.post("/generate-conversation", json={
        "event_description": "Fintech Innovation Summit",
        "interests": ["finance"],
    })
    resp = client.get("/history")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
    assert len(resp.json()) > 0


def test_feedback_endpoint():
    gen_resp = client.post("/generate-conversation", json={
        "event_description": "Healthcare AI Summit",
        "interests": ["healthcare"],
    })
    history_id = gen_resp.json()["history_id"]
    resp = client.post("/feedback", json={
        "history_id": history_id, "starter_index": 0, "useful": True,
    })
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"
