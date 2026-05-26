# Start Sentinel for Stage 2 testing
$ErrorActionPreference = "Stop"

cd "$HOME\Desktop\EyeOnBits-Sentinel"

docker compose down --remove-orphans
docker compose up --build
