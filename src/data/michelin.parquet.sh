#!/bin/bash
# Force execution using local virtual environment python
# Resolve project directory relative to script location
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"$DIR/../../.venv/bin/python3" "$DIR/michelin.py"
