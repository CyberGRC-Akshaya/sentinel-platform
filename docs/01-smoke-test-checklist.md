# Sentinel Smoke Test Checklist

## Start app

```powershell
cd $HOME\Desktop\EyeOnBits-Sentinel
docker compose down --remove-orphans
docker compose up --build
```

Open:

```text
http://localhost:3000
http://localhost:8000/api/health
```

Expected backend:

```json
"version": "10.1.1"
```

Hard refresh browser:

```text
Ctrl + Shift + R
```

## Smoke tests

| # | Test | Expected |
|---|---|---|
| 1 | Final Room | Loads |
| 2 | Launch Room | Loads |
| 3 | Review input | Sample JSON visible |
| 4 | Run + Save Review | Review generated |
| 5 | Review Vault | Saved review appears |
| 6 | Demo Room | Loads narrative |
| 7 | Delivery Kit | Shows readiness/checklist |
| 8 | Portfolio | Loads portfolio summary |
| 9 | Board Pack | Loads executive narrative |
| 10 | Evidence Requests | Loads request-ready asks |
| 11 | Command Center | Register fields editable |
| 12 | Control Atlas | Control mappings visible |
| 13 | HTML export | Downloads |
| 14 | CSV export | Downloads |
| 15 | Vault Backup | Downloads |
