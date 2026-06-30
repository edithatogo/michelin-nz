#!/usr/bin/env python3
import io
import os
import sys

import polars as pl
import requests

COUNTRY_SCALE = 100000
GDP_SCALE = 10000000000

# Define cache dir
CACHE_DIR = os.path.join(os.path.dirname(__file__), ".cache")
os.makedirs(CACHE_DIR, exist_ok=True)


def get_world_bank_data() -> pl.DataFrame:
    """Fetches population and GDP stats from World Bank APIs."""
    pop_url = "http://api.worldbank.org/v2/country/all/indicator/SP.POP.TOTL?format=json&per_page=300&date=2024"
    gdp_url = "http://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.CD?format=json&per_page=300&date=2024"

    pop_data = []
    gdp_data = []

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
    return pl.DataFrame(
        [
            {"country": "CHE", "total_restaurants": 1, "total_stars": 3},
            {"country": "FRA", "total_restaurants": 2, "total_stars": 6},
            {"country": "JPN", "total_restaurants": 2, "total_stars": 6},
            {"country": "NZL", "total_restaurants": 5, "total_stars": 11},
            {"country": "USA", "total_restaurants": 2, "total_stars": 6},
        ],
    )


def build_country_metrics() -> pl.DataFrame:
    """Builds country-level per-capita and per-GDP aggregate metrics."""
    df_aggregate_inputs = get_aggregate_indicator_inputs()
    df_demographics = get_world_bank_data()

    df_merged = df_demographics.join(df_aggregate_inputs, on="country", how="inner")
    df_merged = df_merged.with_columns(
        [
            pl.col("total_restaurants").fill_null(0).cast(pl.Int64),
            pl.col("total_stars").fill_null(0).cast(pl.Int64),
        ],
    )

    # Calculations
    df_merged = df_merged.with_columns(
        [
            ((pl.col("total_stars") / pl.col("population")) * COUNTRY_SCALE).alias(
                "stars_per_100k",
            ),
            (pl.col("gdp") / pl.col("population")).alias("gdp_per_capita"),
            ((pl.col("total_stars") / pl.col("gdp")) * GDP_SCALE).alias("stars_per_10b_gdp"),
        ],
    )

    return df_merged.filter(
        pl.col("population").is_not_null() & (pl.col("total_stars") > 0),
    )


def main() -> None:
    df_merged = build_country_metrics()

    # 4. Stream Parquet structure directly to stdout
    buffer = io.BytesIO()
    df_merged.write_parquet(buffer)
    sys.stdout.buffer.write(buffer.getvalue())


if __name__ == "__main__":
    main()
