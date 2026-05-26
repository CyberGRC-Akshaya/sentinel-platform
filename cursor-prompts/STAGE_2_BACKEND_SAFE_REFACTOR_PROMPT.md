# Cursor Prompt — Backend Safe Refactor

You are refactoring Sentinel backend during Stage 2 Code Stabilization.

Rules:
- Do not change API behavior.
- Do not add new product features.
- Do not remove existing endpoints.
- Move pure functions first.
- Keep FastAPI app working.
- Explain every file changed.

Task:
Review `backend/app/main.py` and identify a safe pure-function group to move into `backend/app/services/`.

Recommended first target:
- scoring logic
- control atlas mapping
- evidence request logic

After moving:
- update imports
- keep endpoint responses unchanged
- test backend health
- test one review from the frontend

Test command:
docker compose down --remove-orphans
docker compose up --build
