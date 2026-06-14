# Stage 4B — Real AI Enablement

## Objective

Enable real AI Assist locally without committing secrets and without breaking fallback mode.

## Safety rules

- Never paste the API key into ChatGPT.
- Never hardcode the API key in source code.
- Never commit `.env`, `.env.local`, or any file containing secrets.
- Keep AI Assist optional. If the key is missing, Sentinel must still run.
- Deterministic Sentinel scoring remains the source of truth.

## What this step changes

This step may update:

```text
docker-compose.yml
.gitignore
```

It creates local-only:

```text
.env.local
```

The `.env.local` file is ignored and must not be committed.

## What this step does not do

- does not change scoring logic
- does not override findings
- does not require AI for normal reviews
- does not expose the key to frontend
- does not claim production AI maturity

## Required local variables

```text
AI_REVIEW_ENABLED=true
OPENAI_MODEL=<model available in your OpenAI account>
OPENAI_API_KEY=<your API key>
```

Use the model name available in your OpenAI account/project settings. If the selected model is unavailable, the app should fail safely and return fallback.

## Completion gate

Stage 4B is complete when:

- backend health works
- frontend loads
- AI fallback still works when disabled
- AI Assist returns real AI text when enabled with a valid key/model
- no secret files appear in `git status`
- changes are committed without secrets
