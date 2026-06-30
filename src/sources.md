# Data Sources & Triangulation Ledger

This page documents the datasource ledger and compiled records for the dashboard.

The repository license covers dashboard code and project-authored documentation. World Bank indicators require World Bank attribution. Michelin Guide names, distinctions, ratings, text, branding, and related database rights are not open data; Michelin-derived fields here should be treated as limited reference facts rather than a redistributable Michelin database.

```js
// Load dynamic database version indicators
const dataVersion = await FileAttachment("data/version.json").json();
const parquetUrl = await FileAttachment("data/michelin.parquet").url();
```

```js
display(html`<div class="card" style="margin-bottom: 1.5rem;">
  <h3>📦 Dataset Versioning Details</h3>
  <p><strong>Database Version:</strong> <code>${dataVersion.version}</code></p>
  <p><strong>Last Compiled:</strong> <code>${dataVersion.compiled}</code></p>
  <p><strong>Country Metrics Parquet:</strong> <a href="${parquetUrl}" download>Download compiled Parquet artifact</a></p>
</div>`);
```

```js
// Trigger the data loader compilation
const data = await FileAttachment("data/country_metrics.json").json();
const restaurants = await FileAttachment("data/restaurants.json").json();
display(Inputs.table(data));
```

## Restaurant-Level Records

```js
display(Inputs.table(restaurants));
```
