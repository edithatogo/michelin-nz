#!/usr/bin/env python3
import csv
from pathlib import Path

LEDGER_PATH = Path("src/data/aggregate_country_ledger.csv")
OFFICIAL_COVERAGE_PATH = Path("src/data/official_michelin_guide_coverage.csv")
VALID_COVERAGE_STATUSES = {"starred", "official-no-stars"}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    ledger_rows = read_rows(LEDGER_PATH)
    official_rows = read_rows(OFFICIAL_COVERAGE_PATH)
    ledger_codes = {row["country"] for row in ledger_rows}
    ledger_star_codes = {row["country"] for row in ledger_rows if int(row["total_stars"]) > 0}

    invalid_statuses = sorted(
        {
            row["coverage_status"]
            for row in official_rows
            if row["coverage_status"] not in VALID_COVERAGE_STATUSES
        },
    )
    if invalid_statuses:
        raise SystemExit(f"Invalid official coverage statuses: {', '.join(invalid_statuses)}")

    missing_starred = sorted(
        {
            row["ledger_country"]
            for row in official_rows
            if row["coverage_status"] == "starred"
            and row["ledger_country"] not in ledger_star_codes
        },
    )
    if missing_starred:
        raise SystemExit(
            "Official starred Michelin markets missing from aggregate ledger: "
            + ", ".join(missing_starred),
        )

    undocumented_zero_star = sorted(
        {
            row["ledger_country"]
            for row in official_rows
            if row["coverage_status"] == "official-no-stars"
            and row["ledger_country"] in ledger_codes
        },
    )
    if undocumented_zero_star:
        raise SystemExit(
            "Official no-star markets should not appear as star-bearing ledger rows: "
            + ", ".join(undocumented_zero_star),
        )

    coverage_codes = {row["ledger_country"] for row in official_rows}
    extra_ledger_codes = sorted(ledger_codes.difference(coverage_codes))
    if "NZL" not in extra_ledger_codes:
        raise SystemExit(
            "New Zealand benchmark row must remain explicitly outside official coverage."
        )

    print(
        "OK Official Michelin coverage reconciles with aggregate star ledger "
        f"({len(official_rows)} official markets, {len(ledger_rows)} ledger rows).",
    )


if __name__ == "__main__":
    main()
