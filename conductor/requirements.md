# Requirements

This document is the Conductor requirements register for the aggregate-only Michelin Star
Per-Capita Dashboard. It uses MoSCoW priority so planned work, delivered work, and deferred work
can be checked against the same contract.

## Must Have

- Aggregate-only country analysis of Michelin star counts against population and GDP.
- Explicit public-data boundary: no restaurant names, reviews, addresses, booking links, photos,
  exact guide-derived coordinates, or proprietary source rows in public artifacts.
- Build-time data pipeline that emits deterministic JSON and Parquet assets for Observable
  Framework.
- Python 3.14 orchestration through Pixi for remaining Python code.
- Experimental Mojo metric backend for deterministic ratio calculations, with Python parity tests.
- Strict code quality gates for formatting, linting, typing, tests, coverage, npm audit, build,
  and static smoke checks.
- Hugging Face Spaces static deployment that serves all intended public routes.
- Live visual contract checks for route status, readable layout, chart presence, bounded controls,
  no horizontal overflow, and no clipped text.
- Repo-local Conductor tracks for country coverage, geographic outcomes, live quality scoring, and
  Mojo migration.
- Source, license, citation, and authorship documentation including ORCID
  `0000-0002-5364-1650`.

## Should Have

- A canonical country coverage ledger for all Michelin Star countries that can be supported by
  documented aggregate evidence.
- Source confidence values for coverage rows: `official`, `official-derived`, `secondary`,
  `withheld`, or `unverified`.
- A global choropleth route using license-compatible country boundaries and aggregate metrics.
- A New Zealand location-safe visualisation that defaults to region/city aggregate or
  centroid-level data unless exact point redistribution rights are documented.
- Scorecards for live visual quality out of 1000 and repository quality out of 100.
- CI and local scripts that separate repo-local failures from external publication gates.

## Could Have

- Additional aggregate-safe public indicators where source rights and redistribution terms are
  documented.
- More pivot dimensions and outcome views if they stay aggregate and license-compatible.
- A Zenodo DOI release after manual GitHub-Zenodo integration and record review.
- Additional Mojo migration beyond pure derived metrics after row-for-row parity is proven.

## Won't Have

- Public restaurant-level Michelin records.
- Public review ingestion or review-derived analysis.
- Public guide text, booking metadata, photos, addresses, or exact guide-derived coordinates.
- A guide-like searchable restaurant database.
- Removal of Python/Polars orchestration before source handling and asset generation have complete
  Mojo parity.

## Requirement Coverage

| Requirement Area | Track | Current Status |
| --- | --- | --- |
| Aggregate dashboard and public boundary | `bootstrap`, `data_loader`, `core_viz`, `linking_cms` archives | Delivered with current aggregate-only dashboard and source documentation |
| Strict CI and live deployment | `live_quality_score_20260703` | Partially delivered; CI and deployment are strict, scorecard command remains planned |
| Mojo metric backend | `mojo_migration_20260703` | Partially delivered; metric backend, tests, CI checks, and docs are in place |
| Full Michelin Star country coverage | `data_coverage_20260703` | Planned |
| Global choropleth and New Zealand location-safe view | `geo_outcomes_20260703` | Planned |
| Zenodo DOI | External publication gate | Planned/manual external gate |
