# Sentinel Stage 4B Create Local AI Environment
# This creates .env.local locally. It is ignored by Git.
# Do not paste this file into chat. Do not commit it.

$ErrorActionPreference = "Stop"

cd "$HOME\Desktop\EyeOnBits-Sentinel"

Write-Host "=== Create local AI environment ===" -ForegroundColor Cyan
Write-Host "Do not paste your API key into ChatGPT or GitHub." -ForegroundColor Yellow

$model = Read-Host "Enter OpenAI model name available in your account"
$key = Read-Host "Enter OpenAI API key for local testing only"

if ([string]::IsNullOrWhiteSpace($model)) {
    Write-Host "Model is required." -ForegroundColor Red
    exit 1
}

if ([string]::IsNullOrWhiteSpace($key)) {
    Write-Host "API key is required for real AI mode. For fallback-only mode, skip this script." -ForegroundColor Red
    exit 1
}

@"
AI_REVIEW_ENABLED=true
OPENAI_MODEL=$model
OPENAI_API_KEY=$key
"@ | Set-Content ".env.local" -Encoding UTF8

Write-Host ".env.local created locally." -ForegroundColor Green
Write-Host "Now run: git status" -ForegroundColor Cyan
Write-Host "Expected: .env.local should NOT appear." -ForegroundColor Cyan
