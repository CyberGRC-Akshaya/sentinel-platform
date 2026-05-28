# Stage 2 — Backend Scoring Extraction

## Objective

Move scoring constants, `EvidenceItem`, and pure scoring helper functions out of:

```text
backend/app/main.py
```

into:

```text
backend/app/services/scoring.py
```

## Why this bundle is required

The helper functions depend on:

- `EvidenceItem`
- `CONTROL_ATLAS`
- `FRAMEWORK_LIBRARY`
- `DIMENSIONS`
- `INTAKE_REQUIREMENTS`
- `DOMAIN_KEYWORDS`

Moving only helper functions would break imports. This extraction moves the dependency bundle together.

## Apply from project folder

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\stage-2\stage-2-extract-backend-scoring.ps1
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

Run one sample review.

## Rollback if needed

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\stage-2\stage-2-rollback-backend-scoring.ps1
```

## Commit if working

```powershell
git add backend/app/main.py backend/app/services scripts/stage-2 docs/stage-2-code-stabilization
git commit -m "Extract backend scoring helpers into service module"
git push
```
