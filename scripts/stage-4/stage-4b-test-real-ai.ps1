# Sentinel Stage 4B Real AI Endpoint Test
$ErrorActionPreference = "Continue"

cd "$HOME\Desktop\EyeOnBits-Sentinel"

Write-Host "=== Sentinel Stage 4B Real AI Test ===" -ForegroundColor Cyan

Write-Host "`nBackend health:"
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/api/health" -TimeoutSec 5
    $health | ConvertTo-Json -Depth 5
    Write-Host "Backend OK" -ForegroundColor Green
} catch {
    Write-Host "Backend failed" -ForegroundColor Red
    Write-Host $_
}

Write-Host "`nAI Assist endpoint:"
$body = @{
    review_id = "stage4b-real-ai-test"
    mode = "executive_summary"
    organization = "Sample Tier-1 Bank"
    industry = "BFSI / Regulated Banking"
    review_objective = "Validate real AI assist mode using sanitized sample evidence"
    result = @{
        evidence_defensibility_score = 62
        overall_rating = "Weak"
        control_atlas_coverage_score = 0
        metadata_completeness_score = 60
        total_findings = 2
        findings = @(
            @{
                severity = "High"
                issue = "Evidence does not show reviewer approval or reconciliation."
                remediation = "Provide approval record, source export, and reconciliation evidence."
            },
            @{
                severity = "Medium"
                issue = "Metric calculation logic is not fully traceable."
                remediation = "Provide calculation workbook and reviewer sign-off."
            }
        )
    }
} | ConvertTo-Json -Depth 10

try {
    $ai = Invoke-RestMethod -Uri "http://localhost:8000/api/ai/assist-review" -Method POST -ContentType "application/json" -Body $body -TimeoutSec 90
    $ai | ConvertTo-Json -Depth 10
    if ($ai.status -eq "completed") {
        Write-Host "Real AI mode completed." -ForegroundColor Green
    } elseif ($ai.status -eq "fallback") {
        Write-Host "Fallback returned. Check .env.local, docker-compose env_file, model access, and API key." -ForegroundColor Yellow
    } else {
        Write-Host "AI returned unexpected status." -ForegroundColor Yellow
    }
} catch {
    Write-Host "AI endpoint test failed." -ForegroundColor Red
    Write-Host $_
}
