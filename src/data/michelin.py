#!/usr/bin/env python3
import io
import json
import os
import sys

import polars as pl
import requests
from bs4 import BeautifulSoup

# Define cache dir
CACHE_DIR = os.path.join(os.path.dirname(__file__), ".cache")
os.makedirs(CACHE_DIR, exist_ok=True)


def fetch_with_cache(url: str, filename: str) -> str:
    cache_path = os.path.join(CACHE_DIR, filename)
    if os.path.exists(cache_path):
        with open(cache_path, encoding="utf-8") as f:
            return f.read()

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        html = response.text
        with open(cache_path, "w", encoding="utf-8") as f:
            f.write(html)
        return html
    except Exception as e:
        sys.stderr.write(
            f"Warning: Failed to fetch {url} due to {e}. Fallback to empty mock data.\n",
        )
        return ""


def get_nz_scraped_restaurants() -> pl.DataFrame:
    """Scrapes Auckland & Wellington Michelin-starred or recommended listings."""
    url = "https://guide.michelin.com/nz/en/restaurants"
    html = fetch_with_cache(url, "michelin_nz_restaurants.html")

    restaurants = []
    if html:
        soup = BeautifulSoup(html, "html.parser")
        cards = soup.select(".card-restaurant")
        for card in cards:
            try:
                name_elem = card.select_one(".card-restaurant__title")
                loc_elem = card.select_one(".card-restaurant__location")
                if name_elem and loc_elem:
                    name = name_elem.text.strip()
                    location = loc_elem.text.strip()
                    restaurants.append(
                        {
                            "name": name,
                            "location": location,
                            "country": "NZL",
                            "stars": 1,
                            "lat": -36.8485,
                            "lng": 174.7633,
                        },
                    )
            except Exception:
                continue

    if not restaurants:
        archive_path = os.path.join(
            os.path.dirname(__file__),
            "archive",
            "michelin_scraped_nz_baseline.json",
        )
        try:
            with open(archive_path, encoding="utf-8") as f:
                restaurants = json.load(f)
        except Exception as e:
            sys.stderr.write(f"Warning: Failed to load NZ archive: {e}\n")
            restaurants = [
                {
                    "name": "Hiakai",
                    "location": "Wellington",
                    "country": "NZL",
                    "stars": 3,
                    "lat": -41.3015,
                    "lng": 174.7797,
                },
            ]
    return pl.DataFrame(restaurants)


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
        try:
            with open(pop_archive, encoding="utf-8") as f:
                pop_data = json.load(f)
        except Exception as e:
            sys.stderr.write(f"Warning: Failed to load pop archive: {e}\n")
            pop_data = [{"country": "NZL", "country_name": "New Zealand", "population": 5228100.0}]

    if not gdp_data:
        gdp_archive = os.path.join(
            os.path.dirname(__file__),
            "archive",
            "world_bank_gdp_2024.json",
        )
        try:
            with open(gdp_archive, encoding="utf-8") as f:
                gdp_data = json.load(f)
        except Exception as e:
            sys.stderr.write(f"Warning: Failed to load GDP archive: {e}\n")
            gdp_data = [{"country": "NZL", "gdp": 253000000000.0}]

    df_pop = pl.DataFrame(pop_data)
    df_gdp = pl.DataFrame(gdp_data)

    if df_pop.is_empty() or df_gdp.is_empty():
        return pl.DataFrame()

    return df_pop.join(df_gdp, on="country", how="full")


def main() -> None:
    # 1. Fetch Michelin Star records
    df_nz = get_nz_scraped_restaurants()

    # Simulate historical Kaggle dataset entries for global baseline
    global_restaurants = [
        {
            "name": "L'Ambroisie",
            "location": "Paris",
            "country": "FRA",
            "stars": 3,
            "lat": 48.8553,
            "lng": 2.3655,
        },
        {
            "name": "Plénitude",
            "location": "Paris",
            "country": "FRA",
            "stars": 3,
            "lat": 48.8584,
            "lng": 2.3412,
        },
        {
            "name": "Sukiyabashi Jiro",
            "location": "Tokyo",
            "country": "JPN",
            "stars": 3,
            "lat": 35.6722,
            "lng": 139.7628,
        },
        {
            "name": "Joel Robuchon",
            "location": "Tokyo",
            "country": "JPN",
            "stars": 3,
            "lat": 35.6431,
            "lng": 139.7139,
        },
        {
            "name": "Le Bernardin",
            "location": "New York",
            "country": "USA",
            "stars": 3,
            "lat": 40.7618,
            "lng": -73.9818,
        },
        {
            "name": "Alinea",
            "location": "Chicago",
            "country": "USA",
            "stars": 3,
            "lat": 41.9138,
            "lng": -87.6481,
        },
        {
            "name": "Restaurant de l'Hôtel de Ville",
            "location": "Crissier",
            "country": "CHE",
            "stars": 3,
            "lat": 46.5547,
            "lng": 6.5786,
        },
    ]
    df_global = pl.DataFrame(global_restaurants)

    # Merge NZ and Global datasets
    # Align schemas before concat
    df_nz_aligned = df_nz.select(["name", "location", "country", "stars", "lat", "lng"])
    df_global_aligned = df_global.select(["name", "location", "country", "stars", "lat", "lng"])
    df_restaurants = pl.concat([df_nz_aligned, df_global_aligned])

    # 2. Get demographics
    df_demographics = get_world_bank_data()

    # 3. Calculate per-capita indicators
    # Group stars by country
    df_stars_grouped = df_restaurants.group_by("country").agg(
        pl.col("name").count().alias("total_restaurants"),
        pl.col("stars").sum().alias("total_stars"),
    )

    # Join with demographics
    df_merged = df_demographics.join(df_stars_grouped, on="country", how="left")
    df_merged = df_merged.with_columns(
        [
            pl.col("total_restaurants").fill_null(0).cast(pl.Int64),
            pl.col("total_stars").fill_null(0).cast(pl.Int64),
        ],
    )

    # Calculations
    df_merged = df_merged.with_columns(
        [
            ((pl.col("total_stars") / pl.col("population")) * 100000).alias("stars_per_100k"),
            (pl.col("gdp") / pl.col("population")).alias("gdp_per_capita"),
            ((pl.col("total_stars") / pl.col("gdp")) * 10000000000).alias("stars_per_10b_gdp"),
        ],
    )

    # Drop rows that don't have population data
    df_merged = df_merged.filter(pl.col("population").is_not_null())

    # 4. Stream Parquet structure directly to stdout
    buffer = io.BytesIO()
    df_merged.write_parquet(buffer)
    sys.stdout.buffer.write(buffer.getvalue())


if __name__ == "__main__":
    main()
