# 1. Brainstorming & Ideation

## Problem Statement

*Fill in: What networking pain point does this solve, and for whom?*

> Attendees at conferences and professional events often struggle to start
> meaningful conversations with strangers, especially when the event covers
> unfamiliar or highly technical topics. Existing note-taking or event apps
> don't offer personalized, context-aware conversation guidance.

## Target Users

- Conference / meetup attendees
- Students at career fairs
- Professionals attending unfamiliar-industry events

## Empathy Map

| Quadrant | Notes |
|---|---|
| **Says** | "I never know what to say when I walk up to someone." |
| **Thinks** | "I hope I don't sound uninformed about this topic." |
| **Does** | Scrolls LinkedIn/event agenda right before approaching people |
| **Feels** | Anxious, underprepared, worried about small talk running dry |

## Why This Solution

- DistilBERT theme extraction removes the need to manually re-read event descriptions
- GPT-2 generated starters reduce the "blank page" problem of small talk
- Wikipedia fact-check gives a confidence boost on unfamiliar topics
- History + feedback loop lets the tool improve to the user's style over time

## Alternatives Considered

*Fill in: what did the team consider and reject, and why?*
- e.g. Rule-based/template-only starters (rejected: too generic, no personalization)
- e.g. Full LLM API (GPT-4/Gemini) only (rejected/deferred: cost, offline dev speed — GPT-2 chosen for local, free iteration)

---
*Team: fill in date, and who led this ideation session.*
