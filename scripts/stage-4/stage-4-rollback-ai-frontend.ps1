# Sentinel Stage 4 AI Frontend Integration Rollback
$ErrorActionPreference = "Stop"

$project = "$HOME\Desktop\EyeOnBits-Sentinel"
cd $project

$backup = Get-ChildItem "frontend\app" -Filter "page.tsx.stage4-ai-frontend-backup-*" | Sort-Object LastWriteTime -Descending | Select-Object -First 1

if ($null -eq $backup) {
    Write-Host "No Stage 4 AI frontend backup found." -ForegroundColor Red
    exit 1
}

Copy-Item $backup.FullName "frontend\app\page.tsx" -Force
Write-Host "Rollback complete for page.tsx." -ForegroundColor Green
Write-Host "Restored from:"
Write-Host $backup.FullName
Write-Host "Note: AI CSS block may remain in globals.css. It is harmless, but can be removed manually if required."
