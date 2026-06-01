# Stage 4 — AI Frontend Integration

## What this step adds

- AI Assist Review button
- AI-assisted output panel
- AI fallback display
- human-review warning text

## What this step does not do

- does not add new tab
- does not override scoring
- does not require API key
- does not change backend scoring
- does not store secrets in frontend

## Manual browser test

1. Run or load a saved review.
2. Click `AI Assist Review`.
3. If AI is disabled, fallback panel should appear.
4. Existing deterministic outputs must remain unchanged.
5. Export buttons must still work.

## Commit if working

```powershell
git add frontend/app/page.tsx frontend/app/globals.css scripts/stage-4 docs/stage-4-ai-integration
git commit -m "Add frontend AI assist review panel"
git push
```

## Rollback if broken

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\stage-4\stage-4-rollback-ai-frontend.ps1
```
