#!/usr/bin/env python3
import json
import os
import sys
from typing import Any


def main():
    reviews_dir = os.path.join(os.path.dirname(__file__), "reviews")
    combined_reviews: list[Any] = []

    if os.path.exists(reviews_dir):
        for filename in os.listdir(reviews_dir):
            if filename.endswith(".json"):
                filepath = os.path.join(reviews_dir, filename)
                try:
                    with open(filepath, encoding="utf-8") as f:
                        review_data = json.load(f)
                        combined_reviews.append(review_data)
                except Exception as e:
                    sys.stderr.write(f"Warning: Failed to parse review {filename}: {e}\n")

    # Write combined reviews output
    output_path = os.path.join(os.path.dirname(__file__), "community_reviews.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(combined_reviews, f, indent=2)
    sys.stdout.write(f"Successfully compiled {len(combined_reviews)} reviews.\n")


if __name__ == "__main__":
    main()
