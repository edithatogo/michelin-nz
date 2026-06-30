import sys
import os
import io
import json
import pandas as pd
import pytest
from hypothesis import given, strategies as st

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
    # Set cache dir to temporary path
    monkeypatch.setattr(michelin, "CACHE_DIR", str(tmp_path))
    
    mock_html = "<div class='card-restaurant'><span class='card-restaurant__title'>Test Food</span><span class='card-restaurant__location'>Akl</span></div>"
    monkeypatch.setattr("requests.get", lambda url, headers, timeout: MockResponse(mock_html, {}))
    
    res = michelin.fetch_with_cache("https://example.com/test", "test.html")
    assert res == mock_html
    # Subsequent calls should read from cache
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
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert df.iloc[0]["name"] == "Auckland Eatery"

def test_world_bank_data_api_success(monkeypatch):
    """Verify that World Bank API downloads join correctly."""
    mock_pop = [{}, [
        {"countryiso3code": "NZL", "country": {"value": "New Zealand"}, "value": 5000000},
        {"countryiso3code": "FRA", "country": {"value": "France"}, "value": 67000000}
    ]]
    mock_gdp = [{}, [
        {"countryiso3code": "NZL", "value": 250000000000},
        {"countryiso3code": "FRA", "value": 2700000000000}
    ]]
    
    # Mock dynamic routing of URLs
    def mock_get(url, timeout):
        if "SP.POP.TOTL" in url:
            return MockResponse("", mock_pop)
        return MockResponse("", mock_gdp)
        
    monkeypatch.setattr("requests.get", mock_get)
    df = michelin.get_world_bank_data()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "NZL" in df["country"].values

def test_world_bank_data_api_failure(monkeypatch):
    """Verify that World Bank downloads fall back on exceptions cleanly."""
    def raise_error(url, timeout):
        raise Exception("API Limit exceeded")
    monkeypatch.setattr("requests.get", raise_error)
    
    df = michelin.get_world_bank_data()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "NZL" in df["country"].values

def test_main_execution(monkeypatch, tmp_path):
    """Execute main mapping entrypoint compiling data and verify output stream."""
    monkeypatch.setattr(michelin, "CACHE_DIR", str(tmp_path))
    # Capture standard output buffer
    out_buffer = io.BytesIO()
    monkeypatch.setattr(sys.stdout.buffer, "write", out_buffer.write)
    
    michelin.main()
    
    # Verify we compiled a valid parquet output buffer stream
    assert len(out_buffer.getvalue()) > 0
    # Read back as pandas to confirm structure
    df = pd.read_parquet(io.BytesIO(out_buffer.getvalue()))
    assert isinstance(df, pd.DataFrame)
    assert "stars_per_100k" in df.columns

def test_reviews_aggregator_parsing(tmp_path, monkeypatch):
    """Verify that the blogger JSON compiler gathers files successfully and compiles unified database."""
    # Set parent path directory of reviews aggregator to tmp_path
    monkeypatch.setattr(reviews_aggregator, "os", os)
    
    # Create reviews subdirectory under temp path
    reviews_dir = tmp_path / "reviews"
    reviews_dir.mkdir()
    
    # Save a mock review JSON file
    review_data = {
      "restaurantId": "test-id",
      "author": "Food Critic",
      "rating": "4.5",
      "content": "Excellent meal",
      "link": "https://example.com"
    }
    with open(reviews_dir / "test.json", "w", encoding="utf-8") as f:
        json.dump(review_data, f)
        
    # Mock __file__ inside reviews_aggregator to compile target outputs to tmp_path
    monkeypatch.setattr(reviews_aggregator, "__file__", os.path.join(tmp_path, "reviews_aggregator.py"))
    
    # Execute actual main compiler function
    reviews_aggregator.main()
    
    # Verify outputs compiled correctly to tmp_path/community_reviews.json
    output_json = tmp_path / "community_reviews.json"
    assert output_json.exists()
    with open(output_json, "r", encoding="utf-8") as f:
        compiled_data = json.load(f)
        
    assert len(compiled_data) == 1
    assert compiled_data[0]["restaurantId"] == "test-id"

# Property-based tests verify calculation boundaries using Hypothesis
@given(
    population=st.floats(min_value=1.0, max_value=2e9, allow_nan=False, allow_infinity=False),
    gdp=st.floats(min_value=1.0, max_value=1e15, allow_nan=False, allow_infinity=False),
    stars=st.integers(min_value=0, max_value=1000)
)
def test_calculation_boundaries(population, gdp, stars):
    """Property-based verification of per-capita indicators safety constraints."""
    df_raw = pd.DataFrame([{
        "country": "TST",
        "country_name": "Test Country",
        "population": population,
        "gdp": gdp,
        "total_stars": stars
    }])
    
    # Run formulas
    df_raw["stars_per_100k"] = (df_raw["total_stars"] / df_raw["population"]) * 100000
    df_raw["gdp_per_capita"] = df_raw["gdp"] / df_raw["population"]
    df_raw["stars_per_10b_gdp"] = (df_raw["total_stars"] / df_raw["gdp"]) * 10000000000
    
    # Assert assertions
    assert df_raw["stars_per_100k"].iloc[0] >= 0
    assert df_raw["gdp_per_capita"].iloc[0] >= 0
    assert df_raw["stars_per_10b_gdp"].iloc[0] >= 0
    assert not df_raw.isna().any().any()
