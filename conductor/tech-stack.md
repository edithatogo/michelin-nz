# Technology Stack: Aggregate Gastronomy Indicator Dashboard

## Frontend And Visualization

* **Observable Framework:** Static site generator for the data app.
* **Observable Plot:** Primary charting library for aggregate scatter, bar, and table views.
* **Vanilla JavaScript:** Lightweight controls for pivot filters and measure selection.
* **Vanilla CSS:** Responsive dashboard styling without extra UI framework weight.

## Data Processing

* **Python:** Build-time data loader in `src/data/michelin.py`.
* **Polars:** DataFrame operations and Parquet output.
* **Requests:** World Bank API access for aggregate country indicators.
* **Pytest and Hypothesis:** Unit and property testing for aggregate calculations.
* **Ruff and basedpyright:** Python linting and type checking.

## Data Scope

The pipeline combines public demographic/economic indicators with aggregate country-level
gastronomy counts. It does not publish source rows from proprietary guides, submitted review data,
or individual restaurant metadata.

## Deployment, Testing, And CI

* **GitHub Actions:** Runs linting, build, smoke tests, Python checks, and scheduled deployment.
* **Hugging Face Spaces:** Hosts the compiled static Observable build.
* **Static smoke tests:** Verify active routes and ensure removed routes are not shipped.
* **External deployment check:** Confirms GitHub and Hugging Face surfaces are reachable.
