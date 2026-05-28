# Sentinel Stage 2 Backend DB Extraction
# Purpose:
#   Move DB_PATH, db(), and ensure_db() from backend/app/main.py
#   into backend/app/db/sqlite.py.
#
# Scope:
#   This script changes backend code.
#   It does not change frontend code.
#   It does not change API routes.
#   It creates a backup before modifying main.py.

$ErrorActionPreference = "Stop"

Write-Host "=== Sentinel Stage 2 Backend DB Extraction ===" -ForegroundColor Cyan

$project = "$HOME\Desktop\EyeOnBits-Sentinel"
$current = (Get-Location).Path

if ($current -ne $project) {
    Write-Host "You are not in the expected project folder." -ForegroundColor Red
    Write-Host "Current:  $current"
    Write-Host "Expected: $project"
    Write-Host "Run: cd `$HOME\Desktop\EyeOnBits-Sentinel"
    exit 1
}

$mainPath = Join-Path $project "backend\app\main.py"
$dbDir = Join-Path $project "backend\app\db"
$dbPath = Join-Path $dbDir "sqlite.py"
$dbInitPath = Join-Path $dbDir "__init__.py"

if (!(Test-Path $mainPath)) {
    Write-Host "main.py not found: $mainPath" -ForegroundColor Red
    exit 1
}

$raw = Get-Content $mainPath -Raw

if ($raw.Contains("from app.db.sqlite import db, ensure_db")) {
    Write-Host "DB extraction already appears to be applied. No changes made." -ForegroundColor Yellow
    exit 0
}

$dbPathStartMarker = "DB_PATH = Path(""data/sentinel.db"")"
$dbPathEndMarker = "app = FastAPI("
$dbFuncStartMarker = "def db():"
$dbFuncEndMarker = "@app.on_event(""startup"")"

$dbPathStart = $raw.IndexOf($dbPathStartMarker)
$dbPathEnd = $raw.IndexOf($dbPathEndMarker)
$dbFuncStart = $raw.IndexOf($dbFuncStartMarker)
$dbFuncEnd = $raw.IndexOf($dbFuncEndMarker)

if ($dbPathStart -lt 0 -or $dbPathEnd -lt 0 -or $dbFuncStart -lt 0 -or $dbFuncEnd -lt 0) {
    Write-Host "Required marker not found. No changes made." -ForegroundColor Red
    Write-Host "dbPathStart=$dbPathStart dbPathEnd=$dbPathEnd dbFuncStart=$dbFuncStart dbFuncEnd=$dbFuncEnd"
    exit 1
}

if (!($dbPathStart -lt $dbPathEnd -and $dbPathEnd -lt $dbFuncStart -and $dbFuncStart -lt $dbFuncEnd)) {
    Write-Host "Marker order is unexpected. No changes made." -ForegroundColor Red
    Write-Host "dbPathStart=$dbPathStart dbPathEnd=$dbPathEnd dbFuncStart=$dbFuncStart dbFuncEnd=$dbFuncEnd"
    exit 1
}

$dbPathBlock = $raw.Substring($dbPathStart, $dbPathEnd - $dbPathStart)
$dbFuncBlock = $raw.Substring($dbFuncStart, $dbFuncEnd - $dbFuncStart)

$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$backupPath = Join-Path $project "backend\app\main.py.stage2-db-backup-$timestamp"
Copy-Item $mainPath $backupPath -Force
Write-Host "Backup created:" -ForegroundColor Green
Write-Host $backupPath

New-Item -ItemType Directory -Path $dbDir -Force | Out-Null
if (!(Test-Path $dbInitPath)) {
    "" | Set-Content $dbInitPath -Encoding UTF8
}

$dbHeader = @"
from pathlib import Path
import sqlite3


"@

$dbContent = $dbHeader + $dbPathBlock.Trim() + "`n`n" + $dbFuncBlock.Trim() + "`n"
Set-Content -Path $dbPath -Value $dbContent -Encoding UTF8

$importBlock = "from app.db.sqlite import db, ensure_db`n"

$updated = $raw.Replace($dbPathBlock, "")
$updated = $updated.Replace($dbFuncBlock, "")

if ($updated.Contains("import uuid`r`n")) {
    $updated = $updated.Replace("import uuid`r`n", "import uuid`r`n" + $importBlock)
} elseif ($updated.Contains("import uuid`n")) {
    $updated = $updated.Replace("import uuid`n", "import uuid`n" + $importBlock)
} else {
    Write-Host "Could not find import uuid marker. Restoring backup." -ForegroundColor Red
    Copy-Item $backupPath $mainPath -Force
    Remove-Item $dbPath -Force
    exit 1
}

Set-Content -Path $mainPath -Value $updated -Encoding UTF8

Write-Host "Created:" -ForegroundColor Green
Write-Host $dbPath
Write-Host "Updated:" -ForegroundColor Green
Write-Host $mainPath

Write-Host "`nPost-extraction checks:" -ForegroundColor Cyan

$mainAfter = Get-Content $mainPath -Raw
$dbAfter = Get-Content $dbPath -Raw

if ($mainAfter.Contains("DB_PATH = Path(""data/sentinel.db"")")) {
    Write-Host "WARNING: DB_PATH definition still found in main.py" -ForegroundColor Yellow
} else {
    Write-Host "OK: DB_PATH moved out of main.py" -ForegroundColor Green
}

if ($mainAfter.Contains("def db():")) {
    Write-Host "WARNING: db() definition still found in main.py" -ForegroundColor Yellow
} else {
    Write-Host "OK: db() definition moved out of main.py" -ForegroundColor Green
}

if ($dbAfter.Contains("def db():") -and $dbAfter.Contains("def ensure_db():")) {
    Write-Host "OK: sqlite.py contains db() and ensure_db()" -ForegroundColor Green
} else {
    Write-Host "WARNING: sqlite.py may be incomplete" -ForegroundColor Yellow
}

Write-Host "`nOptional Python syntax check:" -ForegroundColor Cyan
try {
    python -m py_compile backend\app\main.py backend\app\db\sqlite.py
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Python syntax check passed." -ForegroundColor Green
    } else {
        Write-Host "Python syntax check failed. Review output above." -ForegroundColor Red
    }
} catch {
    Write-Host "Python command unavailable or failed. Docker build will validate." -ForegroundColor Yellow
}

Write-Host "`nNext:" -ForegroundColor Cyan
Write-Host "docker compose down --remove-orphans"
Write-Host "docker compose up --build"
