# Cursor Prompt — Frontend Safe Refactor

You are refactoring Sentinel frontend during Stage 2 Code Stabilization.

Rules:
- Do not change visual design.
- Do not add features.
- Do not remove functionality.
- Preserve current behavior.
- Extract one component at a time.
- Keep TypeScript valid.
- After each change, explain files changed and test command.

Task:
Start by extracting the TabBar or another low-risk UI section from `frontend/app/page.tsx` into a component under `frontend/components/`.

After the extraction:
- update imports
- keep props simple
- ensure page.tsx compiles
- do not modify backend
- do not redesign CSS

Test command:
docker compose down --remove-orphans
docker compose up --build
