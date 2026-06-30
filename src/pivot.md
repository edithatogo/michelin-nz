# Pivot Table

Choose the country set, row grouping, and measure to inspect the compiled dashboard data.

```js
const countryMetrics = await FileAttachment("data/country_metrics.json").json();
const restaurants = await FileAttachment("data/restaurants.json").json();

const countryOptions = ["All", ...countryMetrics.map((d) => d.country_name).sort((a, b) => a.localeCompare(b))];
const selectedCountries = view(Inputs.checkbox(countryOptions, {
  label: "Countries",
  value: countryOptions
}));

const rowDimension = view(Inputs.select(
  [
    ["country_name", "Country"],
    ["country", "Country code"],
    ["source", "Source type"]
  ],
  {label: "Rows", value: "country_name"}
));

const measure = view(Inputs.select(
  [
    ["total_stars", "Total stars"],
    ["total_restaurants", "Total restaurants"],
    ["stars_per_100k", "Stars per 100k residents"],
    ["stars_per_10b_gdp", "Stars per $10B GDP"],
    ["gdp_per_capita", "GDP per capita"],
    ["population", "Population"],
    ["gdp_current_usd", "GDP current USD"]
  ],
  {label: "Measure", value: "stars_per_100k"}
));

const aggregation = view(Inputs.select(
  [
    ["sum", "Sum"],
    ["mean", "Average"],
    ["max", "Maximum"]
  ],
  {label: "Aggregation", value: "sum"}
));
```

```js
const selectedCountrySet = new Set(selectedCountries.includes("All")
  ? countryOptions.filter((d) => d !== "All")
  : selectedCountries);

const metricRows = countryMetrics
  .filter((d) => selectedCountrySet.has(d.country_name))
  .map((d) => ({...d, source: "Country metrics"}));

const restaurantCounts = restaurants
  .filter((d) => metricRows.some((m) => m.country === d.country))
  .map((d) => ({
    country: d.country,
    country_name: countryMetrics.find((m) => m.country === d.country)?.country_name ?? d.country,
    source: "Restaurant records",
    total_stars: d.stars,
    total_restaurants: 1,
    stars_per_100k: null,
    stars_per_10b_gdp: null,
    gdp_per_capita: null,
    population: null,
    gdp_current_usd: null
  }));

const sourceRows = rowDimension === "source"
  ? [...metricRows, ...restaurantCounts]
  : metricRows;

function aggregate(values, mode) {
  const numericValues = values.filter((value) => Number.isFinite(value));
  if (!numericValues.length) return null;
  if (mode === "mean") return numericValues.reduce((sum, value) => sum + value, 0) / numericValues.length;
  if (mode === "max") return Math.max(...numericValues);
  return numericValues.reduce((sum, value) => sum + value, 0);
}

const groupedRows = Array.from(
  Map.groupBy(sourceRows, (d) => d[rowDimension]),
  ([group, rows]) => ({
    [rowDimension]: group,
    records: rows.length,
    total_stars: aggregate(rows.map((d) => Number(d.total_stars)), "sum"),
    total_restaurants: aggregate(rows.map((d) => Number(d.total_restaurants)), "sum"),
    stars_per_100k: aggregate(rows.map((d) => Number(d.stars_per_100k)), aggregation),
    stars_per_10b_gdp: aggregate(rows.map((d) => Number(d.stars_per_10b_gdp)), aggregation),
    gdp_per_capita: aggregate(rows.map((d) => Number(d.gdp_per_capita)), aggregation),
    population: aggregate(rows.map((d) => Number(d.population)), aggregation),
    gdp_current_usd: aggregate(rows.map((d) => Number(d.gdp_current_usd)), aggregation),
    selected_measure: aggregate(rows.map((d) => Number(d[measure])), aggregation)
  })
).sort((a, b) => (b.selected_measure ?? -Infinity) - (a.selected_measure ?? -Infinity));
```

```js
display(Plot.plot({
  theme: "dark",
  marginLeft: 160,
  height: Math.max(260, groupedRows.length * 42),
  x: {grid: true, label: measure},
  y: {label: rowDimension},
  marks: [
    Plot.ruleX([0]),
    Plot.barX(groupedRows, {
      x: "selected_measure",
      y: rowDimension,
      fill: "#64b5f6",
      title: (d) => `${d[rowDimension]}\n${measure}: ${Number(d.selected_measure ?? 0).toLocaleString(undefined, {maximumFractionDigits: 3})}`
    }),
    Plot.text(groupedRows, {
      x: "selected_measure",
      y: rowDimension,
      text: (d) => Number(d.selected_measure ?? 0).toLocaleString(undefined, {maximumFractionDigits: 2}),
      dx: 6,
      fill: "#f8fafc",
      textAnchor: "start"
    })
  ]
}));
```

## Pivot Results

```js
display(Inputs.table(groupedRows, {
  columns: [
    rowDimension,
    "records",
    "selected_measure",
    "total_stars",
    "total_restaurants",
    "stars_per_100k",
    "stars_per_10b_gdp",
    "gdp_per_capita",
    "population",
    "gdp_current_usd"
  ]
}));
```

## Filtered Country Records

```js
display(Inputs.table(metricRows));
```
