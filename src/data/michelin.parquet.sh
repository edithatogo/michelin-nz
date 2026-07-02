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
$python_cmd "$script_dir/michelin.py"
