# Sentinel Stage 4 Smoke Test
$ErrorActionPreference = "Continue"

cd "$HOME\Desktop\EyeOnBits-Sentinel"

Write-Host "=== Sentinel Stage 4 Smoke Test ===" -ForegroundColor Cyan

Write-Host "`nGit status:"
git status --short

Write-Host "`nBackend health:"
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/api/health" -TimeoutSec 5
    $health | ConvertTo-Json -Depth 5
    Write-Host "Backend OK" -ForegroundColor Green
} catch {
    Write-Host "Backend failed" -ForegroundColor Red
    Write-Host $_
}

Write-Host "`nFrontend:"
try {
    $frontend = Invoke-WebRequest -Uri "http://localhost:3000" -UseBasicParsing -TimeoutSec 5
    Write-Host "Frontend HTTP status: $($frontend.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "Frontend failed" -ForegroundColor Red
    Write-Host $_
}

Write-Host "`nAI config environment check:"
if ($env:OPENAI_API_KEY) {
    Write-Host "OPENAI_API_KEY appears set in current shell." -ForegroundColor Green
} else {
    Write-Host "OPENAI_API_KEY not set in current shell. This is okay if AI is disabled/fallback mode." -ForegroundColor Yellow
}
