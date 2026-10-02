# 🔗 Linkora

### Connect smarter. Converse better.

Linkora is an AI-powered web application that generates personalized conversation starters for networking events. It extracts themes from event descriptions using **DistilBERT** (zero-shot classification), generates conversation prompts using **GPT-2**, verifies quick facts through the **Wikipedia API**, and records conversation history and user feedback in local JSON files.

## Project Structure

```text
Linkora/
├── .env                          # Keep your secret API keys here
├── .gitignore                    # Ignores venv/ and .env
├── requirements.txt              # Python dependencies
├── README.md                     # Project documentation
│
├── backend/                      # FastAPI backend
│   ├── main.py                   # API routes and logic
│   ├── event_analyzer.py         # DistilBERT pipeline helper
│   ├── topic_generator.py        # GPT-2 generation helper
│   └── fact_checker.py           # Wikipedia API integration
│
├── frontend/                     # Streamlit frontend
│   └── ui.py                     # UI, tabs, and layout
│
├── data/                         # Local data logs
│   ├── history.json              # Conversation history
│   └── feedback.json             # User feedback metrics
│
├── tests/                        # Automated testing
│   └── test_main.py              # Unit and API tests
│
└── templates_and_milestones/     # Project reports and documentation
    ├── 1_Brainstorming_Ideation/
    ├── 2_Requirement_Analysis/
    ├── 3_Project_Design/
    └── 8_Project_Demonstration/
```

## Features

* **Conversation Generation:** Creates tailored conversation starters from event descriptions and user interests.
* **Theme Extraction:** Uses DistilBERT zero-shot classification to identify event themes.
* **AI Text Generation:** Uses GPT-2 to generate conversation prompts.
* **Fact Checking:** Uses the Wikipedia API for quick fact lookups.
* **Conversation History:** Saves previous generations in local JSON files.
* **Feedback Tracking:** Records user feedback on generated conversation starters.

## Tech Stack

* Python
* FastAPI
* Streamlit
* DistilBERT
* GPT-2
* Wikipedia API
* Hugging Face Transformers
* JSON

## Setup

Requires Python 3.10 or later.

### 1. Create a virtual environment

```bash
python -m venv venv
```

### 2. Activate the virtual environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**

```cmd
venv\Scripts\activate
```

**Linux/macOS:**

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Add your real API keys to `.env` if required. Never commit secrets to GitHub. The `GEMINI_API_KEY` variable is available for a possible future integration with Gemini.

The first run may download DistilBERT and GPT-2 model weights from Hugging Face.

## Running Locally

Run both services from the project root.

**Terminal 1 — Backend:**

```powershell
python -m uvicorn backend.main:app --reload
```

API documentation: http://localhost:8000/docs

**Terminal 2 — Frontend:**

```powershell
python -m streamlit run frontend/ui.py
```

Application: http://localhost:8501

## API Endpoints

| Method | Endpoint                 | Description                                    |
| ------ | ------------------------ | ---------------------------------------------- |
| POST   | `/analyze-event`         | Extract themes from an event description       |
| POST   | `/generate-conversation` | Generate conversation starters and log history |
| GET    | `/history`               | Retrieve previous generations                  |
| POST   | `/feedback`              | Record feedback on a conversation starter      |
| POST   | `/fact-check`            | Perform a Wikipedia-backed fact lookup         |

## Running Tests

```powershell
pytest tests/test_main.py -v
```

## Known Limitations

* GPT-2 is a small, general-purpose language model, so generated results may be uneven.
* Local JSON files are intended for development and demonstration, not concurrent multi-user production.
* Model loading happens lazily on the first API request, which can make the first request slower.
* Generated conversation starters should be reviewed for relevance and quality.

## Future Improvements

* Improve conversation starter relevance and quality.
* Explore integration with larger language models.
* Improve scalability and data storage.
* Enhance personalization based on user preferences.
