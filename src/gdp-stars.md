# GDP & Stars Analysis

We analyze the correlation between national economic metrics (GDP and GDP per capita) and culinary stars density.

```js
// Load the parquet file attachment
const michelinFile = FileAttachment("data/michelin.parquet");

// Establish unified reactive sliders
const minStars = view(Inputs.range([0, 10], {step: 1, label: "Min Total Stars", value: 1}));
const minPop = view(Inputs.range([1000000, 400000000], {step: 1000000, label: "Min Population", value: 1000000, format: d => (d / 1000000).toFixed(0) + "M"}));
```

We execute a client-side SQL query against our Parquet file using DuckDB:

```js
// Query DuckDB using client-side SQL block
const queryResults = await michelinFile.query(
  `SELECT country, country_name, population, gdp, total_stars, stars_per_100k, gdp_per_capita, stars_per_10b_gdp
   FROM "data/michelin.parquet"
   WHERE total_stars >= ${minStars} AND population >= ${minPop}
   ORDER BY stars_per_100k DESC`
);
```

### Visualizing Culinary Intensity vs. Wealth

Below, we plot the relationship between **GDP per Capita (USD)** and **Michelin Stars per 100,000 residents**. Each point represents a country matching our filters.

```js
const chart = Plot.plot({
  grid: true,
  theme: "dark",
  x: {
    label: "GDP per Capita (USD) →",
    type: "log",
    tickFormat: "$,.0f"
  },
  y: {
    label: "↑ Michelin Stars per 100k residents",
    zero: true
  },
  color: {
    scheme: "spectral"
  },
  marks: [
    Plot.ruleY([0]),
    Plot.dot(queryResults, {
      x: "gdp_per_capita",
      y: "stars_per_100k",
      fill: "stars_per_100k",
      r: 8,
      title: d => `${d.country_name}\nStars: ${d.total_stars}\nStars/100k: ${d.stars_per_100k.toFixed(3)}\nGDP/capita: $${d.gdp_per_capita.toLocaleString(undefined, {maximumFractionDigits: 0})}`
    }),
    Plot.text(queryResults, {
      x: "gdp_per_capita",
      y: "stars_per_100k",
      text: "country",
      dy: -12,
      fontSize: 10,
      fill: "#f8fafc"
    })
  ]
});

display(chart);
```

### Filtered Data Table

```js
display(Inputs.table(queryResults));
```
