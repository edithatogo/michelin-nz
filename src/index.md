# Michelin Star Per-Capita Dashboard

This dashboard compares aggregate gastronomy indicators against country population and GDP. It is useful for testing methodology and interactive analysis, but it is not a complete Michelin Guide database.

```js
const countryMetrics = await FileAttachment("data/country_metrics.json").json();

const totalCountries = countryMetrics.length;
const totalRestaurants = countryMetrics.reduce(
  (sum, d) => sum + Number(d.total_restaurants ?? 0),
  0
);
const totalStars = countryMetrics.reduce((sum, d) => sum + Number(d.total_stars ?? 0), 0);
const nzAggregate = countryMetrics.find((d) => d.country === "NZL");
const topDensity = countryMetrics.toSorted((a, b) => b.stars_per_100k - a.stars_per_100k)[0];
const topGdpEfficiency = countryMetrics.toSorted(
  (a, b) => b.stars_per_10b_gdp - a.stars_per_10b_gdp
)[0];
const overviewRows = countryMetrics
  .toSorted((a, b) => b.stars_per_100k - a.stars_per_100k)
  .slice(0, 20)
  .toSorted((a, b) => a.stars_per_100k - b.stars_per_100k);
```

```js
display(
  html`<div class="kpi-grid">
    <div class="metric-card">
      <span>Countries</span><strong>${totalCountries}</strong
      ><small>represented in the compiled sample</small>
    </div>
    <div class="metric-card">
      <span>Aggregate Records</span><strong>${totalRestaurants}</strong
      ><small>counted records only</small>
    </div>
    <div class="metric-card">
      <span>Total Stars</span><strong>${totalStars}</strong
      ><small>sum of compiled indicators</small>
    </div>
    <div class="metric-card">
      <span>NZ Aggregate Stars</span><strong>${nzAggregate.total_stars}</strong
      ><small>no row-level records published</small>
    </div>
  </div>`
);
```

```js
display(
  html`<div class="notice">
    <strong>Aggregation boundary:</strong> this public dashboard redistributes only country-level
    aggregate metrics and derived analysis. It does not publish individual restaurant records,
    review content, coordinates, or row-level Michelin-derived data.
  </div>`
);
```

## Overview

```js
display(
  html`<div class="chart-frame">
    ${Plot.plot({
      theme: "dark",
      height: 620,
      marginLeft: 150,
      width: 1100,
      x: { grid: true, label: "Stars per 100k residents" },
      y: { label: null },
      marks: [
        Plot.ruleX([0]),
        Plot.barX(overviewRows, {
          x: "stars_per_100k",
          y: "country_name",
          fill: "#38bdf8",
          title: (d) =>
            `${d.country_name}\nStars: ${d.total_stars}\nRestaurants: ${d.total_restaurants}\nStars/100k: ${d.stars_per_100k.toFixed(3)}`
        }),
        Plot.text(overviewRows, {
          x: "stars_per_100k",
          y: "country_name",
          text: (d) => d.stars_per_100k.toFixed(3),
          dx: 6,
          fill: "#e2e8f0"
        })
      ]
    })}
  </div>`
);
```

<div class="dashboard-grid">
  <a class="nav-card" href="./pivot"><strong>Pivot Table</strong><span>Filter countries, choose measures, and change aggregations.</span></a>
  <a class="nav-card" href="./gdp-stars"><strong>GDP Analysis</strong><span>Compare density against GDP per capita and economic scale.</span></a>
  <a class="nav-card" href="./nz"><strong>NZ Aggregate</strong><span>Review New Zealand's aggregate benchmark metrics.</span></a>
  <a class="nav-card" href="./sources"><strong>Sources</strong><span>Review licensing, provenance, and aggregate metric tables.</span></a>
</div>

## Current Leaders In This Sample

```js
display(
  Inputs.table(
    [
      {
        metric: "Highest stars per 100k residents",
        country: topDensity.country_name,
        value: topDensity.stars_per_100k
      },
      {
        metric: "Highest stars per $10B GDP",
        country: topGdpEfficiency.country_name,
        value: topGdpEfficiency.stars_per_10b_gdp
      }
    ],
    {
      format: {
        value: (d) => Number(d).toLocaleString(undefined, { maximumFractionDigits: 4 })
      }
    }
  )
);
```

## Methodology And Licensing Boundaries

- Michelin Guide names, distinctions, ratings, text, branding, and related database rights are not open data. This public site avoids redistributing individual Michelin-derived records.
- World Bank population and GDP indicators are reused with attribution from World Bank Open Data.
- New Zealand values are benchmark indicators from the local compiled sample; they are not official Michelin Guide New Zealand awards.
- Per-capita metrics are sensitive to guide coverage. Countries where Michelin covers only selected cities are not comparable to countries with broader guide coverage.
