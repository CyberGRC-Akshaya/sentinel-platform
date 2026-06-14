# Sentinel Stage 4B Secure Gitignore
$ErrorActionPreference = "Stop"

cd "$HOME\Desktop\EyeOnBits-Sentinel"

$ignoreBlock = @"

# Local environment and secrets
.env
.env.local
.env.*.local
*.secret
*apikey*
*api-key*

# Local Stage 4 AI backups
backend/app/*.stage4-ai-backup-*
frontend/app/*.stage4-ai-frontend-backup-*
"@

$gitignore = ".gitignore"
if (!(Test-Path $gitignore)) {
    "" | Set-Content $gitignore
}

$current = Get-Content $gitignore -Raw
if ($current -notmatch "\.env\.local") {
    Add-Content -Path $gitignore -Value $ignoreBlock
    Write-Host ".gitignore updated with local secret protections." -ForegroundColor Green
} else {
    Write-Host ".gitignore already appears to include local secret protections." -ForegroundColor Yellow
}
