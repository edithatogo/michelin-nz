#!/usr/bin/env python3
import io
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import polars as pl
import requests

COUNTRY_SCALE = 100000
GDP_SCALE = 10000000000
MOJO_METRIC_FIELD_COUNT = 3
REPO_ROOT = Path(__file__).resolve().parents[2]
MOJO_METRICS_PATH = REPO_ROOT / "src" / "data" / "metrics.mojo"
AGGREGATE_COUNTRY_LEDGER_PATH = REPO_ROOT / "src" / "data" / "aggregate_country_ledger.csv"
AGGREGATE_INPUT_COLUMNS = ["country", "total_restaurants", "total_stars"]
STAR_TIER_COLUMNS = [
    "one_star_restaurants",
    "two_star_restaurants",
    "three_star_restaurants",
]
RESTRICTED_PUBLIC_FIELDS = {
    "address",
    "booking_url",
    "latitude",
    "longitude",
    "name",
    "review_text",
}

# Define cache dir
CACHE_DIR = os.path.join(os.path.dirname(__file__), ".cache")
os.makedirs(CACHE_DIR, exist_ok=True)


@dataclass(frozen=True)
class DerivedMetrics:
    """Derived aggregate dashboard metrics for one country row."""

    stars_per_100k: float
    gdp_per_capita: float
    stars_per_10b_gdp: float


def calculate_derived_metrics_python(
    population: float,
    gdp: float,
    total_stars: float,
) -> DerivedMetrics:
    """Calculate aggregate dashboard ratios in Python."""
    if population <= 0:
        raise ValueError("population must be positive")
    if gdp <= 0:
        raise ValueError("gdp must be positive")
    return DerivedMetrics(
        stars_per_100k=(total_stars / population) * COUNTRY_SCALE,
        gdp_per_capita=gdp / population,
        stars_per_10b_gdp=(total_stars / gdp) * GDP_SCALE,
    )


