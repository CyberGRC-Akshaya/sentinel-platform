# Sentinel Stage 2 VS Code Preflight Check
$ErrorActionPreference = "Continue"

Write-Host "=== Sentinel Stage 2 VS Code Preflight ===" -ForegroundColor Cyan

$project = "$HOME\Desktop\EyeOnBits-Sentinel"
$current = (Get-Location).Path

Write-Host "`nExpected project folder:"
Write-Host $project

Write-Host "`nCurrent folder:"
Write-Host $current

if ($current -ne $project) {
    Write-Host "`nWARNING: You are not in the expected project folder." -ForegroundColor Yellow
    Write-Host "Run this:" -ForegroundColor Yellow
    Write-Host "cd `$HOME\Desktop\EyeOnBits-Sentinel"
} else {
    Write-Host "`nFolder check passed." -ForegroundColor Green
}

Write-Host "`nChecking key files..."
$required = @(
    "docker-compose.yml",
    "backend\app\main.py",
    "backend\requirements.txt",
    "frontend\app\page.tsx",
    "frontend\app\globals.css",
    "frontend\package.json",
    "README.md"
)

foreach ($file in $required) {
    if (Test-Path $file) {
        Write-Host "OK: $file" -ForegroundColor Green
    } else {
        Write-Host "MISSING: $file" -ForegroundColor Red
    }
}

Write-Host "`nGit version:"
git --version

Write-Host "`nGit status:"
git status --short

Write-Host "`nDocker version:"
docker --version

Write-Host "`nDocker Compose version:"
docker compose version

Write-Host "`nDocker Compose config validation:"
docker compose config | Out-Null
if ($LASTEXITCODE -eq 0) {
    Write-Host "Docker compose config OK." -ForegroundColor Green
} else {
    Write-Host "Docker compose config has an issue." -ForegroundColor Red
}

Write-Host "`nPreflight completed."
