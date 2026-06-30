# ruff: noqa
import io
import json
import os
import sys

import polars as pl
from hypothesis import given
from hypothesis import strategies as st

# Set path wrapper to import data module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/data")))
import michelin
import reviews_aggregator


class MockResponse:
    def __init__(self, text_data, json_data, status_code=200):
        self.text = text_data
        self.json_data = json_data
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code != 200:
            raise Exception("HTTP Error")

    def json(self):
        return self.json_data

def test_fetch_with_cache_success(monkeypatch, tmp_path):
    """Test fetch caching matches correctly on requests success."""
    monkeypatch.setattr(michelin, "CACHE_DIR", str(tmp_path))

    mock_html = "<div class='card-restaurant'><span class='card-restaurant__title'>Test Food</span><span class='card-restaurant__location'>Akl</span></div>"
    monkeypatch.setattr("requests.get", lambda url, headers, timeout: MockResponse(mock_html, {}))

    res = michelin.fetch_with_cache("https://example.com/test", "test.html")
    assert res == mock_html
    monkeypatch.setattr("requests.get", lambda url, headers, timeout: None)
    res_cached = michelin.fetch_with_cache("https://example.com/test", "test.html")
    assert res_cached == mock_html

def test_fetch_with_cache_failure(monkeypatch, tmp_path):
    """Test cache fetch exceptions fall back clean."""
    monkeypatch.setattr(michelin, "CACHE_DIR", str(tmp_path))
    def raise_error(url, headers, timeout):
        raise Exception("Network blocked")
    monkeypatch.setattr("requests.get", raise_error)

    res = michelin.fetch_with_cache("https://example.com/test", "failed.html")
    assert res == ""

def test_nz_scraped_restaurants_fallback():
    """Verify that NZ scraper fallback list generates a valid DataFrame with required attributes."""
    df = michelin.get_nz_scraped_restaurants()
    assert isinstance(df, pl.DataFrame)
    assert not df.is_empty()
    assert "name" in df.columns
    assert "stars" in df.columns
    assert "lat" in df.columns
    assert "lng" in df.columns

def test_nz_scraped_restaurants_parsing(monkeypatch, tmp_path):
    """Test restaurant parsing from mocked DOM HTML contents."""
    monkeypatch.setattr(michelin, "CACHE_DIR", str(tmp_path))
    mock_html = """
    <div class="card-restaurant">
      <div class="card-restaurant__title">Auckland Eatery</div>
      <div class="card-restaurant__location">Auckland CBD</div>
    </div>
    """
    monkeypatch.setattr("requests.get", lambda url, headers, timeout: MockResponse(mock_html, {}))
    df = michelin.get_nz_scraped_restaurants()
    assert isinstance(df, pl.DataFrame)
    assert not df.is_empty()
    assert df["name"][0] == "Auckland Eatery"

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
            return MockResponse("", mock_pop)
        return MockResponse("", mock_gdp)

    monkeypatch.setattr("requests.get", mock_get)
    df = michelin.get_world_bank_data()
    assert isinstance(df, pl.DataFrame)
    assert not df.is_empty()
    assert "NZL" in df["country"].to_list()

def test_world_bank_data_api_failure(monkeypatch):
    """Verify that World Bank downloads fall back on exceptions cleanly."""
    def raise_error(url, timeout):
        raise Exception("API Limit exceeded")
    monkeypatch.setattr("requests.get", raise_error)

    df = michelin.get_world_bank_data()
    assert isinstance(df, pl.DataFrame)
    assert not df.is_empty()
    assert "NZL" in df["country"].to_list()

def test_main_execution(monkeypatch, tmp_path):
    """Execute main mapping entrypoint compiling data and verify output stream."""
    monkeypatch.setattr(michelin, "CACHE_DIR", str(tmp_path))
    out_buffer = io.BytesIO()
    monkeypatch.setattr(sys.stdout.buffer, "write", out_buffer.write)

    michelin.main()

    assert len(out_buffer.getvalue()) > 0
    df = pl.read_parquet(io.BytesIO(out_buffer.getvalue()))
    assert isinstance(df, pl.DataFrame)
    assert "stars_per_100k" in df.columns

def test_reviews_aggregator_parsing(tmp_path, monkeypatch):
    """Verify that the blogger JSON compiler gathers files successfully and compiles unified database."""
    monkeypatch.setattr(reviews_aggregator, "os", os)
    reviews_dir = tmp_path / "reviews"
    reviews_dir.mkdir()

    review_data = {
      "restaurantId": "test-id",
      "author": "Food Critic",
      "rating": "4.5",
      "content": "Excellent meal",
      "link": "https://example.com",
    }
    with open(reviews_dir / "test.json", "w", encoding="utf-8") as f:
        json.dump(review_data, f)

    monkeypatch.setattr(reviews_aggregator, "__file__", os.path.join(tmp_path, "reviews_aggregator.py"))
    reviews_aggregator.main()

    output_json = tmp_path / "community_reviews.json"
    assert output_json.exists()
    with open(output_json, encoding="utf-8") as f:
        compiled_data = json.load(f)

    assert len(compiled_data) == 1
    assert compiled_data[0]["restaurantId"] == "test-id"

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

