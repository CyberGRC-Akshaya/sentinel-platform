# Stop Sentinel
$ErrorActionPreference = "Continue"

cd "$HOME\Desktop\EyeOnBits-Sentinel"

docker compose down --remove-orphans
