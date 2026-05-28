# Run Sentinel Product
$ErrorActionPreference = "Stop"

cd "$HOME\Desktop\EyeOnBits-Sentinel"

docker compose down --remove-orphans
docker compose up --build
