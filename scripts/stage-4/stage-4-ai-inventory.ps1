# Sentinel Stage 4 AI Inventory
$ErrorActionPreference = "Continue"

Write-Host "=== Sentinel Stage 4 AI Inventory ===" -ForegroundColor Cyan

$project = "$HOME\Desktop\EyeOnBits-Sentinel"
$current = (Get-Location).Path

if ($current -ne $project) {
    Write-Host "WARNING: You are not in expected project folder." -ForegroundColor Yellow
    Write-Host "Current:  $current"
    Write-Host "Expected: $project"
    Write-Host "Run: cd `$HOME\Desktop\EyeOnBits-Sentinel"
    exit 1
}

$reportDir = Join-Path $project "docs\stage-4-ai-integration"
New-Item -ItemType Directory -Path $reportDir -Force | Out-Null
$report = Join-Path $reportDir "STAGE_4_AI_INVENTORY_REPORT.txt"

if (Test-Path $report) {
    Remove-Item $report -Force
}

function Add-Line {
    param([string]$Text)
    Add-Content -Path $report -Value $Text -Encoding UTF8
}

function Count-Lines {
    param([string]$File)
    if (Test-Path $File) {
        return (Get-Content $File | Measure-Object -Line).Lines
    }
    return 0
}

function Count-Matches {
    param([string]$File, [string]$Pattern)
    if (Test-Path $File) {
        return (Select-String -Path $File -Pattern $Pattern -AllMatches -ErrorAction SilentlyContinue | Measure-Object).Count
    }
    return 0
}

$main = "backend\app\main.py"
$scoring = "backend\app\services\scoring.py"
$db = "backend\app\db\sqlite.py"
$page = "frontend\app\page.tsx"
$compose = "docker-compose.yml"
$requirements = "backend\requirements.txt"

Add-Line "SENTINEL STAGE 4 AI INVENTORY REPORT"
Add-Line ("Generated: " + (Get-Date))
Add-Line ("Branch: " + (git branch --show-current))
Add-Line ""

Add-Line "GIT STATUS"
Add-Line "----------"
$status = git status --short
if ($status) {
    foreach ($line in $status) { Add-Line $line }
} else {
    Add-Line "Working tree clean."
}
Add-Line ""

Add-Line "KEY FILE LINE COUNTS"
Add-Line "--------------------"
Add-Line ("backend/app/main.py lines: " + (Count-Lines $main))
Add-Line ("backend/app/services/scoring.py lines: " + (Count-Lines $scoring))
Add-Line ("backend/app/db/sqlite.py lines: " + (Count-Lines $db))
Add-Line ("frontend/app/page.tsx lines: " + (Count-Lines $page))
Add-Line ("backend/requirements.txt lines: " + (Count-Lines $requirements))
Add-Line ""

Add-Line "AI-RELATED EXISTING REFERENCES"
Add-Line "------------------------------"
Add-Line ("main.py OpenAI references: " + (Count-Matches $main "openai|OpenAI|AI Assist|ai_review|prompt"))
Add-Line ("page.tsx OpenAI references: " + (Count-Matches $page "openai|OpenAI|AI Assist|ai_review|prompt"))
Add-Line ("requirements OpenAI references: " + (Count-Matches $requirements "openai"))
Add-Line ("docker-compose env references: " + (Count-Matches $compose "OPENAI|AI_REVIEW|env_file|environment"))
Add-Line ""

Add-Line "BACKEND ROUTE REFERENCES"
Add-Line "------------------------"
if (Test-Path $main) {
    $routes = Select-String -Path $main -Pattern "@app\."
    foreach ($r in $routes) {
        Add-Line ("Line " + $r.LineNumber + ": " + $r.Line.Trim())
    }
}
Add-Line ""

Add-Line "FRONTEND FETCH CALLS"
Add-Line "--------------------"
if (Test-Path $page) {
    $fetches = Select-String -Path $page -Pattern "fetch\("
    foreach ($f in $fetches) {
        Add-Line ("Line " + $f.LineNumber + ": " + $f.Line.Trim())
    }
}
Add-Line ""

Add-Line "RECOMMENDED STAGE 4 FIRST CODE CHANGE"
Add-Line "-------------------------------------"
Add-Line "1. Add AI configuration template first."
Add-Line "2. Add backend/app/services/ai_review.py second."
Add-Line "3. Add backend route only after service exists."
Add-Line "4. Do not touch frontend until backend AI endpoint is stable."
Add-Line "5. AI must be optional and fallback-safe."

Write-Host "Stage 4 AI inventory report created:" -ForegroundColor Green
Write-Host $report
