#!/bin/sh
set -eu

script_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
project_root="$(CDPATH= cd -- "$script_dir/../.." && pwd)"

if [ -x "$project_root/.venv/bin/python3" ]; then
  python_bin="$project_root/.venv/bin/python3"
elif [ -x "$project_root/.venv/bin/python" ]; then
  python_bin="$project_root/.venv/bin/python"
else
  python_bin="python3"
fi

"$python_bin" "$script_dir/reviews_aggregator.py" > /dev/null
cat "$script_dir/community_reviews.json"
