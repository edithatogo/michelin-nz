# Contributing to the Aggregate Dashboard

This project now accepts aggregate-only changes. Contributions should improve methodology,
country-level indicators, documentation, charting, accessibility, testing, or deployment.

Do not submit individual restaurant records, review snippets, coordinates, guide text, photos,
booking metadata, scraped Michelin pages, or other source rows derived from proprietary guides.

## Acceptable Contributions

1. Country-level aggregate metrics with clear provenance and a redistribution basis.
2. Reproducible analysis code that calculates ratios from aggregate inputs.
3. Documentation that explains assumptions, data limitations, licensing, and methodology.
4. UI improvements for the existing aggregate dashboard pages.
5. Tests, CI fixes, accessibility fixes, and deployment improvements.

## Data Requirements

Any data contribution must include:

1. The source name and URL.
2. The exact fields used.
3. The permission, license, or public-domain basis for using the data.
4. A note confirming that no individual restaurant-level or review-level records are included.

## Developer Workflow

1. Fork the repo and create a branch such as `feat/aggregate-methodology`.
2. Follow the coding guidelines inside `conductor/code_styleguides/`.
3. Run the local checks before opening a pull request:

```bash
npm run lint
OBSERVABLE_TELEMETRY_DISABLE=true npm run build
npm run smoke:dist
.venv/bin/ruff check src/data/ tests/ scripts/check_external_deployments.py
.venv/bin/pytest --cov=src/data --cov-fail-under=85
npx basedpyright src/data/
```
