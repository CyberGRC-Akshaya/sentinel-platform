# Sentinel Stage 4 Frontend AI Snippet Extraction
# Purpose: Extract exact frontend sections before editing page.tsx.

$ErrorActionPreference = "Stop"

Write-Host "=== Sentinel Stage 4 Frontend AI Snippet Extraction ===" -ForegroundColor Cyan

$project = "$HOME\Desktop\EyeOnBits-Sentinel"
$current = (Get-Location).Path

if ($current -ne $project) {
    Write-Host "You are not in expected project folder." -ForegroundColor Red
    Write-Host "Current:  $current"
    Write-Host "Expected: $project"
    exit 1
}

$page = Join-Path $project "frontend\app\page.tsx"
$outDir = Join-Path $project "docs\stage-4-ai-integration\snippets"
New-Item -ItemType Directory -Path $outDir -Force | Out-Null

if (!(Test-Path $page)) {
    Write-Host "page.tsx not found." -ForegroundColor Red
    exit 1
}

$lines = Get-Content $page

function Save-Range {
    param(
        [string]$Name,
        [int]$Start,
        [int]$End
    )
    $max = $lines.Count - 1
    if ($Start -lt 0) { $Start = 0 }
    if ($End -gt $max) { $End = $max }
    $path = Join-Path $outDir $Name
    $lines[$Start..$End] | Set-Content $path -Encoding UTF8
    Write-Host "Created: $path" -ForegroundColor Green
}

# These ranges are intentionally broad but read-only.
Save-Range "01_top_imports_and_types.txt" 0 120
Save-Range "02_state_and_loader_functions.txt" 100 260
Save-Range "03_core_review_functions.txt" 620 760
Save-Range "04_download_and_copy_functions.txt" 760 840
Save-Range "05_main_render_start_and_actions.txt" 820 950
Save-Range "06_tab_render_area.txt" 900 1125
Save-Range "07_lower_render_area.txt" 1125 1388

$report = Join-Path $outDir "README_SNIPPETS.txt"
@"
Stage 4 frontend snippets created.

Please share these files before modifying page.tsx:
1. 01_top_imports_and_types.txt
2. 02_state_and_loader_functions.txt
3. 03_core_review_functions.txt
4. 05_main_render_start_and_actions.txt
5. 06_tab_render_area.txt

Do not edit page.tsx until insertion points are reviewed.
"@ | Set-Content $report -Encoding UTF8

Write-Host ""
Write-Host "Snippet extraction complete." -ForegroundColor Cyan
Write-Host "Folder: docs\stage-4-ai-integration\snippets"
