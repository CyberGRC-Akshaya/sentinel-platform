# Stop Sentinel Product
$ErrorActionPreference = "Continue"

cd "$HOME\Desktop\EyeOnBits-Sentinel"

docker compose down --remove-orphans
