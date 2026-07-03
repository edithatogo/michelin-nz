# Data Sources & Triangulation Ledger

This page documents the datasource ledger and compiled aggregate records for the dashboard.

The repository license covers dashboard code and project-authored documentation. World Bank indicators require World Bank attribution. Michelin Guide names, distinctions, ratings, text, branding, and related database rights are not open data. This public dashboard intentionally avoids redistributing individual Michelin-derived records, reviews, coordinates, or a row-level guide-like database.

The aggregate country ledger is a repo-local 2026 snapshot derived from a secondary country-ranking table that cites the Michelin restaurant search. It is used as a coverage baseline until each country can be reconciled directly against official Michelin guide pages. New Zealand remains a local benchmark row and is not represented as an official Michelin Guide country.

```js
// Load dynamic database version indicators
const dataVersion = await FileAttachment("data/version.json").json();
```

```js
display(
  html`<div class="card" style="margin-bottom: 1.5rem;">
    <h3>📦 Dataset Versioning Details</h3>
    <p><strong>Database Version:</strong> <code>${dataVersion.version}</code></p>
    <p><strong>Last Compiled:</strong> <code>${dataVersion.compiled}</code></p>
    <p><strong>Public artifact boundary:</strong> aggregate country metrics only.</p>
  </div>`
);
```

```js
// Trigger the data loader compilation
const data = await FileAttachment("data/country_metrics.json").json();
display(Inputs.table(data));
```

## Aggregate Country Metrics

No individual restaurant rows or review records are published from this page.
