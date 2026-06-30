# Track: Core Visualizations & DuckDB Integration

## Overview
This track integrates client-side database management and core chart layouts. It sets up:
1. DuckDB WASM and SQLRooms / Mosaic to query the local `.parquet` data loader assets.
2. Reactive HTML UI controllers (sliders, checkboxes) powered by SQL query filters.
3. Core statistical visual charts (e.g. GDP vs. Stars per-capita scatter plot) using Observable Plot.

## Tasks

### [x] Task: In-Browser SQL Ingest (DuckDB & SQLRooms)
*   **Action:** Install and import `duckdb-wasm` and wire up the database loading routine.
*   **Verification:** Ensure parquet data loads cleanly into client memory and can be queried via standard SQL statements.
*   **Git Action:** Commit as `feat(viz): integrate client-side duckdb WASM query client`.

### [x] Task: State & Filtering Controls (SQLRooms)
*   **Action:** Establish reactive controller components. Set up state listeners that trigger SQL query updates when sliders or menus change.
*   **Verification:** Verify console logging shows dynamic SQL updates.
*   **Git Action:** Commit as `feat(viz): implement reactive controls using SQLRooms unified state`.

### [x] Task: Observable Plot Charts
*   **Action:** Render the GDP vs Stars scatter plot and per-capita bar comparisons using Observable Plot, drawing directly from the SQL query outputs.
*   **Verification:** Test compilation build and inspect layout renders.
*   **Git Action:** Commit as `feat(viz): build GDP and stars correlation charts using Observable Plot`.
