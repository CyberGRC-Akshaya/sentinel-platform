# Sentinel Stage 4B Install Docker Compose env_file for backend
# Backs up docker-compose.yml and adds .env.local to backend service if missing.

$ErrorActionPreference = "Stop"

cd "$HOME\Desktop\EyeOnBits-Sentinel"

$compose = "docker-compose.yml"

if (!(Test-Path $compose)) {
    Write-Host "docker-compose.yml not found." -ForegroundColor Red
    exit 1
}

$raw = Get-Content $compose -Raw

if ($raw -match "\.env\.local") {
    Write-Host "docker-compose.yml already references .env.local. No change made." -ForegroundColor Yellow
    exit 0
}

$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$backup = "docker-compose.yml.stage4b-ai-env-backup-$timestamp"
Copy-Item $compose $backup -Force
Write-Host "Backup created: $backup" -ForegroundColor Green

$lines = Get-Content $compose
$backendIndex = -1

for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match "^\s{2}backend:\s*$|^backend:\s*$") {
        $backendIndex = $i
        break
    }
}

if ($backendIndex -lt 0) {
    Write-Host "Could not find backend service in docker-compose.yml." -ForegroundColor Red
    exit 1
}

$backendLine = $lines[$backendIndex]
$indent = ($backendLine -replace "backend:\s*$", "")
$childIndent = $indent + "  "
$listIndent = $childIndent + "  "

# Insert env_file immediately after backend: line. This is simple and valid for compose service keys.
$insert = @(
    "$childIndent" + "env_file:",
    "$listIndent" + "- .env.local"
)

$newLines = @()
for ($i = 0; $i -lt $lines.Count; $i++) {
    $newLines += $lines[$i]
    if ($i -eq $backendIndex) {
        $newLines += $insert
    }
}

$newLines | Set-Content $compose -Encoding UTF8

Write-Host "docker-compose.yml updated to pass .env.local into backend service." -ForegroundColor Green

Write-Host "`nValidate compose config:" -ForegroundColor Cyan
docker compose config | Out-Null
if ($LASTEXITCODE -eq 0) {
    Write-Host "Docker compose config OK." -ForegroundColor Green
} else {
    Write-Host "Docker compose config failed. Use rollback backup if needed." -ForegroundColor Red
}
