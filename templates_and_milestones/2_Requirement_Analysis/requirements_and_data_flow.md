# 2. Requirement Analysis

## Functional Requirements

| ID | Requirement |
|---|---|
| FR-1 | User can input an event description and their interests |
| FR-2 | System extracts themes from the event description (DistilBERT) |
| FR-3 | System generates 2–3 tailored conversation starters (GPT-2) |
| FR-4 | User can fact-check a topic via Wikipedia before the event |
| FR-5 | System logs every generation to history |
| FR-6 | User can mark a starter as useful (👍) or not (👎) |
| FR-7 | User can view past conversation history |

## Non-Functional Requirements

- Response time: theme extraction + generation under ~10s on CPU after model warm-up
- Local-first: no external DB required, works fully offline except Wikipedia calls
- Modularity: each AI component (analyzer/generator/fact-checker) independently testable

## Tech Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI |
| Frontend | Streamlit |
| Theme extraction | DistilBERT (`typeform/distilbert-base-uncased-mnli`, zero-shot) |
| Generation | GPT-2 (Hugging Face `transformers`) |
| Fact-checking | Wikipedia API (`wikipedia-api`) |
| Storage | Local JSON files (`data/history.json`, `data/feedback.json`) |
| Testing | pytest, httpx, FastAPI TestClient |

## Data Flow Diagram (textual)

```
[User Input: event_description, interests]
              │
              ▼
     ┌─────────────────┐
     │  event_analyzer  │  (DistilBERT zero-shot classification)
     └────────┬─────────┘
              │ themes[]
              ▼
     ┌─────────────────┐
     │ topic_generator  │  (GPT-2 text generation + cleanup)
     └────────┬─────────┘
              │ starters[]
              ▼
     ┌─────────────────┐        ┌──────────────────┐
     │   main.py API    │───────▶│ data/history.json │
     └────────┬─────────┘        └──────────────────┘
              │
              ▼
     [Streamlit UI displays themes + starters]
              │
              ▼ (user clicks 👍 / 👎)
     ┌──────────────────┐
     │ data/feedback.json│
     └──────────────────┘

Separately:
[User query] ──▶ fact_checker.py ──▶ Wikipedia API ──▶ [Summary + source URL]
```

*Replace this text diagram with an actual DFD image/diagram tool export
(e.g. draw.io, Lucidchart) before submission if your mentor expects a visual.*
