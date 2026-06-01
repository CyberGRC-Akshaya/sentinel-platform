# Stage 4 — Real AI Integration Control Plan

## Objective

Add a real AI-assisted review layer to Sentinel without breaking the deterministic rule engine.

## Non-negotiable design rule

The rule engine remains the default system of record.

AI is optional, additive, and review-assistive.

If no API key exists, Sentinel must still run normally.

## Stage 4 completion definition

Stage 4 is complete when Sentinel can:

- run the existing rule-based evidence review normally
- optionally generate AI-assisted review narrative
- optionally draft evidence requests
- optionally improve executive summary language
- log prompt/response metadata for traceability
- fail gracefully if AI is disabled or unavailable

## What AI may do

| AI capability | Allowed use |
|---|---|
| Executive summary enhancement | Improve narrative clarity |
| Finding narrative drafting | Convert scored findings into professional language |
| Evidence request drafting | Draft owner-ready requests |
| Control challenge questions | Add reviewer-style follow-up questions |
| Board summary drafting | Create senior-management narrative |

## What AI must not do

- make final risk decisions
- override deterministic scores automatically
- claim regulatory approval
- claim audit reliance
- change stored evidence without user action
- process real client confidential data during early testing
- run if API key is absent without fallback

## Stage 4 technical direction

Backend additions:

```text
backend/app/services/ai_review.py
backend/app/routes/ai.py
```

Configuration:

```text
OPENAI_API_KEY=
AI_REVIEW_ENABLED=false
OPENAI_MODEL=
```

Frontend addition later:

```text
AI Assist Review
```

But do not touch frontend until backend is stable.
