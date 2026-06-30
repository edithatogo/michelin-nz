#!/bin/bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"$DIR/../../.venv/bin/python3" "$DIR/reviews_aggregator.py" > /dev/null
cat "$DIR/community_reviews.json"
