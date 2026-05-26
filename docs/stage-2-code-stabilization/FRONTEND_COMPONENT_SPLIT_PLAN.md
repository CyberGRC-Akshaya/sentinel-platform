# Frontend Component Split Plan

## Objective

Reduce the risk caused by a large `frontend/app/page.tsx`.

## Rule

Do not rewrite the UI in one attempt.

Move one component at a time and test after every move.

## Proposed component extraction order

| Order | Component | Source responsibility |
|---|---|---|
| 1 | `TabBar.tsx` | Active tab buttons |
| 2 | `Hero.tsx` | Header/positioning section |
| 3 | `ReviewInput.tsx` | Evidence input and case selection |
| 4 | `OutputPanel.tsx` | Score/finding output display |
| 5 | `ControlAtlas.tsx` | Control mapping tab |
| 6 | `EvidenceRequests.tsx` | Evidence request workflow |
| 7 | `BoardPack.tsx` | Board pack tab |
| 8 | `DeliveryKit.tsx` | Delivery kit tab |
| 9 | `DemoRoom.tsx` | Demo room tab |
| 10 | `FinalRoom.tsx` | Final room tab |
| 11 | `LaunchRoom.tsx` | Launch room tab |
| 12 | `CommandCenter.tsx` | Remediation register |
| 13 | `Portfolio.tsx` | Portfolio analytics |

## Test after each extraction

```powershell
docker compose down --remove-orphans
docker compose up --build
```

Then open:

```text
http://localhost:3000
```

## Cursor instruction

Cursor must not redesign the app during Stage 2. It should only extract components while preserving visual behavior.
