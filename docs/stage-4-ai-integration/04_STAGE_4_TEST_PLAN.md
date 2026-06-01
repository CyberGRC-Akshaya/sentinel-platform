# Stage 4 — AI Test Plan

## Backend health before AI

```powershell
docker compose down --remove-orphans
docker compose up --build
```

Open:

```text
http://localhost:8000/api/health
```

## Test mode 1 — AI disabled

Expected:

- normal review works
- AI endpoint returns disabled/fallback
- no crash

## Test mode 2 — AI enabled without key

Expected:

- normal review works
- AI endpoint returns configuration required message
- no crash

## Test mode 3 — AI enabled with key

Expected:

- normal review works
- AI endpoint returns AI narrative
- no secrets printed
- no frontend crash

## Manual UI checks after frontend AI button later

- Run + Save Review
- AI Assist Review
- Evidence Requests
- Board Pack
- Final Room
- Exports
