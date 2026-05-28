# Sentinel Stage 2 Code Inventory Script - Hotfix
# Purpose: Inspect current codebase without changing application code.
# This version avoids fragile quoting and writes a simple text report.

$ErrorActionPreference = "Continue"

Write-Host "=== Sentinel Stage 2 Code Inventory Hotfix ===" -ForegroundColor Cyan

$project = Join-Path $HOME "Desktop\EyeOnBits-Sentinel"
$current = (Get-Location).Path

if ($current -ne $project) {
    Write-Host "WARNING: You are not in the expected project folder." -ForegroundColor Yellow
    Write-Host "Current:  $current"
    Write-Host "Expected: $project"
    Write-Host "Run: cd `$HOME\Desktop\EyeOnBits-Sentinel"
    exit 1
}

$reportDir = Join-Path $project "docs\stage-2-code-stabilization"
New-Item -ItemType Directory -Path $reportDir -Force | Out-Null

$report = Join-Path $reportDir "STAGE_2_CODE_INVENTORY_REPORT.txt"

if (Test-Path $report) {
    Remove-Item $report -Force
}

function Add-ReportLine {
    param([string]$Text)
    Add-Content -Path $report -Value $Text -Encoding UTF8
}

function Get-LineCount {
    param([string]$FilePath)
    if (Test-Path $FilePath) {
        return (Get-Content -Path $FilePath -ErrorAction SilentlyContinue | Measure-Object -Line).Lines
    }
    return 0
}

function Get-PatternCount {
    param([string]$FilePath, [string]$Pattern)
    if (Test-Path $FilePath) {
        return (Select-String -Path $FilePath -Pattern $Pattern -AllMatches -ErrorAction SilentlyContinue | Measure-Object).Count
    }
    return 0
}

function Add-Matches {
    param([string]$Title, [string]$FilePath, [string]$Pattern)

    Add-ReportLine ""
    Add-ReportLine $Title
    Add-ReportLine ("-" * $Title.Length)

    if (!(Test-Path $FilePath)) {
        Add-ReportLine "File not found: $FilePath"
        return
    }

    $matches = Select-String -Path $FilePath -Pattern $Pattern -ErrorAction SilentlyContinue
    if ($null -eq $matches) {
        Add-ReportLine "No matches found."
        return
    }

    foreach ($match in $matches) {
        $lineText = $match.Line.Trim()
        Add-ReportLine ("Line " + $match.LineNumber + ": " + $lineText)
    }
}

$frontendPage = "frontend\app\page.tsx"
$frontendCss = "frontend\app\globals.css"
$frontendLayout = "frontend\app\layout.tsx"
$backendMain = "backend\app\main.py"
$composeFile = "docker-compose.yml"

Add-ReportLine "SENTINEL STAGE 2 CODE INVENTORY REPORT"
Add-ReportLine ("Generated: " + (Get-Date))
Add-ReportLine ("Project: " + $project)
Add-ReportLine ("Branch: " + (git branch --show-current))
Add-ReportLine ""

Add-ReportLine "GIT STATUS"
Add-ReportLine "----------"
$gitStatus = git status --short
if ($gitStatus) {
    foreach ($line in $gitStatus) { Add-ReportLine $line }
} else {
    Add-ReportLine "Working tree clean."
}
Add-ReportLine ""

Add-ReportLine "KEY FILE LINE COUNTS"
Add-ReportLine "--------------------"
Add-ReportLine ($frontendPage + " : " + (Get-LineCount $frontendPage) + " lines")
Add-ReportLine ($frontendCss + " : " + (Get-LineCount $frontendCss) + " lines")
Add-ReportLine ($frontendLayout + " : " + (Get-LineCount $frontendLayout) + " lines")
Add-ReportLine ($backendMain + " : " + (Get-LineCount $backendMain) + " lines")
Add-ReportLine ($composeFile + " : " + (Get-LineCount $composeFile) + " lines")
Add-ReportLine ""

Add-ReportLine "FRONTEND INVENTORY - page.tsx"
Add-ReportLine "-----------------------------"
Add-ReportLine ("useState count: " + (Get-PatternCount $frontendPage "useState"))
Add-ReportLine ("useEffect count: " + (Get-PatternCount $frontendPage "useEffect"))
Add-ReportLine ("async function count: " + (Get-PatternCount $frontendPage "async function"))
Add-ReportLine ("function count: " + (Get-PatternCount $frontendPage "function "))
Add-ReportLine ("fetch call count: " + (Get-PatternCount $frontendPage "fetch"))
Add-ReportLine ("activeTab references: " + (Get-PatternCount $frontendPage "activeTab"))
Add-ReportLine ("download references: " + (Get-PatternCount $frontendPage "download"))

Add-Matches "FRONTEND TAB REFERENCES" $frontendPage "activeTab|setActiveTab"
Add-Matches "FRONTEND API CALLS" $frontendPage "fetch"
Add-Matches "FRONTEND DOWNLOAD FUNCTIONS" $frontendPage "download"

Add-ReportLine ""
Add-ReportLine "BACKEND INVENTORY - main.py"
Add-ReportLine "---------------------------"
Add-ReportLine ("app route count: " + (Get-PatternCount $backendMain "@app\."))
Add-ReportLine ("def count: " + (Get-PatternCount $backendMain "^def "))
Add-ReportLine ("async def count: " + (Get-PatternCount $backendMain "^async def "))
Add-ReportLine ("HTMLResponse references: " + (Get-PatternCount $backendMain "HTMLResponse"))
Add-ReportLine ("sqlite references: " + (Get-PatternCount $backendMain "sqlite"))
Add-ReportLine ("json references: " + (Get-PatternCount $backendMain "json"))

Add-Matches "BACKEND ROUTES" $backendMain "@app\."
Add-Matches "BACKEND FUNCTION DEFINITIONS" $backendMain "^(def|async def) "

Add-ReportLine ""
Add-ReportLine "CSS INVENTORY - globals.css"
Add-ReportLine "---------------------------"
Add-ReportLine ("class selector rough count: " + (Get-PatternCount $frontendCss "^\.[a-zA-Z0-9_-]+"))
Add-ReportLine ("media query count: " + (Get-PatternCount $frontendCss "@media"))
Add-ReportLine ("important count: " + (Get-PatternCount $frontendCss "!important"))

Add-ReportLine ""
Add-ReportLine "DOCKER COMPOSE CONFIG CHECK"
Add-ReportLine "---------------------------"
docker compose config | Out-Null
if ($LASTEXITCODE -eq 0) {
    Add-ReportLine "Docker Compose config: OK"
} else {
    Add-ReportLine "Docker Compose config: FAILED"
}

Add-ReportLine ""
Add-ReportLine "RECOMMENDED FIRST STABILIZATION TARGETS"
Add-ReportLine "---------------------------------------"
Add-ReportLine "1. Do not change Docker yet."
Add-ReportLine "2. Do not redesign UI."
Add-ReportLine "3. First inspect frontend/app/page.tsx section boundaries."
Add-ReportLine "4. First low-risk frontend extraction should be helper functions/static constants, not JSX-heavy tabs."
Add-ReportLine "5. First low-risk backend extraction should be pure scoring/helper functions, not routes."
Add-ReportLine "6. Commit only after app still builds and health check passes."

Write-Host "Inventory report created:" -ForegroundColor Green
Write-Host $report
Write-Host ""
Write-Host "Open/share this report:" -ForegroundColor Cyan
Write-Host "docs\stage-2-code-stabilization\STAGE_2_CODE_INVENTORY_REPORT.txt"
