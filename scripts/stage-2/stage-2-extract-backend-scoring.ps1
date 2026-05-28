# Sentinel Stage 2 Backend Scoring Extraction
$ErrorActionPreference = "Stop"

Write-Host "=== Sentinel Stage 2 Backend Scoring Extraction ===" -ForegroundColor Cyan

$project = "$HOME\Desktop\EyeOnBits-Sentinel"
$current = (Get-Location).Path

if ($current -ne $project) {
    Write-Host "You are not in the expected project folder." -ForegroundColor Red
    Write-Host "Current:  $current"
    Write-Host "Expected: $project"
    Write-Host "Run: cd `$HOME\Desktop\EyeOnBits-Sentinel"
    exit 1
}

$mainPath = Join-Path $project "backend\app\main.py"
$servicesDir = Join-Path $project "backend\app\services"
$scoringPath = Join-Path $servicesDir "scoring.py"
$initPath = Join-Path $servicesDir "__init__.py"

if (!(Test-Path $mainPath)) {
    Write-Host "main.py not found: $mainPath" -ForegroundColor Red
    exit 1
}

$raw = Get-Content $mainPath -Raw

if ($raw.Contains("from app.services.scoring import")) {
    Write-Host "Scoring extraction already appears to be applied. No changes made." -ForegroundColor Yellow
    exit 0
}

$constantsStartMarker = "CONTROL_ATLAS = "
$constantsEndMarker = "class AnalyzeRequest(BaseModel):"
$helpersStartMarker = "def normalize_text(item: EvidenceItem)"
$helpersEndMarker = "def build_finding("

$constantsStart = $raw.IndexOf($constantsStartMarker)
$constantsEnd = $raw.IndexOf($constantsEndMarker)
$helpersStart = $raw.IndexOf($helpersStartMarker)
$helpersEnd = $raw.IndexOf($helpersEndMarker)

if ($constantsStart -lt 0 -or $constantsEnd -lt 0 -or $helpersStart -lt 0 -or $helpersEnd -lt 0) {
    Write-Host "Required marker not found. No changes made." -ForegroundColor Red
    Write-Host "constantsStart=$constantsStart constantsEnd=$constantsEnd helpersStart=$helpersStart helpersEnd=$helpersEnd"
    exit 1
}

if (!($constantsStart -lt $constantsEnd -and $constantsEnd -lt $helpersStart -and $helpersStart -lt $helpersEnd)) {
    Write-Host "Marker order is unexpected. No changes made." -ForegroundColor Red
    Write-Host "constantsStart=$constantsStart constantsEnd=$constantsEnd helpersStart=$helpersStart helpersEnd=$helpersEnd"
    exit 1
}

$constantsBlock = $raw.Substring($constantsStart, $constantsEnd - $constantsStart)
$helpersBlock = $raw.Substring($helpersStart, $helpersEnd - $helpersStart)

$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$backupPath = Join-Path $project "backend\app\main.py.stage2-scoring-backup-$timestamp"
Copy-Item $mainPath $backupPath -Force
Write-Host "Backup created:" -ForegroundColor Green
Write-Host $backupPath

New-Item -ItemType Directory -Path $servicesDir -Force | Out-Null
if (!(Test-Path $initPath)) {
    "" | Set-Content $initPath -Encoding UTF8
}

$scoringHeader = @"
from pydantic import BaseModel
from typing import Any, Dict, List, Optional


"@

$scoringContent = $scoringHeader + $constantsBlock.Trim() + "`n`n" + $helpersBlock.Trim() + "`n"
Set-Content -Path $scoringPath -Value $scoringContent -Encoding UTF8

$importBlock = @"
from app.services.scoring import (
    CONTROL_ATLAS,
    FRAMEWORK_LIBRARY,
    DIMENSIONS,
    INTAKE_REQUIREMENTS,
    DOMAIN_KEYWORDS,
    EvidenceItem,
    normalize_text,
    detect_domain,
    infer_artifact_profile,
    intake_gap_analysis,
    dimension_score,
    map_control_atlas,
    score_item,
    severity_from_score,
    framework_mappings_for,
)

"@

$updated = $raw.Replace($constantsBlock, "")
$updated = $updated.Replace($helpersBlock, "")

if ($updated.Contains("import uuid`r`n")) {
    $updated = $updated.Replace("import uuid`r`n", "import uuid`r`n`r`n" + $importBlock)
} elseif ($updated.Contains("import uuid`n")) {
    $updated = $updated.Replace("import uuid`n", "import uuid`n`n" + $importBlock)
} else {
    Write-Host "Could not find import uuid marker. Restoring backup." -ForegroundColor Red
    Copy-Item $backupPath $mainPath -Force
    Remove-Item $scoringPath -Force
    exit 1
}

Set-Content -Path $mainPath -Value $updated -Encoding UTF8

Write-Host "Created:" -ForegroundColor Green
Write-Host $scoringPath
Write-Host "Updated:" -ForegroundColor Green
Write-Host $mainPath

Write-Host "`nPost-extraction checks:" -ForegroundColor Cyan

$mainAfter = Get-Content $mainPath -Raw
$scoringAfter = Get-Content $scoringPath -Raw

if ($mainAfter.Contains("CONTROL_ATLAS = ")) {
    Write-Host "WARNING: CONTROL_ATLAS definition still found in main.py" -ForegroundColor Yellow
} else {
    Write-Host "OK: CONTROL_ATLAS definition moved out of main.py" -ForegroundColor Green
}

if ($mainAfter.Contains("def normalize_text(item: EvidenceItem)")) {
    Write-Host "WARNING: normalize_text definition still found in main.py" -ForegroundColor Yellow
} else {
    Write-Host "OK: scoring helper definitions moved out of main.py" -ForegroundColor Green
}

if ($scoringAfter.Contains("class EvidenceItem(BaseModel):") -and $scoringAfter.Contains("def score_item(item: EvidenceItem)")) {
    Write-Host "OK: scoring.py contains EvidenceItem and score_item" -ForegroundColor Green
} else {
    Write-Host "WARNING: scoring.py may be incomplete" -ForegroundColor Yellow
}

Write-Host "`nOptional Python syntax check:" -ForegroundColor Cyan
try {
    python -m py_compile backend\app\main.py backend\app\services\scoring.py
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Python syntax check passed." -ForegroundColor Green
    } else {
        Write-Host "Python syntax check failed. Review output above." -ForegroundColor Red
    }
} catch {
    Write-Host "Python command unavailable or failed. Docker build will validate." -ForegroundColor Yellow
}

Write-Host "`nNext:" -ForegroundColor Cyan
Write-Host "docker compose down --remove-orphans"
Write-Host "docker compose up --build"
