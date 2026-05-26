# Codebase Refactor Map

## Purpose

This map identifies where the current prototype is fragile and how to stabilize it safely.

## Current likely structure

```text
EyeOnBits-Sentinel/
  backend/
    app/
      main.py
    requirements.txt
    Dockerfile
  frontend/
    app/
      page.tsx
      layout.tsx
      globals.css
    package.json
    Dockerfile
  docker-compose.yml
  README.md
  docs/
  sample-data/
```

## Primary stabilization risk

| Area | Risk |
|---|---|
| `frontend/app/page.tsx` | Too much logic and JSX in one file; high risk of syntax break |
| `frontend/app/globals.css` | Repeated patch CSS can create conflicting layout rules |
| `backend/app/main.py` | Too many routes, scoring functions, report generators, DB logic in one file |
| version naming | v10 docs, v10.1.1 health, v10.4 launch assets may confuse repo readers |
| scripts | Need stable run/test scripts |

## Target structure after Stage 2

```text
backend/
  app/
    main.py
    routes/
      health.py
      reviews.py
      portfolio.py
      exports.py
      product.py
    services/
      scoring.py
      control_atlas.py
      evidence_requests.py
      board_pack.py
      demo_room.py
      vault.py
    models/
      schemas.py
    db/
      sqlite.py

frontend/
  app/
    page.tsx
    layout.tsx
    globals.css
  components/
    Shell.tsx
    Hero.tsx
    TabBar.tsx
    ReviewInput.tsx
    OutputPanel.tsx
    FinalRoom.tsx
    LaunchRoom.tsx
    DemoRoom.tsx
    DeliveryKit.tsx
    Portfolio.tsx
    BoardPack.tsx
    EvidenceRequests.tsx
    CommandCenter.tsx
    ControlAtlas.tsx
  lib/
    api.ts
    downloads.ts
    sampleCases.ts
```

## Safe refactor order

| Order | Area | Why |
|---|---|---|
| 1 | Create backup and branch | Prevent loss |
| 2 | Add preflight scripts | Validate environment |
| 3 | Split frontend utility functions | Low visual risk |
| 4 | Split frontend display components one by one | Avoid JSX mass break |
| 5 | Split backend pure functions | Easier to test |
| 6 | Split backend routes | Higher risk; do after functions |
| 7 | Clean CSS | After components are stable |
| 8 | Update README/runbook | Reflect stabilized structure |
