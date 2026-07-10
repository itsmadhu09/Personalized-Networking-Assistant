# 8. Project Demonstration — Demo Planning & Scalability

## Demo Script (suggested flow, ~5–7 min)

1. **Intro (30s)** — State the problem: networking small-talk anxiety, unfamiliar event topics.
2. **Live Generate demo (2 min)**
   - Input: `"AI for Sustainable Cities"`, interests: `climate change, urban planning`
   - Show detected themes appearing
   - Show 2–3 generated conversation starters
   - Click 👍 on one starter to show feedback logging
3. **Fact Check demo (1 min)**
   - Query: `"blockchain in healthcare"`
   - Show summary + Wikipedia source link
4. **History demo (1 min)**
   - Switch to History tab, show the entry just created, expand it
5. **Architecture walkthrough (1–2 min)**
   - Briefly show `backend/main.py`, point out the 3 AI service files, mention Swagger docs at `/docs`
6. **Wrap-up (30s)** — Mention known limitations + what you'd improve with more time (see below).

## Pre-Demo Checklist

- [ ] `data/history.json` reset to `[]` (or pre-seeded with 2–3 clean example entries)
- [ ] Backend running (`uvicorn backend.main:app --reload`) and warmed up — send one throwaway request first so model load time doesn't happen live
- [ ] Frontend running (`streamlit run frontend/ui.py`)
- [ ] `.env` filled in if using Gemini API as a fallback/enhancement
- [ ] Swagger UI (`/docs`) open in a second tab as backup if the Streamlit UI has issues

## Known Limitations (be upfront about these)

- GPT-2 is small and general-purpose; starter quality is decent but not GPT-4-level polish
- No authentication/multi-user support — single local user only
- Wikipedia fact-check depends on exact/close page-title matches; obscure topics may return "not found"

## Scalability Plan (what's next)

| Area | Current state | Scale-up path |
|---|---|---|
| Storage | Flat JSON files | Migrate to SQLite → PostgreSQL for concurrent users |
| Generation model | GPT-2 (local, free) | Swap in Gemini API / GPT-4 via API for higher-quality starters |
| Deployment | Local (`localhost`) | Containerize with Docker; deploy backend to Cloud Run, frontend to Streamlit Community Cloud |
| Auth | None | Add user accounts so history/feedback are per-user, not global |
| Theme labels | Fixed candidate list | Make dynamic/configurable, or fine-tune a classifier on real event data |

---
*Fill in actual presenter name(s) and rehearsal date before submission.*
