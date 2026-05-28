# Sentinel Stage 2 Backend DB Extraction Rollback
$ErrorActionPreference = "Stop"

$project = "$HOME\Desktop\EyeOnBits-Sentinel"
cd $project

$backup = Get-ChildItem "backend\app" -Filter "main.py.stage2-db-backup-*" | Sort-Object LastWriteTime -Descending | Select-Object -First 1

if ($null -eq $backup) {
    Write-Host "No Stage 2 DB backup found." -ForegroundColor Red
    exit 1
}

Copy-Item $backup.FullName "backend\app\main.py" -Force

if (Test-Path "backend\app\db\sqlite.py") {
    Remove-Item "backend\app\db\sqlite.py" -Force
}

Write-Host "Rollback complete." -ForegroundColor Green
Write-Host "Restored from:"
Write-Host $backup.FullName
