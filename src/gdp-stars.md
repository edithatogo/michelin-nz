# GDP & Stars Analysis

Compare compiled restaurant indicators against population and GDP. The controls below update both the chart and the table.

```js
const countryMetrics = await FileAttachment("data/country_metrics.json").json();

const measureOptions = new Map([
  ["stars_per_100k", "Stars per 100k residents"],
  ["stars_per_10b_gdp", "Stars per $10B GDP"],
  ["total_stars", "Total stars"],
  ["total_restaurants", "Restaurant records"],
  ["gdp_per_capita", "GDP per capita"]
]);

const xMeasure = view(Inputs.select(
  [["gdp_per_capita", "GDP per capita"], ["population", "Population"], ["gdp", "GDP current USD"]],
  {label: "X axis", value: "gdp_per_capita"}
));
const yMeasure = view(Inputs.select(Array.from(measureOptions), {
  label: "Y axis",
  value: "stars_per_100k"
}));
const minStars = view(Inputs.range([1, 12], {step: 1, label: "Minimum total stars", value: 1}));
const countries = view(Inputs.checkbox(countryMetrics.map((d) => d.country_name), {
  label: "Countries",
  value: countryMetrics.map((d) => d.country_name)
}));
```

```js
const selectedCountries = new Set(countries);
const queryResults = countryMetrics
  .filter((d) => selectedCountries.has(d.country_name))
  .filter((d) => d.total_stars >= minStars)
  .toSorted((a, b) => Number(b[yMeasure]) - Number(a[yMeasure]));
```

```js
display(html`<div class="summary-row">
  <div><strong>${queryResults.length}</strong><span>countries selected</span></div>
  <div><strong>${queryResults.reduce((sum, d) => sum + d.total_restaurants, 0)}</strong><span>restaurant records</span></div>
  <div><strong>${queryResults.reduce((sum, d) => sum + d.total_stars, 0)}</strong><span>total stars</span></div>
</div>`);
```

```js
display(Plot.plot({
  grid: true,
  theme: "dark",
  height: 460,
  x: {
    label: xMeasure,
    type: xMeasure === "population" || xMeasure === "gdp" || xMeasure === "gdp_per_capita" ? "log" : "linear"
  },
  y: {
    label: yMeasure,
    zero: true
  },
  color: {legend: true, label: "Country"},
  marks: [
    Plot.ruleY([0]),
    Plot.dot(queryResults, {
      x: xMeasure,
      y: yMeasure,
      fill: "country_name",
      r: (d) => Math.max(5, Math.sqrt(d.total_stars) * 4),
      title: (d) => `${d.country_name}\n${yMeasure}: ${Number(d[yMeasure]).toLocaleString(undefined, {maximumFractionDigits: 4})}\nStars: ${d.total_stars}\nRecords: ${d.total_restaurants}`
    }),
    Plot.text(queryResults, {
      x: xMeasure,
      y: yMeasure,
      text: "country",
      dy: -12,
      fontSize: 11,
      fill: "#f8fafc",
      stroke: "#020617",
      strokeWidth: 3
    })
  ]
}));
```

## Ranked Countries

```js
display(Inputs.table(queryResults, {
  columns: ["country_name", "country", "total_restaurants", "total_stars", "stars_per_100k", "stars_per_10b_gdp", "gdp_per_capita", "population", "gdp"],
  format: {
    stars_per_100k: (d) => Number(d).toFixed(4),
    stars_per_10b_gdp: (d) => Number(d).toFixed(4),
    gdp_per_capita: (d) => `$${Number(d).toLocaleString(undefined, {maximumFractionDigits: 0})}`,
    population: (d) => Number(d).toLocaleString(),
    gdp: (d) => `$${Number(d).toLocaleString(undefined, {maximumFractionDigits: 0})}`
  }
}));
```
