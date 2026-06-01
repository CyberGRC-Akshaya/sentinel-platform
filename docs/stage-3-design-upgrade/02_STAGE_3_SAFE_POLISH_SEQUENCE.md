# Stage 3 — Safe Polish Sequence

## Sequence

Do not polish randomly.

### Step 1 — Inventory current CSS

Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\stage-3\stage-3-ui-inventory.ps1
```

### Step 2 — Identify CSS-only improvements

Start with `frontend/app/globals.css`.

Do not touch `page.tsx` unless needed.

### Step 3 — Apply only one visual group at a time

Recommended order:

| Order | Area |
|---:|---|
| 1 | body/background/page shell |
| 2 | cards/panels |
| 3 | buttons |
| 4 | tabs/navigation |
| 5 | text hierarchy |
| 6 | tables/outputs |
| 7 | responsive fixes |

### Step 4 — Test after each group

```powershell
docker compose down --remove-orphans
docker compose up --build
```

### Step 5 — Commit after stable visual pass

```powershell
git add frontend/app/globals.css frontend/app/page.tsx docs scripts
git commit -m "Polish Stage 3 visual baseline"
git push
```

## Do not

- paste a full CSS reset blindly
- change class names unless necessary
- delete existing classes aggressively
- modify JSX structure before CSS inventory
