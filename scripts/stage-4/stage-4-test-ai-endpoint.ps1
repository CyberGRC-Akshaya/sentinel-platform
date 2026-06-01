# Sentinel Stage 4 AI Endpoint Fallback Test
$ErrorActionPreference = "Continue"

cd "$HOME\Desktop\EyeOnBits-Sentinel"

Write-Host "=== Sentinel Stage 4 AI Endpoint Fallback Test ===" -ForegroundColor Cyan

$body = @{
    review_id = "local-test"
    mode = "executive_summary"
    organization = "Sample Tier-1 Bank"
    industry = "BFSI / Regulated Banking"
    review_objective = "Test AI assist fallback behavior"
    result = @{
        evidence_defensibility_score = 62
        overall_rating = "Weak"
        control_atlas_coverage_score = 0
        metadata_completeness_score = 60
        total_findings = 12
        findings = @(
            @{
                severity = "High"
                issue = "Evidence does not show reviewer approval."
                remediation = "Provide approval record and reconciliation evidence."
            }
        )
    }
} | ConvertTo-Json -Depth 10

try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/ai/assist-review" -Method POST -ContentType "application/json" -Body $body -TimeoutSec 20
    $response | ConvertTo-Json -Depth 10
    Write-Host "AI endpoint fallback test completed." -ForegroundColor Green
} catch {
    Write-Host "AI endpoint fallback test failed." -ForegroundColor Red
    Write-Host $_
}
