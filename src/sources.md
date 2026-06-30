# Data Sources & Triangulation Ledger

This page documents the datasources, scraping rules, and validation ledger scores for this **open-source gastronomy data science** project.

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
