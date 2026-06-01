# Stage 2 — Code Stabilization Exit Checklist

## Required gates

| Gate | Required Result | Status |
|---|---|---|
| Git branch | `stage-2-code-stabilization` active or merged | Pending |
| Runtime DB excluded from Git | `backend/data/*.db` ignored | Pending |
| Frontend helper refactor | Download helpers refactored and committed | Pending |
| Backend scoring extraction | `backend/app/services/scoring.py` working | Pending |
| Backend DB extraction | `backend/app/db/sqlite.py` working | Pending |
| Docker build | `docker compose up --build` works | Pending |
| Backend health | `/api/health` returns `10.1.1` | Pending |
| Frontend | `localhost:3000` opens | Pending |
| Review flow | Run + Save Review to Vault works | Pending |
| Vault | Saved reviews load | Pending |
| Exports | JSON, CSV, HTML downloads work | Pending |
| Git | working tree clean | Pending |

## Stage 2 exit command sequence

```powershell
cd $HOME\Desktop\EyeOnBits-Sentinel
git status
docker compose down --remove-orphans
docker compose up --build
```

Open:

```text
http://localhost:8000/api/health
http://localhost:3000
```
