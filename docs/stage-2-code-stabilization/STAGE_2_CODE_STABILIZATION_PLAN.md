# Stage 2 — Code Stabilization Plan

## Objective

Clean and harden the current Sentinel codebase before moving to Stage 3 Design Upgrade.

Stage 2 is not for new features.

Stage 2 is for reliability, maintainability, repeatable startup, safer refactoring, and predictable GitHub history.

## Current baseline

| Item | Baseline |
|---|---|
| Product | Sentinel Evidence Defensibility Workbench |
| Project folder | `C:\Users\Akshaya\Desktop\EyeOnBits-Sentinel` |
| Frontend | Next.js |
| Backend | FastAPI |
| Runtime | Docker Compose |
| Current stable hotfix target | `10.1.1` backend health expected |
| Stage status | Stage 2 starting |

## Stage 2 principles

1. No new product features.
2. No new major tabs.
3. No large refactor without backup.
4. No code patch without running smoke test.
5. Every change must be committed in small Git commits.
6. All work must preserve the current working product behavior.
7. If a refactor breaks the app, revert immediately and split the change smaller.

## Workstreams

| Workstream | Goal |
|---|---|
| Baseline backup | Preserve current working state before refactor |
| Git branch | Create `stage-2-code-stabilization` branch |
| Frontend cleanup | Split risky large `page.tsx` into maintainable components |
| Backend cleanup | Separate scoring, routes, reports, vault logic |
| Docker reliability | Ensure repeatable local startup |
| Test scripts | Add preflight and health check scripts |
| Documentation | Keep runbook aligned with actual commands |
| Issue tracking | Track bugs in known issues register |

## Stage 2 exit criteria

| Gate | Required condition |
|---|---|
| 1 | Docker build starts cleanly |
| 2 | Backend health endpoint returns expected version |
| 3 | Frontend loads without compile/runtime error |
| 4 | All major tabs load |
| 5 | Run + Save Review works |
| 6 | Vault reload works |
| 7 | Key exports work |
| 8 | Code structure is easier to understand |
| 9 | GitHub branch and tag are clean |
| 10 | Stage 3 Design Upgrade can start safely |
