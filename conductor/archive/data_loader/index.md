# Track: Data Loader Pipeline & Scraping

## Overview
This track implements the data ingestion and preparation scripts. It sets up:
1. Web scrapers to extract live Michelin Star entries (focusing on New Zealand and missing guides).
2. Data normalization pipelines merging Kaggle historic data, scraped records, and UN/World Bank GDP & population parameters.
3. Auto-generation of compressed Parquet/JSON data assets inside `src/data/` for frontend use.

## Tasks

### [x] Task: Ingestion & Triangulation Scripts
*   **Action:** Create a Python script (`src/data/triangulate.py`) to parse local raw files, scrape Michelin Guide lists resiliently (caching HTML locally), and merge databases with ISO 3166 key codes.
*   **Verification:** Run Python validation checks to ensure zero-duplicate restaurants and check data integrity counts.
*   **Git Action:** Commit as `feat(data): implement multi-source michelin triangulation`.

### [x] Task: Demographic & Economic Normalization
*   **Action:** Incorporate World Bank API requests to download population and GDP figures. Compute Stars-per-Capita and Stars-per-GDP ratios.
*   **Verification:** Confirm final JSON/Parquet outputs exist and contain the target computed indices.
*   **Git Action:** Commit as `feat(data): integrate economic and demographic normalization`.

### [x] Task: Observable Build Integration
*   **Action:** Set up an Observable Data Loader file (`src/data/michelin.parquet.py`) that wraps the Python scripts so that running `npm run build` triggers data updates.
*   **Verification:** Run `npm run build` and check that the resulting bundle contains updated, verified data loader outputs.
*   **Git Action:** Commit as `feat(data): build observable framework data loader integration`.
