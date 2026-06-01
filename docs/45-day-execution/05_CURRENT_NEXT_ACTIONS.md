# Current Next Actions

## Current stage

Stage 2 — Code Stabilization

## Immediate task

Confirm backend DB extraction result.

Send status:

```text
DB extraction: worked / failed
Backend health: worked / failed
Frontend: worked / failed
Run + Save Review: worked / failed
Git commit: done / not done
```

## If DB extraction works

Commit:

```powershell
git add backend/app/main.py backend/app/db scripts/stage-2 docs/stage-2-code-stabilization
git commit -m "Extract backend database helpers into db module"
git push
```

Then tag Stage 2 stable baseline after full smoke test.

## If DB extraction fails

Rollback:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\stage-2\stage-2-rollback-backend-db.ps1
```
