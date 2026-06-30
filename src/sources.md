# Data Sources & Triangulation Ledger

This page documents the datasources, scraping rules, and validation ledger scores for this **open-source gastronomy data science** project.

```js
// Load dynamic database version indicators
const dataVersion = await FileAttachment("data/version.json").json();
```

<div class="card" style="margin-bottom: 1.5rem;">
  <h3>📦 Dataset Versioning Details</h3>
  <p><strong>Database Version:</strong> <code>${dataVersion.version}</code></p>
  <p><strong>Last Compiled:</strong> <code>${dataVersion.compiled}</code></p>
</div>

```js
// Trigger the data loader compilation
const data = await FileAttachment("data/michelin.parquet").parquet();
const table = Inputs.table(data);
display(table);
```

