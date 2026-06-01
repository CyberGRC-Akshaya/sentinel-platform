# Sentinel Stage 4 Frontend AI Manual Test Checklist
$ErrorActionPreference = "Continue"

cd "$HOME\Desktop\EyeOnBits-Sentinel"

Write-Host "=== Stage 4 Frontend AI Test ===" -ForegroundColor Cyan

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

Write-Host "`nManual test required in browser:"
Write-Host "1. Open http://localhost:3000"
Write-Host "2. Run + Save Review to Vault"
Write-Host "3. Click AI Assist Review"
Write-Host "4. Expected: fallback panel appears safely if AI is disabled"
Write-Host "5. Confirm Run + Save, exports, and tabs still work"
