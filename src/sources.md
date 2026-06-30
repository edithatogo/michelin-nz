# Data Sources & Triangulation Ledger

This page documents the datasources, scraping rules, and verification ledger scores.

```js
// Trigger the data loader compilation
const data = await FileAttachment("data/michelin.parquet").parquet();
const table = Inputs.table(data);
display(table);
```

