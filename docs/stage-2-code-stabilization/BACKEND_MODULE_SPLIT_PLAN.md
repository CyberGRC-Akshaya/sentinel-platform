# Backend Module Split Plan

## Objective

Reduce risk in `backend/app/main.py` by separating concerns.

## Rule

Move pure functions first. Move routes later.

## Proposed extraction order

| Order | Module | Move |
|---|---|---|
| 1 | `services/scoring.py` | Scoring functions and severity logic |
| 2 | `services/control_atlas.py` | Control mapping logic |
| 3 | `services/evidence_requests.py` | Evidence request and closure readiness functions |
| 4 | `services/board_pack.py` | Board pack JSON/HTML generation |
| 5 | `services/demo_room.py` | Demo room manifest/report logic |
| 6 | `services/vault.py` | Save/load review vault logic |
| 7 | `db/sqlite.py` | DB connection and initialization |
| 8 | `routes/reviews.py` | Review endpoints |
| 9 | `routes/portfolio.py` | Portfolio endpoints |
| 10 | `routes/product.py` | Product/final release endpoints |

## Backend test after each extraction

```powershell
docker compose down --remove-orphans
docker compose up --build
```

Open:

```text
http://localhost:8000/api/health
```

Then run a review from UI.
