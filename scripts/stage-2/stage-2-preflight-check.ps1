# Sentinel Stage 2 Preflight Check
$ErrorActionPreference = "Continue"

Write-Host "=== Sentinel Stage 2 Preflight Check ===" -ForegroundColor Cyan

$expected = "$HOME\Desktop\EyeOnBits-Sentinel"
$current = (Get-Location).Path

Write-Host "Current folder: $current"

if ($current -ne $expected) {
    Write-Host "WARNING: You are not in expected folder: $expected" -ForegroundColor Yellow
    Write-Host "Run: cd `$HOME\Desktop\EyeOnBits-Sentinel" -ForegroundColor Yellow
} else {
    Write-Host "Folder check passed." -ForegroundColor Green
}

Write-Host "`nChecking required files..."
$required = @(
    "docker-compose.yml",
    "backend\app\main.py",
    "frontend\app\page.tsx",
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

Write-Host "`nChecking Git..."
git --version
git status --short

Write-Host "`nChecking Docker..."
docker --version
docker compose version

Write-Host "`nValidating docker compose config..."
docker compose config | Out-Null
if ($LASTEXITCODE -eq 0) {
    Write-Host "Docker compose config OK." -ForegroundColor Green
} else {
    Write-Host "Docker compose config has issues." -ForegroundColor Red
}

Write-Host "`nPreflight complete."
