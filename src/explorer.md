# Country Explorer

Filter the aggregate country dataset by star tier, displayed countries, metric, and sort order.

```js
const countryMetrics = await FileAttachment("data/country_metrics.json").json();

const tierOptions = [
  "total_restaurants",
  "one_star_restaurants",
  "two_star_restaurants",
  "three_star_restaurants"
];

const metricOptions = [
  "total_restaurants",
  "total_stars",
  "one_star_restaurants",
  "two_star_restaurants",
  "three_star_restaurants",
  "stars_per_100k",
  "stars_per_10b_gdp",
  "gdp_per_capita",
  "population",
  "gdp"
];

const sortOptions = ["descending", "ascending"];
const scopeOptions = ["top", "all", "single"];

const metricLabels = {
  total_restaurants: "Aggregate restaurants",
  total_stars: "Total stars",
  one_star_restaurants: "1-star restaurants",
  two_star_restaurants: "2-star restaurants",
  three_star_restaurants: "3-star restaurants",
  stars_per_100k: "Stars per 100k residents",
  stars_per_10b_gdp: "Stars per $10B GDP",
  gdp_per_capita: "GDP per capita",
  population: "Population",
  gdp: "GDP current USD"
};

const allCountryNames = countryMetrics
  .map((d) => d.country_name)
  .sort((a, b) => a.localeCompare(b));

const tierField = view(
  Inputs.select(tierOptions, { label: "Star tier", value: "total_restaurants" })
);
const metric = view(
  Inputs.select(metricOptions, { label: "Chart metric", value: "total_restaurants" })
);
const sortDirection = view(Inputs.select(sortOptions, { label: "Sort", value: "descending" }));
const minTierRestaurants = view(
  Inputs.range([1, 100], {
    step: 1,
    label: "Minimum tier restaurants",
    value: tierField === "total_restaurants" ? 10 : 1
  })
);
const rowLimit = view(Inputs.range([10, 52], { step: 1, label: "Rows shown", value: 25 }));
const displayScope = view(Inputs.select(scopeOptions, { label: "Display", value: "top" }));
const focusCountry = view(Inputs.select(allCountryNames, { label: "Country", value: "France" }));
```

```js
const filteredRows = countryMetrics
  .filter((d) => displayScope !== "single" || d.country_name === focusCountry)
  .filter((d) => Number(d[tierField] ?? 0) >= minTierRestaurants)
  .toSorted((a, b) => {
    const left = Number(a[metric] ?? 0);
    const right = Number(b[metric] ?? 0);
    return sortDirection === "ascending" ? left - right : right - left;
  });

const visibleRows = displayScope === "all" ? filteredRows : filteredRows.slice(0, rowLimit);
const chartRows = visibleRows;
```

```js
display(
  html`<div class="summary-row">
    <div><strong>${filteredRows.length}</strong><span>matching countries</span></div>
    <div>
      <strong>${filteredRows.reduce((sum, d) => sum + Number(d.total_restaurants ?? 0), 0)}</strong
      ><span>aggregate restaurants</span>
    </div>
    <div>
      <strong>${filteredRows.reduce((sum, d) => sum + Number(d.total_stars ?? 0), 0)}</strong
      ><span>total stars</span>
    </div>
    <div>
      <strong>${filteredRows.reduce((sum, d) => sum + Number(d[tierField] ?? 0), 0)}</strong
      ><span>${metricLabels[tierField]}</span>
    </div>
  </div>`
);
```

```js
display(
  html`<div class="chart-frame">
    ${Plot.plot({
      theme: "dark",
      width: 1120,
      height: Math.max(440, chartRows.length * 32),
      marginLeft: 170,
      x: {
        grid: true,
        label: metricLabels[metric],
        type: metric === "population" || metric === "gdp" ? "log" : "linear"
      },
      y: { label: null },
      marks: [
        Plot.ruleX([0]),
        Plot.barX(chartRows, {
          x: metric,
          y: "country_name",
          fill: "#22d3ee",
          title: (d) =>
            `${d.country_name}\n${metricLabels[metric]}: ${Number(d[metric]).toLocaleString(undefined, { maximumFractionDigits: 4 })}\n1-star: ${d.one_star_restaurants}\n2-star: ${d.two_star_restaurants}\n3-star: ${d.three_star_restaurants}`
        }),
        Plot.text(chartRows, {
          x: metric,
          y: "country_name",
          text: (d) => Number(d[metric]).toLocaleString(undefined, { maximumFractionDigits: 2 }),
          dx: 6,
          fill: "#f8fafc",
          textAnchor: "start"
        })
      ]
    })}
  </div>`
);
```

## Filtered Countries

```js
display(
  Inputs.table(visibleRows, {
    columns: [
      "country_name",
      "country",
      "total_restaurants",
      "total_stars",
      "one_star_restaurants",
      "two_star_restaurants",
      "three_star_restaurants",
      "stars_per_100k",
      "stars_per_10b_gdp",
      "gdp_per_capita"
    ],
    format: {
      stars_per_100k: (d) => Number(d).toFixed(4),
      stars_per_10b_gdp: (d) => Number(d).toFixed(4),
      gdp_per_capita: (d) => `$${Number(d).toLocaleString(undefined, { maximumFractionDigits: 0 })}`
    }
  })
);
```
