# Personalized Networking Assistant

AI-powered web app that generates tailored conversation starters for networking
events. Extracts themes from an event description with **DistilBERT**
(zero-shot classification), generates human-like prompts with **GPT-2**,
verifies quick facts via the **Wikipedia API**, and logs conversation history
and feedback to local JSON files.

## Project Structure

```
personalized-networking-assistant/
├── .env                          Keep your secret API keys here
├── .gitignore                    Tells Git to ignore venv/ and .env
├── requirements.txt              List of all pip packages
├── README.md                     This guide
│
├── backend/                      FastAPI code
│   ├── main.py                   FastAPI routes & logic
│   ├── event_analyzer.py         DistilBERT pipeline helper
│   ├── topic_generator.py        GPT-2 generation helper
│   └── fact_checker.py           Wikipedia API integration
│
├── frontend/                     Streamlit UI code
│   └── ui.py                     Streamlit views, tabs, and layout
│
├── data/                         Real-time data logs
│   ├── history.json              Chronological generation log
│   └── feedback.json             Thumbs up/down metrics
│
├── tests/                        Automated testing
│   └── test_main.py              pytest suite (unit + API tests)
│
└── templates_and_milestones/     Word/PDF reports for mentor review
    ├── 1_Brainstorming_Ideation/       Problem Statement, Empathy Map
    ├── 2_Requirement_Analysis/         Data Flow Diagram, Tech Stack
    ├── 3_Project_Design/               Solution Architecture
    └── 8_Project_Demonstration/        Demo Planning, Scalability Plan
```

## Setup

Requires Python 3.10+.

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Copy your real keys into `.env` (never commit this file — it's already in
`.gitignore`). The `GEMINI_API_KEY` slot is there if you later want to swap
or supplement GPT-2 with Google's Gemini API.

First run will download the DistilBERT and GPT-2 model weights from
Hugging Face (a few hundred MB total) — this can take a few minutes.

## Running locally

**Terminal 1 — backend:**
```bash
uvicorn backend.main:app --reload
```
API docs (Swagger UI): http://localhost:8000/docs

**Terminal 2 — frontend:**
```bash
streamlit run frontend/ui.py
```
App: http://localhost:8501

> Run both commands from the project root so the `backend` package resolves
> correctly.

## Running tests

```bash
pytest tests/test_main.py -v
```

## API Endpoints

| Method | Path                     | Description                                |
|--------|--------------------------|---------------------------------------------|
| POST   | `/analyze-event`         | Extract themes from an event description   |
| POST   | `/generate-conversation` | Generate conversation starters + log history|
| GET    | `/history`               | Retrieve past generations                    |
| POST   | `/feedback`              | Record thumbs up/down on a starter          |
| POST   | `/fact-check`            | Wikipedia-backed quick fact lookup          |

## Notes / known limitations

- GPT-2 is a small, general-purpose model — outputs are post-processed but
  can still be uneven. See `templates_and_milestones/8_Project_Demonstration/`
  for the plan to upgrade this.
- `data/history.json` and `data/feedback.json` are flat-file storage,
  intended for local dev/demo use, not concurrent multi-user production.
- Model loading happens lazily on first API call — the very first request
  after starting the server will be noticeably slower than the rest.

## Team

C S Madhulika (Team Lead) · Meghana Kaverigari · Shaik Thanveen Afnan ·
Veerapuram Sreeram · Venkatasuneel R
