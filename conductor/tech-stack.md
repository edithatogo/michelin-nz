# Technology Stack: Michelin Star Per-Capita Dashboard

## Frontend & Visualizations
* **Core Framework:** [Observable Framework](https://observablehq.com/framework/) - Static site generator designed specifically for data apps, dashboards, and reports. It includes built-in support for data loaders (runs build-time data prep) and features instant routing and page updates.
* **Visualization Engines (Non-Redundant):**
  - [Observable Plot](https://observablehq.com/plot/) - Primary charting library for standard statistical charts (scatters, bars, histograms).
  - [Cosmograph](https://cosmograph.app/) (cosmos.gl) - Primary GPU-accelerated force layout engine for node-link chef networks.
  - [Unovis](https://unovis.dev/) - For custom relational representations (chord, cluster relationships) where Observable Plot is insufficient.
* **In-Browser Database & State Coordination:** [DuckDB WASM](https://duckdb.org/docs/api/wasm/overview) & [SQLRooms](https://sqlrooms.org/) - Unified data client. All client filtering, sorting, and selections execute SQL queries on the loaded Parquet data. All visual components (Plot, Deck.gl, Cosmograph) subscribe to SQLRooms state to prevent state duplication.
* **GPU Mapping & Acceleration:** [Deck.gl](https://deck.gl/) - Primary mapping interface rendering spatial queries directly from DuckDB. No other standalone mapping engines (like Leaflet) are imported.
* **AI Assistance:** Hugging Face Inference API client for natural language queries translated to client-side SQL.
* **Styling:** Vanilla CSS & View Transitions API, styled with custom dark-mode properties aligned with our Sleek Dark theme.

## Data Processing & Triangulation Pipeline
* **Build-time Data Loaders:** Written in **Python** (using `pandas`, `requests`, and `beautifulsoup4` or `playwright` for scraping). Data loaders run during compilation to scrape, merge, and clean Michelin star records alongside demographic data (World Bank/UN population and GDP stats), outputting highly compressed **Parquet** files directly into the frontend bundle.
* **Scraper Resilience:** Cache raw HTML locally during development builds, cycle headers/user-agents, use polite request pacing, and integrate structural fail-safes (fallback to static data if live scraping encounters blocking or network failure).
* **Map Optimization:** [Mapshaper](https://github.com/mbloch/mapshaper) - Command-line pipeline tool utilized during compilation to clean and simplify geographic boundaries into high-performance custom TopoJSON layers.
* **Data Sources for Triangulation:**
  - Kaggle/GitHub historic Michelin restaurant databases.
  - Official Michelin Guide website scraping (specifically for New Zealand and recent guide releases).
  - World Bank / UN Open Data APIs for population, GDP, and GDP per capita.

## Deployment, Testing & CI/CD
* **Platform:** Hugging Face Spaces (Static Docker or Node space) to host the compiled Observable Framework static build.
* **Git Verification:** Husky & lint-staged blocking commits that violate lint/type rules.
* **QA & Testing:** Playwright running visual regression tests in GitHub Actions on every Pull Request.
* **CI/CD:** GitHub Actions scheduled weekly trigger to fetch new Michelin ratings, build, run verification, and sync build output to Hugging Face production. Open PRs trigger deployment previews on Hugging Face.
