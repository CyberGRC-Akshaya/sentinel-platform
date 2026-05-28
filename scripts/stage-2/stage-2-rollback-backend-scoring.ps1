# Sentinel Stage 2 Backend Scoring Extraction Rollback
$ErrorActionPreference = "Stop"

$project = "$HOME\Desktop\EyeOnBits-Sentinel"
cd $project

$backup = Get-ChildItem "backend\app" -Filter "main.py.stage2-scoring-backup-*" | Sort-Object LastWriteTime -Descending | Select-Object -First 1

if ($null -eq $backup) {
    Write-Host "No Stage 2 scoring backup found." -ForegroundColor Red
    exit 1
}

Copy-Item $backup.FullName "backend\app\main.py" -Force

if (Test-Path "backend\app\services\scoring.py") {
    Remove-Item "backend\app\services\scoring.py" -Force
}

Write-Host "Rollback complete." -ForegroundColor Green
Write-Host "Restored from:"
Write-Host $backup.FullName
