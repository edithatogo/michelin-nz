#!/bin/bash
# Dynamically compute hash of data records and pipeline script to version the dataset
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_HASH=$(cat "$DIR/michelin.py" "$DIR/archive/world_bank_population_2024.json" "$DIR/archive/world_bank_gdp_2024.json" | shasum -a 256 | head -c 8)
DATE_STR=$(date +"%Y.%m.%d")

cat <<EOF
{
  "version": "DATA-v${DATE_STR}-${DATA_HASH}",
  "compiled": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
}
EOF