def calculate_derived_metrics_mojo(
    population: float,
    gdp: float,
    total_stars: float,
) -> DerivedMetrics:
    """Calculate aggregate dashboard ratios by delegating to the Mojo metrics executable."""
    result = subprocess.run(
        [
            "pixi",
            "run",
            "mojo",
            str(MOJO_METRICS_PATH),
            str(population),
            str(gdp),
            str(total_stars),
        ],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    output_lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    if not output_lines:
        raise RuntimeError("Mojo metrics executable produced no output")
    values = output_lines[-1].split()
    if len(values) != MOJO_METRIC_FIELD_COUNT:
        raise RuntimeError(f"Unexpected Mojo metrics output: {output_lines[-1]}")
    return DerivedMetrics(
        stars_per_100k=float(values[0]),
        gdp_per_capita=float(values[1]),
        stars_per_10b_gdp=float(values[2]),
    )


def calculate_derived_metrics(
    population: float,
    gdp: float,
    total_stars: float,
) -> DerivedMetrics:
    """Calculate derived metrics with the configured experimental backend."""
    if os.environ.get("MICHELIN_METRICS_BACKEND", "python").lower() == "mojo":
        return calculate_derived_metrics_mojo(population, gdp, total_stars)
    return calculate_derived_metrics_python(population, gdp, total_stars)


def get_world_bank_data() -> pl.DataFrame:
    """Fetches population and GDP stats from World Bank APIs."""
    pop_url = "http://api.worldbank.org/v2/country/all/indicator/SP.POP.TOTL?format=json&per_page=300&date=2024"
    gdp_url = "http://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.CD?format=json&per_page=300&date=2024"

    pop_data: list[dict[str, object]] = []
    gdp_data: list[dict[str, object]] = []

    try:
        r_pop = requests.get(pop_url, timeout=10).json()
        if len(r_pop) > 1 and r_pop[1] is not None:
            for item in r_pop[1]:
                pop_data.append(
                    {
                        "country": item["countryiso3code"],
                        "country_name": item["country"]["value"],
                        "population": float(item["value"]) if item["value"] is not None else None,
                    },
                )
    except Exception as e:
        sys.stderr.write(f"Error fetching World Bank pop data: {e}\n")

    try:
        r_gdp = requests.get(gdp_url, timeout=10).json()
        if len(r_gdp) > 1 and r_gdp[1] is not None:
            for item in r_gdp[1]:
                gdp_data.append(
                    {
                        "country": item["countryiso3code"],
                        "gdp": float(item["value"]) if item["value"] is not None else None,
                    },
                )
    except Exception as e:
        sys.stderr.write(f"Error fetching World Bank GDP data: {e}\n")

    if not pop_data:
        pop_archive = os.path.join(
            os.path.dirname(__file__),
            "archive",
            "world_bank_population_2024.json",
        )
        pop_data = pl.read_json(pop_archive).to_dicts()

    if not gdp_data:
        gdp_archive = os.path.join(
            os.path.dirname(__file__),
            "archive",
            "world_bank_gdp_2024.json",
        )
        gdp_data = pl.read_json(gdp_archive).to_dicts()

    df_pop = pl.DataFrame(pop_data)
    df_gdp = pl.DataFrame(gdp_data)

    if df_pop.is_empty() or df_gdp.is_empty():
        return pl.DataFrame()

    return df_pop.join(df_gdp, on="country", how="left")


def get_aggregate_indicator_inputs() -> pl.DataFrame:
    """Returns aggregate country-level indicator inputs without row-level records."""
    return get_aggregate_country_ledger().select(AGGREGATE_INPUT_COLUMNS)


def get_aggregate_country_ledger() -> pl.DataFrame:
    """Load and validate the repo-local aggregate country coverage ledger."""
    ledger = pl.read_csv(AGGREGATE_COUNTRY_LEDGER_PATH)
    restricted_columns = RESTRICTED_PUBLIC_FIELDS.intersection(ledger.columns)
    if restricted_columns:
        columns = ", ".join(sorted(restricted_columns))
        raise ValueError(f"Coverage ledger contains restricted row-level fields: {columns}")

    required_columns = {
        "country",
        "country_name",
        "total_restaurants",
        "total_stars",
        *STAR_TIER_COLUMNS,
        "source_confidence",
        "guide_geography",
        "source_url",
        "accessed_date",
        "redistribution_note",
        "population_fallback",
        "gdp_fallback",
    }
    missing_columns = required_columns.difference(ledger.columns)
    if missing_columns:
        columns = ", ".join(sorted(missing_columns))
        raise ValueError(f"Coverage ledger is missing required columns: {columns}")

    duplicate_codes = (
        ledger.group_by("country").len().filter(pl.col("len") > 1).get_column("country").to_list()
    )
    if duplicate_codes:
        codes = ", ".join(str(code) for code in duplicate_codes)
        raise ValueError(f"Coverage ledger contains duplicate country codes: {codes}")

    return ledger.with_columns(
        [
            pl.col("total_restaurants").cast(pl.Int64),
            pl.col("total_stars").cast(pl.Int64),
            pl.col("one_star_restaurants").cast(pl.Int64),
            pl.col("two_star_restaurants").cast(pl.Int64),
            pl.col("three_star_restaurants").cast(pl.Int64),
            pl.col("population_fallback").cast(pl.Float64),
            pl.col("gdp_fallback").cast(pl.Float64),
        ],
    )


def build_country_metrics() -> pl.DataFrame:
    """Builds country-level per-capita and per-GDP aggregate metrics."""
    df_ledger = get_aggregate_country_ledger()
    df_aggregate_inputs = df_ledger.select(
        [
            "country",
            "country_name",
            "total_restaurants",
            "total_stars",
            *STAR_TIER_COLUMNS,
            "population_fallback",
            "gdp_fallback",
        ],
    )
    df_demographics = get_world_bank_data()

    df_merged = df_aggregate_inputs.join(df_demographics, on="country", how="left")
    df_merged = df_merged.with_columns(
        [
            pl.col("total_restaurants").fill_null(0).cast(pl.Int64),
            pl.col("total_stars").fill_null(0).cast(pl.Int64),
            pl.col("one_star_restaurants").fill_null(0).cast(pl.Int64),
            pl.col("two_star_restaurants").fill_null(0).cast(pl.Int64),
            pl.col("three_star_restaurants").fill_null(0).cast(pl.Int64),
            pl.coalesce([pl.col("population"), pl.col("population_fallback")]).alias(
                "population",
            ),
            pl.coalesce([pl.col("gdp"), pl.col("gdp_fallback")]).alias("gdp"),
        ],
    )
    missing_demographics = df_merged.filter(
        pl.col("population").is_null() | pl.col("gdp").is_null(),
    )
    if not missing_demographics.is_empty():
        codes = ", ".join(str(code) for code in missing_demographics.get_column("country"))
        raise ValueError(f"Missing population or GDP values for coverage ledger rows: {codes}")

    if os.environ.get("MICHELIN_METRICS_BACKEND", "python").lower() == "mojo":
        rows: list[dict[str, object]] = []
        for row in df_merged.to_dicts():
            metrics = calculate_derived_metrics(
                float(row["population"]),
                float(row["gdp"]),
                float(row["total_stars"]),
            )
            rows.append(
                {
                    "country": row["country"],
                    "country_name": row["country_name"],
                    "population": row["population"],
                    "gdp": row["gdp"],
                    "total_restaurants": row["total_restaurants"],
                    "total_stars": row["total_stars"],
                    "one_star_restaurants": row["one_star_restaurants"],
                    "two_star_restaurants": row["two_star_restaurants"],
                    "three_star_restaurants": row["three_star_restaurants"],
                    "stars_per_100k": metrics.stars_per_100k,
                    "gdp_per_capita": metrics.gdp_per_capita,
                    "stars_per_10b_gdp": metrics.stars_per_10b_gdp,
                },
            )
        df_merged = pl.DataFrame(rows)
    else:
        df_merged = df_merged.with_columns(
            [
                ((pl.col("total_stars") / pl.col("population")) * COUNTRY_SCALE).alias(
                    "stars_per_100k",
                ),
                (pl.col("gdp") / pl.col("population")).alias("gdp_per_capita"),
                ((pl.col("total_stars") / pl.col("gdp")) * GDP_SCALE).alias(
                    "stars_per_10b_gdp",
                ),
            ],
        )

    return df_merged.filter(
        pl.col("population").is_not_null() & (pl.col("total_stars") > 0),
    ).select(
        [
            "country",
            "country_name",
            "population",
            "gdp",
            "total_restaurants",
            "total_stars",
            *STAR_TIER_COLUMNS,
            "stars_per_100k",
            "gdp_per_capita",
            "stars_per_10b_gdp",
        ],
    )


def main() -> None:
    df_merged = build_country_metrics()

    # 4. Stream Parquet structure directly to stdout
    buffer = io.BytesIO()
    df_merged.write_parquet(buffer)
    sys.stdout.buffer.write(buffer.getvalue())


if __name__ == "__main__":
    main()
