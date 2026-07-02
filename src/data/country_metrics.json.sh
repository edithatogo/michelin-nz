#!/bin/sh
set -eu

script_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
project_root="$(CDPATH= cd -- "$script_dir/../.." && pwd)"

if command -v pixi >/dev/null 2>&1; then
  python_cmd="pixi run python"
elif [ -x "$project_root/.venv/bin/python3" ]; then
  python_cmd="$project_root/.venv/bin/python3"
elif [ -x "$project_root/.venv/bin/python" ]; then
  python_cmd="$project_root/.venv/bin/python"
else
  python_cmd="python3"
fi

cd "$project_root"
SCRIPT_DIR="$script_dir" $python_cmd - <<'PY'
import json
import os
import sys

sys.path.insert(0, os.environ["SCRIPT_DIR"])
import michelin

rows = michelin.build_country_metrics().sort("stars_per_100k", descending=True)
print(json.dumps(rows.to_dicts(), ensure_ascii=False))
PY
