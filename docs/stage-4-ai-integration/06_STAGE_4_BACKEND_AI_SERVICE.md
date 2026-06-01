# Stage 4 — Backend AI Service

## What this step adds

This step adds a fallback-safe backend AI Assist service.

## Files created

```text
backend/app/services/ai_review.py
```

## Files updated

```text
backend/app/main.py
backend/requirements.txt
.env.example
```

## Endpoint added

```text
POST /api/ai/assist-review
```

## Safety design

- AI disabled by default
- no API key committed
- app works without AI
- OpenAI package imported lazily
- AI failure returns fallback, not crash
- human review required in response

## Environment configuration

```text
AI_REVIEW_ENABLED=false
OPENAI_MODEL=gpt-5.5
OPENAI_API_KEY=
```

## Test fallback mode

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\stage-4\stage-4-test-ai-endpoint.ps1
```

Expected status:

```text
fallback
```

## Enable real AI later

Set these in your local environment only, not in Git:

```powershell
$env:AI_REVIEW_ENABLED="true"
$env:OPENAI_API_KEY="your-key-here"
```

Then restart Docker with environment passed appropriately later.
