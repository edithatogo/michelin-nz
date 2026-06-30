#!/bin/sh
set -eu

# Dynamically compute hash of data records and pipeline script to version the dataset
script_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
DATA_HASH=$(cat "$script_dir/michelin.py" "$script_dir/archive/world_bank_population_2024.json" "$script_dir/archive/world_bank_gdp_2024.json" | shasum -a 256 | head -c 8)
DATE_STR=$(date +"%Y.%m.%d")

cat <<EOF
{
  "version": "DATA-v${DATE_STR}-${DATA_HASH}",
  "compiled": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
}
EOF
