# Sentinel Stage 4 AI Health + Fallback Test
$ErrorActionPreference = "Continue"

cd "$HOME\Desktop\EyeOnBits-Sentinel"

Write-Host "=== Sentinel Stage 4 AI Health + Fallback Test ===" -ForegroundColor Cyan

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

Write-Host "`nAI fallback endpoint:"
$body = @{
    review_id = "stage4-prep-test"
    mode = "executive_summary"
    organization = "Sample Organization"
    industry = "Financial Services"
    review_objective = "Validate AI Assist fallback behavior"
    result = @{
        evidence_defensibility_score = 71
        overall_rating = "Moderate"
        control_atlas_coverage_score = 60
        metadata_completeness_score = 80
        total_findings = 3
        findings = @(
            @{
                severity = "Medium"
                issue = "Evidence package needs clearer source lineage."
                remediation = "Provide source export and review approval."
            }
        )
    }
} | ConvertTo-Json -Depth 10

try {
    $ai = Invoke-RestMethod -Uri "http://localhost:8000/api/ai/assist-review" -Method POST -ContentType "application/json" -Body $body -TimeoutSec 20
    $ai | ConvertTo-Json -Depth 10
    Write-Host "AI fallback endpoint OK." -ForegroundColor Green
} catch {
    Write-Host "AI fallback endpoint failed." -ForegroundColor Red
    Write-Host $_
}
