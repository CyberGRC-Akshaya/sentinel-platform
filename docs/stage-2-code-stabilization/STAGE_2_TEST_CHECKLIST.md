# Stage 2 Test Checklist

## Before testing

Open Docker Desktop and wait until it is ready.

Open PowerShell in:

```text
C:\Users\Akshaya\Desktop\EyeOnBits-Sentinel
```

Run:

```powershell
docker compose down --remove-orphans
docker compose up --build
```

## Backend checks

Open:

```text
http://localhost:8000/api/health
```

Expected:

```json
"version": "10.1.1"
```

## Frontend checks

Open:

```text
http://localhost:3000
```

Hard refresh:

```text
Ctrl + Shift + R
```

## UI smoke checklist

| # | Check | Expected |
|---|---|---|
| 1 | Final Room loads | No crash |
| 2 | Launch Room loads | No crash |
| 3 | Demo Room loads | No crash |
| 4 | Delivery Kit loads | No crash |
| 5 | Portfolio loads | No crash |
| 6 | Board Pack loads | No crash |
| 7 | Evidence Requests loads | No crash |
| 8 | Command Center loads | No crash |
| 9 | Control Atlas loads | No crash |
| 10 | Review input visible | Sample JSON appears |
| 11 | Run + Save Review | Output generated |
| 12 | Review Vault | Saved review visible |
| 13 | Reload saved review | Review reloads |
| 14 | Register CSV | Downloads |
| 15 | HTML report | Downloads |

## Failure rule

If a refactor breaks the app:

1. Stop.
2. Do not add new changes.
3. Capture error.
4. Revert last commit if needed.
5. Retry smaller.
