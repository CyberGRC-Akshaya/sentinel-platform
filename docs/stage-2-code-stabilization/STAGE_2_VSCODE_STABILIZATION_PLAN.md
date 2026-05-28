# Stage 2 — Code Stabilization Using VS Code + ChatGPT

## Decision

Cursor is optional and will not be used as a dependency.

Stage 2 will proceed using:

- VS Code
- ChatGPT
- GitHub
- Docker
- PowerShell
- Manual controlled edits

## Objective

Stabilize the current Sentinel codebase without adding features.

## Current project folder

```text
C:\Users\Akshaya\Desktop\EyeOnBits-Sentinel
```

This is the only project folder to preserve.

## Stage 2 rule

No new tabs.  
No new features.  
No AI integration.  
No design overhaul.  
No deployment work.

Only stabilization.

## Working method

1. Open project in VS Code.
2. Run preflight checks.
3. Create backup.
4. Create Stage 2 branch.
5. Review risky files.
6. Refactor only one small section at a time.
7. Run Docker build after every change.
8. Commit only working changes.

## Current high-risk files

| File | Risk | Stabilization approach |
|---|---|---|
| `frontend/app/page.tsx` | Too large, easy to break JSX | Split gradually, one section at a time |
| `frontend/app/globals.css` | Patch CSS may conflict | Clean only after UI is stable |
| `backend/app/main.py` | Too many routes/functions | Extract pure functions first |
| `docker-compose.yml` | Runtime dependency | Do not change unless required |
| `README.md` | May not match current runtime | Keep aligned with real commands |

## Exit criteria

Stage 2 is complete only when:

- app starts cleanly
- backend health works
- frontend loads
- all key tabs load
- Run + Save Review works
- exports work
- code is easier to maintain
- Git branch is clean
- no known blocking issues remain
