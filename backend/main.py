"""
main.py
---------
FastAPI application: routes, request/response models, and the JSON-file
persistence logic all live here, matching the flat backend/ layout.

Run with:
    uvicorn backend.main:app --reload

Swagger docs: http://localhost:8000/docs
"""

import json
import os
import threading
import uuid
from datetime import datetime

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from backend.event_analyzer import extract_themes
from backend.topic_generator import generate_starters
from backend.fact_checker import check_fact

load_dotenv()

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Personalized Networking Assistant API",
    description="Generates tailored conversation starters for networking events, "
                 "with theme extraction and Wikipedia-backed fact-checking.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Data persistence (writes to the top-level data/ folder)
# ---------------------------------------------------------------------------
_LOCK = threading.Lock()
_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
HISTORY_PATH = os.path.join(_DATA_DIR, "history.json")
FEEDBACK_PATH = os.path.join(_DATA_DIR, "feedback.json")


def _read(path: str) -> list[dict]:
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        content = f.read().strip()
        return json.loads(content) if content else []


def _write(path: str, data: list[dict]) -> None:
    os.makedirs(_DATA_DIR, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def add_history_entry(event_description: str, interests: list[str],
                       themes: list[str], starters: list[str]) -> str:
    with _LOCK:
        data = _read(HISTORY_PATH)
        entry_id = str(uuid.uuid4())[:8]
        data.append({
            "id": entry_id,
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "event_description": event_description,
            "interests": interests,
            "themes": themes,
            "starters": starters,
        })
        _write(HISTORY_PATH, data)
        return entry_id


def get_history() -> list[dict]:
    with _LOCK:
        return list(reversed(_read(HISTORY_PATH)))  # most recent first


def add_feedback(history_id: str, starter_index: int, useful: bool) -> None:
    with _LOCK:
        data = _read(FEEDBACK_PATH)
        data.append({
            "history_id": history_id,
            "starter_index": starter_index,
            "useful": useful,
            "timestamp": datetime.now().isoformat(timespec="seconds"),
        })
        _write(FEEDBACK_PATH, data)


# ---------------------------------------------------------------------------
# Request / response models
# ---------------------------------------------------------------------------
class EventRequest(BaseModel):
    event_description: str = Field(..., min_length=3, example="AI for Sustainable Cities")
    interests: list[str] = Field(default_factory=list, example=["climate change", "urban planning"])


class ThemeResult(BaseModel):
    label: str
    score: float


class AnalyzeResponse(BaseModel):
    themes: list[ThemeResult]


class ConversationResponse(BaseModel):
    themes: list[str]
    starters: list[str]
    history_id: str


class FactCheckRequest(BaseModel):
    query: str = Field(..., min_length=2, example="blockchain in healthcare")


class FactCheckResponse(BaseModel):
    query: str
    summary: str
    source_url: str | None = None
    found: bool


class FeedbackRequest(BaseModel):
    history_id: str
    starter_index: int
    useful: bool  # True = thumbs up, False = thumbs down


class HistoryEntry(BaseModel):
    id: str
    timestamp: str
    event_description: str
    interests: list[str]
    themes: list[str]
    starters: list[str]


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.get("/")
def root():
    return {"status": "ok", "message": "Personalized Networking Assistant API is running."}


@app.post("/analyze-event", response_model=AnalyzeResponse, tags=["analyze"])
def analyze_event(req: EventRequest):
    """Extract themes from an event description without generating starters."""
    pairs = extract_themes(req.event_description)
    return AnalyzeResponse(themes=[ThemeResult(label=l, score=s) for l, s in pairs])


@app.post("/generate-conversation", response_model=ConversationResponse, tags=["generate"])
def generate_conversation(req: EventRequest):
    """
    Full pipeline: extract themes, generate tailored conversation starters,
    and log the result to data/history.json.
    """
    theme_pairs = extract_themes(req.event_description)
    themes = [label for label, _ in theme_pairs]

    starters = generate_starters(themes, req.interests)

    history_id = add_history_entry(
        event_description=req.event_description,
        interests=req.interests,
        themes=themes,
        starters=starters,
    )

    return ConversationResponse(themes=themes, starters=starters, history_id=history_id)


@app.get("/history", response_model=list[HistoryEntry], tags=["generate"])
def history():
    """Return all past conversation generations, most recent first."""
    return get_history()


@app.post("/feedback", tags=["generate"])
def feedback(req: FeedbackRequest):
    """Record a thumbs up/down on a specific generated starter."""
    add_feedback(req.history_id, req.starter_index, req.useful)
    return {"status": "ok"}


@app.post("/fact-check", response_model=FactCheckResponse, tags=["fact-check"])
def fact_check(req: FactCheckRequest):
    """Look up a quick reference summary for the given query via Wikipedia."""
    result = check_fact(req.query)
    return FactCheckResponse(**result)
