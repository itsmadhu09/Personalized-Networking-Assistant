# 3. Project Design — Solution Architecture

## High-Level Architecture

```
┌────────────────────┐        HTTP/JSON        ┌───────────────────────┐
│  Streamlit Frontend │ ───────────────────────▶│   FastAPI Backend      │
│    (frontend/ui.py) │◀─────────────────────── │    (backend/main.py)   │
└────────────────────┘                          └───────────┬────────────┘
                                                              │
                              ┌───────────────────────────────┼───────────────────────────────┐
                              ▼                                ▼                                ▼
                  ┌───────────────────────┐      ┌──────────────────────┐      ┌───────────────────────┐
                  │  event_analyzer.py     │      │  topic_generator.py   │      │  fact_checker.py        │
                  │  (DistilBERT zero-shot)│      │  (GPT-2 generation)    │      │  (Wikipedia API)         │
                  └───────────────────────┘      └──────────────────────┘      └───────────────────────┘
                              │
                              ▼
                  ┌───────────────────────┐
                  │  data/history.json      │
                  │  data/feedback.json     │
                  └───────────────────────┘
```

## Component Responsibilities

- **frontend/ui.py** — all user-facing interaction: input forms, results display, feedback buttons, history browser. Talks to the backend only via HTTP.
- **backend/main.py** — API surface (routes), request/response validation (Pydantic), and JSON persistence logic.
- **backend/event_analyzer.py** — single responsibility: text in, ranked themes out.
- **backend/topic_generator.py** — single responsibility: themes + interests in, cleaned starter strings out.
- **backend/fact_checker.py** — single responsibility: query in, Wikipedia summary out.

## Why This Separation

Each AI component is a pure function with no side effects (no direct file I/O, no route logic), which makes them independently unit-testable and safely swappable later — e.g. replacing GPT-2 with the Gemini API only requires changes inside `topic_generator.py`.

## API Contract Summary

| Endpoint | Method | Purpose |
|---|---|---|
| `/analyze-event` | POST | Theme extraction only |
| `/generate-conversation` | POST | Full pipeline + history logging |
| `/history` | GET | Retrieve past generations |
| `/feedback` | POST | Log thumbs up/down |
| `/fact-check` | POST | Wikipedia lookup |

## Scalability Notes (see also Milestone 8)

- JSON storage is fine for local/demo use; swap for SQLite/Postgres if moving beyond single-user local deployment
- Models are loaded lazily and cached per-process (`lru_cache`) to avoid reload cost per request
- Stateless API design means the backend could be horizontally scaled behind a load balancer if needed later
