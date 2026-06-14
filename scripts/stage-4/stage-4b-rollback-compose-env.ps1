# Sentinel Stage 4B Rollback Docker Compose env_file change
$ErrorActionPreference = "Stop"

cd "$HOME\Desktop\EyeOnBits-Sentinel"

$backup = Get-ChildItem -Filter "docker-compose.yml.stage4b-ai-env-backup-*" | Sort-Object LastWriteTime -Descending | Select-Object -First 1

if ($null -eq $backup) {
    Write-Host "No docker-compose Stage 4B backup found." -ForegroundColor Red
    exit 1
}

Copy-Item $backup.FullName "docker-compose.yml" -Force
Write-Host "docker-compose.yml restored from:" -ForegroundColor Green
Write-Host $backup.FullName
