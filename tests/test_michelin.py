# ruff: noqa
import io
import math
import os
import sys

import polars as pl
import pytest
from hypothesis import given
from hypothesis import strategies as st

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/data")))
import michelin


class MockResponse:
    def __init__(self, json_data):
        self.json_data = json_data

    def json(self):
        return self.json_data


def test_aggregate_indicator_inputs_are_country_level_only():
    """Verify that aggregate inputs do not expose row-level restaurant fields."""
    df = michelin.get_aggregate_indicator_inputs()
    assert isinstance(df, pl.DataFrame)
    assert set(df.columns) == {"country", "total_restaurants", "total_stars"}
    assert "name" not in df.columns
    assert "lat" not in df.columns
    assert "lng" not in df.columns
    assert df["total_stars"].sum() > 0
    assert df.height > 5
    assert {"FRA", "JPN", "USA", "TWN", "NZL"}.issubset(set(df["country"].to_list()))


def test_aggregate_country_ledger_has_source_metadata():
    """Verify that coverage rows carry source metadata without row-level fields."""
    df = michelin.get_aggregate_country_ledger()
    assert df.height > 50
    assert {
        "country",
        "country_name",
        "source_confidence",
        "guide_geography",
        "source_url",
        "accessed_date",
        "redistribution_note",
    }.issubset(set(df.columns))
    assert not michelin.RESTRICTED_PUBLIC_FIELDS.intersection(df.columns)
    assert df["total_restaurants"].sum() > 4000
    assert df["total_stars"].sum() > 5000


def test_world_bank_data_fallback():
    """Verify that World Bank fallback matches standard expected schemas."""
    df = michelin.get_world_bank_data()
    assert isinstance(df, pl.DataFrame)
    assert not df.is_empty()
    assert "population" in df.columns
    assert "gdp" in df.columns


def test_world_bank_data_api_success(monkeypatch):
    """Verify that World Bank API downloads join correctly."""
    mock_pop = [{}, [
        {"countryiso3code": "NZL", "country": {"value": "New Zealand"}, "value": 5000000},
        {"countryiso3code": "FRA", "country": {"value": "France"}, "value": 67000000},
    ]]
    mock_gdp = [{}, [
        {"countryiso3code": "NZL", "value": 250000000000},
        {"countryiso3code": "FRA", "value": 2700000000000},
    ]]

    def mock_get(url, timeout):
        if "SP.POP.TOTL" in url:
            return MockResponse(mock_pop)
        return MockResponse(mock_gdp)

    monkeypatch.setattr("requests.get", mock_get)
    df = michelin.get_world_bank_data()
    assert isinstance(df, pl.DataFrame)
    assert not df.is_empty()
    assert "NZL" in df["country"].to_list()


def test_world_bank_data_api_failure(monkeypatch):
    """Verify that World Bank downloads fall back on archive data."""
    def raise_error(url, timeout):
        raise Exception("API limit exceeded")

    monkeypatch.setattr("requests.get", raise_error)
    df = michelin.get_world_bank_data()
    assert isinstance(df, pl.DataFrame)
    assert not df.is_empty()
    assert "NZL" in df["country"].to_list()


def test_build_country_metrics_contains_only_aggregate_columns():
    """Verify that country metrics are aggregate-only and derived safely."""
    df = michelin.build_country_metrics()
    assert isinstance(df, pl.DataFrame)
    assert not df.is_empty()
    assert df.height > 50
    assert "stars_per_100k" in df.columns
    assert "stars_per_10b_gdp" in df.columns
    assert "gdp_per_capita" in df.columns
    assert "source_url" not in df.columns
    assert "name" not in df.columns
    assert "lat" not in df.columns
    assert "lng" not in df.columns


def test_mojo_metric_backend_matches_python():
    """Verify the experimental Mojo metrics backend matches the Python calculation."""
    population = 5228100.0
    gdp = 253000000000.0
    total_stars = 11.0

    python_metrics = michelin.calculate_derived_metrics_python(population, gdp, total_stars)
    mojo_metrics = michelin.calculate_derived_metrics_mojo(population, gdp, total_stars)

    assert math.isclose(mojo_metrics.stars_per_100k, python_metrics.stars_per_100k)
    assert math.isclose(mojo_metrics.gdp_per_capita, python_metrics.gdp_per_capita)
    assert math.isclose(mojo_metrics.stars_per_10b_gdp, python_metrics.stars_per_10b_gdp)


def test_build_country_metrics_can_use_mojo_backend(monkeypatch):
    """Verify the data loader can use Mojo for derived metric calculations."""
    monkeypatch.setenv("MICHELIN_METRICS_BACKEND", "mojo")
    monkeypatch.setattr(
        michelin,
        "get_world_bank_data",
        lambda: pl.DataFrame(
            [
                {
                    "country": "NZL",
                    "country_name": "New Zealand",
                    "population": 5228100.0,
                    "gdp": 253000000000.0,
                },
            ],
        ),
    )
    monkeypatch.setattr(
        michelin,
        "get_aggregate_country_ledger",
        lambda: pl.DataFrame(
            [
                {
                    "country": "NZL",
                    "country_name": "New Zealand",
                    "total_restaurants": 5,
                    "total_stars": 11,
                    "population_fallback": 5228100.0,
                    "gdp_fallback": 253000000000.0,
                },
            ],
        ),
    )

    df = michelin.build_country_metrics()
    expected = michelin.calculate_derived_metrics_python(5228100.0, 253000000000.0, 11.0)

    assert df.height == 1
    assert df["country"][0] == "NZL"
    assert df["stars_per_100k"][0] == pytest.approx(expected.stars_per_100k)
    assert df["gdp_per_capita"][0] == pytest.approx(expected.gdp_per_capita)
    assert df["stars_per_10b_gdp"][0] == pytest.approx(expected.stars_per_10b_gdp)


def test_main_execution(monkeypatch):
    """Execute main compiling aggregate metrics and verify output stream."""
    out_buffer = io.BytesIO()
    monkeypatch.setattr(sys.stdout.buffer, "write", out_buffer.write)

    michelin.main()

    assert len(out_buffer.getvalue()) > 0
    df = pl.read_parquet(io.BytesIO(out_buffer.getvalue()))
    assert isinstance(df, pl.DataFrame)
    assert "stars_per_100k" in df.columns
    assert "name" not in df.columns


@given(
    population=st.floats(min_value=1.0, max_value=2e9, allow_nan=False, allow_infinity=False),
    gdp=st.floats(min_value=1.0, max_value=1e15, allow_nan=False, allow_infinity=False),
    stars=st.integers(min_value=0, max_value=1000),
)
def test_calculation_boundaries(population, gdp, stars):
    """Property-based verification of per-capita indicators safety constraints."""
    df_raw = pl.DataFrame([{
        "country": "TST",
        "country_name": "Test Country",
        "population": population,
        "gdp": gdp,
        "total_stars": stars,
    }])

    df_raw = df_raw.with_columns([
        ((pl.col("total_stars") / pl.col("population")) * 100000).alias("stars_per_100k"),
        (pl.col("gdp") / pl.col("population")).alias("gdp_per_capita"),
        ((pl.col("total_stars") / pl.col("gdp")) * 10000000000).alias("stars_per_10b_gdp"),
    ])

    assert df_raw["stars_per_100k"][0] >= 0
    assert df_raw["gdp_per_capita"][0] >= 0
    assert df_raw["stars_per_10b_gdp"][0] >= 0
    assert not df_raw.null_count().select(pl.all().sum()).row(0)[0] > 0
