# GDP & Stars Analysis

Compare compiled aggregate gastronomy indicators against population and GDP. The controls below update both the chart and the table.

```js
const countryMetrics = await FileAttachment("data/country_metrics.json").json();

const measureOptions = [
  "stars_per_100k",
  "stars_per_10b_gdp",
  "total_stars",
  "total_restaurants",
  "gdp_per_capita"
];

const xMeasureOptions = ["gdp_per_capita", "population", "gdp"];

const measureLabels = {
  stars_per_100k: "Stars per 100k residents",
  stars_per_10b_gdp: "Stars per $10B GDP",
  total_stars: "Total stars",
  total_restaurants: "Aggregate records",
  gdp_per_capita: "GDP per capita",
  population: "Population",
  gdp: "GDP current USD"
};

const starCountries = countryMetrics.filter((d) => d.total_stars > 0).map((d) => d.country_name);
const defaultCountrySet = new Set(
  countryMetrics
    .toSorted((a, b) => b.total_stars - a.total_stars)
    .slice(0, 25)
    .map((d) => d.country_name)
);
defaultCountrySet.add("New Zealand");
const defaultCountries = [...defaultCountrySet];

const xMeasure = view(Inputs.select(xMeasureOptions, { label: "X axis", value: "gdp_per_capita" }));
const yMeasure = view(
  Inputs.select(measureOptions, {
    label: "Y axis",
    value: "stars_per_100k"
  })
);
const minStars = view(Inputs.range([1, 100], { step: 1, label: "Minimum total stars", value: 10 }));
const countries = view(
  Inputs.checkbox(starCountries, {
    label: "Countries",
    value: defaultCountries
  })
);
```

```js
const selectedCountries = new Set(countries);
const queryResults = countryMetrics
  .filter((d) => selectedCountries.has(d.country_name))
  .filter((d) => d.total_stars >= minStars)
  .toSorted((a, b) => Number(b[yMeasure]) - Number(a[yMeasure]));
const nzRows = queryResults.filter((d) => d.country === "NZL");
const usesPositiveRateScale = ["stars_per_100k", "stars_per_10b_gdp", "gdp_per_capita"].includes(
  yMeasure
);
```

```js
display(
  html`<div class="summary-row">
    <div><strong>${queryResults.length}</strong><span>countries selected</span></div>
    <div>
      <strong>${queryResults.reduce((sum, d) => sum + d.total_restaurants, 0)}</strong
      ><span>aggregate records</span>
    </div>
    <div>
      <strong>${queryResults.reduce((sum, d) => sum + d.total_stars, 0)}</strong
      ><span>total stars</span>
    </div>
  </div>`
);
```

```js
display(
  html`<div class="chart-frame">
    ${Plot.plot({
      grid: true,
      theme: "dark",
      height: 620,
      width: 1100,
      x: {
        label: measureLabels[xMeasure],
        type:
          xMeasure === "population" || xMeasure === "gdp" || xMeasure === "gdp_per_capita"
            ? "log"
            : "linear"
      },
      y: {
        label: measureLabels[yMeasure],
        grid: true,
        type: usesPositiveRateScale ? "log" : "linear",
        zero: !usesPositiveRateScale
      },
      color: { legend: true, label: "Country" },
      marks: [
        ...(usesPositiveRateScale ? [] : [Plot.ruleY([0])]),
        Plot.dot(queryResults, {
          x: xMeasure,
          y: yMeasure,
          fill: "country_name",
          fillOpacity: (d) => (d.country === "NZL" ? 1 : 0.72),
          stroke: (d) => (d.country === "NZL" ? "#fbbf24" : "#020617"),
          strokeWidth: (d) => (d.country === "NZL" ? 2.5 : 0.8),
          r: (d) => Math.max(5, Math.sqrt(d.total_stars) * 4),
          title: (d) =>
            `${d.country_name}\n${yMeasure}: ${Number(d[yMeasure]).toLocaleString(undefined, { maximumFractionDigits: 4 })}\nStars: ${d.total_stars}\nRecords: ${d.total_restaurants}`
        }),
        Plot.dot(nzRows, {
          x: xMeasure,
          y: yMeasure,
          r: 9,
          fill: "#fbbf24",
          stroke: "#020617",
          strokeWidth: 2
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
        }),
        Plot.text(nzRows, {
          x: xMeasure,
          y: yMeasure,
          text: "country",
          dy: -18,
          fontSize: 13,
          fontWeight: "bold",
          fill: "#fbbf24",
          stroke: "#020617",
          strokeWidth: 4
        })
      ]
    })}
  </div>`
);
```

## Ranked Countries

```js
display(
  Inputs.table(queryResults, {
    columns: [
      "country_name",
      "country",
      "total_restaurants",
      "total_stars",
      "stars_per_100k",
      "stars_per_10b_gdp",
      "gdp_per_capita",
      "population",
      "gdp"
    ],
    format: {
      stars_per_100k: (d) => Number(d).toFixed(4),
      stars_per_10b_gdp: (d) => Number(d).toFixed(4),
      gdp_per_capita: (d) =>
        `$${Number(d).toLocaleString(undefined, { maximumFractionDigits: 0 })}`,
      population: (d) => Number(d).toLocaleString(),
      gdp: (d) => `$${Number(d).toLocaleString(undefined, { maximumFractionDigits: 0 })}`
    }
  })
);
```
