# Sentinel Stage 2 Health Check
$ErrorActionPreference = "Continue"

Write-Host "=== Sentinel Stage 2 Health Check ===" -ForegroundColor Cyan

Write-Host "`nDocker containers:"
docker compose ps

Write-Host "`nBackend health:"
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/api/health" -TimeoutSec 5
    $health | ConvertTo-Json -Depth 5
    Write-Host "Backend health check OK." -ForegroundColor Green
} catch {
    Write-Host "Backend health check failed." -ForegroundColor Red
    Write-Host $_
}

Write-Host "`nFrontend status:"
try {
    $response = Invoke-WebRequest -Uri "http://localhost:3000" -TimeoutSec 5
    Write-Host "Frontend HTTP status: $($response.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "Frontend check failed." -ForegroundColor Red
    Write-Host $_
}

Write-Host "`nRecent frontend logs:"
docker compose logs --tail=40 frontend

Write-Host "`nRecent backend logs:"
docker compose logs --tail=40 backend
