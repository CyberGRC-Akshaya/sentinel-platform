# Stage 4 — Real AI Integration Plan

## Objective

Add real OpenAI-assisted evidence reasoning without replacing the deterministic rule engine.

## Design rule

Rule engine remains default. AI is optional.

If no API key is present, Sentinel must still work.

## AI capabilities

- evidence narrative enhancement
- evidence request drafting
- board summary drafting
- control challenge question generation
- prompt logging

## Required safety boundaries

- no autonomous decisions
- no claim of regulatory advice
- human review required
- prompt and response logs retained
- API key stored in environment variable only
