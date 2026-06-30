# Product Guide: Michelin Star Per-Capita Dashboard

## Vision
A visually stunning, data-driven dashboard that visualizes the distribution of Michelin-starred restaurants globally, adjusted for population, GDP, and geographic location. The project aims to identify fine-dining density hotspots (like Tokyo, Paris, and Singapore) and benchmark New Zealand's culinary standing relative to its population and economic capacity.

## Key Features
1. **Multi-Source Triangulation & Scraping Pipeline:**
   - Ingestion from public Michelin dataset repositories (e.g., Kaggle, GitHub).
   - Custom scraping script to fill in missing gaps and collect fresh data for New Zealand and newly rated regions.
   - Validation ledger matching scraped counts against official Michelin Guide numbers to ensure data integrity.
2. **Interactive Demographic Visualizations:**
   - **Global Choropleth Map / Zoomable WebGL Globe:** Visualization of Michelin Stars per 100,000 residents and stars per $10B GDP with WebGL acceleration (Maplibre GL or D3 Canvas) for 60fps zooming.
   - **Interactive DuckDB WASM Queries:** In-browser SQL engine querying compressed parquet data to power real-time multi-dimensional sliders.
   - **Scatter Plots:** Interactive correlation between GDP per capita (X) and Stars per capita (Y), enabling identification of culinary "outliers."
   - **Ridgeplots & Distribution Curves:** Comparing star density distribution within countries (showing central concentration vs. regional distribution).
   - **Influence Network Visualization:** Visualizing chef lineages and culinary style migrations across continents.
3. **New Zealand Geographic Analysis:**
   - A highly localized map showing New Zealand's top restaurants (stars or equivalent recommendations/hats) mapped against local regional populations.
4. **Interactive Dashboard UX & Deep Linking:**
   - Designed using **Astro/Observable Framework**, **Observable Plot**, and high-end interactive libraries.
   - Deep linking on each restaurant card to allow one-click directions (Google Maps, Apple Maps, OpenStreetMap) and official booking guides.
   - Aggregated review score summaries (pulling data from Google, OpenTable, etc.) with click-through links.
5. **Community Review CMS & Automation:**
   - PR-based contribution system allowing food bloggers, Substack writers, and social media critics to submit their reviews into flat-file database cards.
   - Automated daily web check via GitHub Actions to ingest new Michelin updates and check for newly published culinary reviews.
   - Fully deployed as a high-performance web app on **Hugging Face Spaces**.
