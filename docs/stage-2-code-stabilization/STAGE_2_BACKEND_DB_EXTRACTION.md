# Stage 2 — Backend DB Extraction

## Objective

Move database path and DB connection helpers out of:

```text
backend/app/main.py
```

into:

```text
backend/app/db/sqlite.py
```

## What moves

- `DB_PATH`
- `DB_PATH.parent.mkdir(...)`
- `db()`
- `ensure_db()`

## What stays in main.py

- FastAPI app initialization
- middleware
- startup event
- routes
- review logic
- portfolio logic
- report logic

## Why this is a safe Stage 2 step

The DB helpers are isolated infrastructure helpers. Moving them reduces `main.py` size without changing route behavior or response shape.

## Apply from project folder

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\stage-2\stage-2-extract-backend-db.ps1
```

## Test

```powershell
docker compose down --remove-orphans
docker compose up --build
```

Open:

```text
http://localhost:8000/api/health
http://localhost:3000
```

Run one saved review.

## Rollback if needed

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\stage-2\stage-2-rollback-backend-db.ps1
```

## Commit if working

```powershell
git add backend/app/main.py backend/app/db scripts/stage-2 docs/stage-2-code-stabilization
git commit -m "Extract backend database helpers into db module"
git push
```
