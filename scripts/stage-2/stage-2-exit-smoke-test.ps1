# Sentinel Stage 2 Exit Smoke Test
$ErrorActionPreference = "Continue"

cd "$HOME\Desktop\EyeOnBits-Sentinel"

Write-Host "=== Stage 2 Exit Smoke Test ===" -ForegroundColor Cyan

Write-Host "`nGit status:"
git status --short

Write-Host "`nDocker compose config:"
docker compose config | Out-Null
if ($LASTEXITCODE -eq 0) { Write-Host "Docker compose config OK" -ForegroundColor Green } else { Write-Host "Docker compose config failed" -ForegroundColor Red }

Write-Host "`nCurrent containers:"
docker compose ps

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
