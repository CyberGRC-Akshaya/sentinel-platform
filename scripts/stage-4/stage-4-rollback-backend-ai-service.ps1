# Sentinel Stage 4 Backend AI Service Rollback
$ErrorActionPreference = "Stop"

$project = "$HOME\Desktop\EyeOnBits-Sentinel"
cd $project

$backup = Get-ChildItem "backend\app" -Filter "main.py.stage4-ai-backup-*" | Sort-Object LastWriteTime -Descending | Select-Object -First 1

if ($null -eq $backup) {
    Write-Host "No Stage 4 AI backup found." -ForegroundColor Red
    exit 1
}

Copy-Item $backup.FullName "backend\app\main.py" -Force

if (Test-Path "backend\app\services\ai_review.py") {
    Remove-Item "backend\app\services\ai_review.py" -Force
}

Write-Host "Rollback complete." -ForegroundColor Green
Write-Host "Restored from:"
Write-Host $backup.FullName
Write-Host "Note: requirements.txt and .env.example may still contain AI lines; remove manually only if needed."
