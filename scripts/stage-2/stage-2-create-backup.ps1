# Sentinel Stage 2 Backup Script
$ErrorActionPreference = "Stop"

$project = "$HOME\Desktop\EyeOnBits-Sentinel"
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$backupRoot = "$HOME\Desktop\Sentinel-Backups"
$backupFile = Join-Path $backupRoot "EyeOnBits-Sentinel-stage2-backup-$timestamp.zip"

if (!(Test-Path $project)) {
    Write-Host "Project folder not found: $project" -ForegroundColor Red
    exit 1
}

New-Item -ItemType Directory -Path $backupRoot -Force | Out-Null

Write-Host "Creating backup:" -ForegroundColor Cyan
Write-Host $backupFile

$temp = Join-Path $env:TEMP "sentinel-backup-$timestamp"
if (Test-Path $temp) { Remove-Item $temp -Recurse -Force }
New-Item -ItemType Directory -Path $temp | Out-Null

robocopy $project $temp /E /XD node_modules .next __pycache__ .venv venv /XF "*.pyc" | Out-Null

Compress-Archive -Path (Join-Path $temp "*") -DestinationPath $backupFile -Force

Remove-Item $temp -Recurse -Force

Write-Host "Backup created successfully." -ForegroundColor Green
Write-Host $backupFile
