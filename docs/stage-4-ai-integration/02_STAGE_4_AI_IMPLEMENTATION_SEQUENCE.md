# Stage 4 — AI Implementation Sequence

## Safe sequence

### Step 1 — AI inventory

Inspect current backend and frontend before changes.

### Step 2 — Add environment template

Add `.env.example` entries for AI configuration.

### Step 3 — Add backend AI service

Create `backend/app/services/ai_review.py`.

This service must:

- check whether AI is enabled
- check whether API key exists
- prepare controlled prompt
- call OpenAI only if configured
- return fallback response if unavailable

### Step 4 — Add backend AI route

Create AI route only after service works.

### Step 5 — Test backend only

Do not touch frontend yet.

### Step 6 — Add frontend AI Assist button

Only after backend route works.

### Step 7 — Add prompt log

Add basic prompt log structure.

## Testing requirements

Test three states:

| State | Expected behavior |
|---|---|
| AI disabled | App works; AI endpoint returns disabled/fallback |
| AI enabled but no key | App works; AI endpoint returns clear configuration message |
| AI enabled with key | AI response generated |

## Commit strategy

| Commit | Purpose |
|---|---|
| Commit 1 | Stage 4 docs/inventory |
| Commit 2 | AI config and backend service |
| Commit 3 | AI route |
| Commit 4 | Frontend AI Assist |
| Commit 5 | Prompt logging and final smoke test |
