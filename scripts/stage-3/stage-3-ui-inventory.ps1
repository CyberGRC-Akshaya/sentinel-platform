# Sentinel Stage 3 UI Inventory
$ErrorActionPreference = "Continue"

Write-Host "=== Sentinel Stage 3 UI Inventory ===" -ForegroundColor Cyan

$project = "$HOME\Desktop\EyeOnBits-Sentinel"
$current = (Get-Location).Path

if ($current -ne $project) {
    Write-Host "WARNING: You are not in expected project folder." -ForegroundColor Yellow
    Write-Host "Current:  $current"
    Write-Host "Expected: $project"
    Write-Host "Run: cd `$HOME\Desktop\EyeOnBits-Sentinel"
    exit 1
}

$reportDir = Join-Path $project "docs\stage-3-design-upgrade"
New-Item -ItemType Directory -Path $reportDir -Force | Out-Null
$report = Join-Path $reportDir "STAGE_3_UI_INVENTORY_REPORT.txt"

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

$page = "frontend\app\page.tsx"
$css = "frontend\app\globals.css"

Add-Line "SENTINEL STAGE 3 UI INVENTORY REPORT"
Add-Line ("Generated: " + (Get-Date))
Add-Line ("Branch: " + (git branch --show-current))
Add-Line ""

Add-Line "FILE SIZE"
Add-Line "---------"
Add-Line ("page.tsx lines: " + (Count-Lines $page))
Add-Line ("globals.css lines: " + (Count-Lines $css))
Add-Line ""

Add-Line "CSS COUNTS"
Add-Line "----------"
Add-Line ("class selector count: " + (Count-Matches $css "^\.[a-zA-Z0-9_-]+"))
Add-Line ("media query count: " + (Count-Matches $css "@media"))
Add-Line ("important count: " + (Count-Matches $css "!important"))
Add-Line ("gradient references: " + (Count-Matches $css "gradient"))
Add-Line ("box-shadow references: " + (Count-Matches $css "box-shadow"))
Add-Line ("border-radius references: " + (Count-Matches $css "border-radius"))
Add-Line ""

Add-Line "POSSIBLE CORE CSS SECTIONS"
Add-Line "--------------------------"
$patterns = @("body", ".page", ".hero", ".card", ".panel", ".tabs", ".button", ".btn", ".grid", ".output", ".finding", ".severity", ".table", ".final", ".launch", ".demo")
foreach ($p in $patterns) {
    Add-Line ("Pattern " + $p + " count: " + (Count-Matches $css [regex]::Escape($p)))
}

Add-Line ""
Add-Line "PAGE CLASSNAME REFERENCES"
Add-Line "-------------------------"
$matches = Select-String -Path $page -Pattern "className="
foreach ($m in $matches | Select-Object -First 80) {
    Add-Line ("Line " + $m.LineNumber + ": " + $m.Line.Trim())
}

Write-Host "UI inventory report created:" -ForegroundColor Green
Write-Host $report
Write-Host ""
Write-Host "Share this report before making CSS changes." -ForegroundColor Cyan
