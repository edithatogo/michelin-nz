#!/bin/sh
set -eu

# Dynamically compute hash of data records and pipeline scripts to version the dataset
script_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
DATA_HASH=$(cat "$script_dir/michelin.py" "$script_dir/metrics.mojo" "$script_dir/aggregate_country_ledger.csv" "$script_dir/official_michelin_guide_coverage.csv" "$script_dir/archive/world_bank_population_2024.json" "$script_dir/archive/world_bank_gdp_2024.json" | shasum -a 256 | head -c 8)
DATE_STR=$(date +"%Y.%m.%d")

cat <<EOF
{
  "version": "DATA-v${DATE_STR}-${DATA_HASH}",
  "compiled": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
}
EOF
