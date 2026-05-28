# Stage 2 First Tasks

## Task 1 — Apply this pack

Apply `sentinel-stage-2-vscode-stabilization-pack`.

## Task 2 — Open VS Code

Open folder:

```text
C:\Users\Akshaya\Desktop\EyeOnBits-Sentinel
```

## Task 3 — Run preflight

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\stage-2\stage-2-vscode-preflight.ps1
```

## Task 4 — Create backup

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\stage-2\stage-2-create-backup.ps1
```

## Task 5 — Run app

```powershell
docker compose down --remove-orphans
docker compose up --build
```

## Task 6 — Health check

Open another terminal:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\stage-2\stage-2-health-check.ps1
```

## Task 7 — Do not refactor yet

After preflight and backup, share:
- preflight output
- health check result
- whether app loads

Then we decide the first safe file to clean.
