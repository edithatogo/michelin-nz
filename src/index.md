# Michelin Star Per-Capita Dashboard

This dashboard compares a small, explicitly curated set of restaurant indicators against country population and GDP. It is useful for testing methodology and interactive analysis, but it is not a complete Michelin Guide database.

```js
const countryMetrics = await FileAttachment("data/country_metrics.json").json();
const restaurants = await FileAttachment("data/restaurants.json").json();

const totalCountries = countryMetrics.length;
const totalRestaurants = restaurants.length;
const totalStars = restaurants.reduce((sum, d) => sum + Number(d.stars ?? 0), 0);
const nzRestaurants = restaurants.filter((d) => d.country === "NZL").length;
const topDensity = countryMetrics.toSorted((a, b) => b.stars_per_100k - a.stars_per_100k)[0];
const topGdpEfficiency = countryMetrics.toSorted((a, b) => b.stars_per_10b_gdp - a.stars_per_10b_gdp)[0];
```

```js
display(html`<div class="kpi-grid">
  <div class="metric-card"><span>Countries</span><strong>${totalCountries}</strong><small>represented in the compiled sample</small></div>
  <div class="metric-card"><span>Restaurants</span><strong>${totalRestaurants}</strong><small>restaurant-level records</small></div>
  <div class="metric-card"><span>Total Stars</span><strong>${totalStars}</strong><small>sum of compiled indicators</small></div>
  <div class="metric-card"><span>NZ Records</span><strong>${nzRestaurants}</strong><small>local benchmark entries</small></div>
</div>`);
```

```js
display(html`<div class="notice">
  <strong>Coverage warning:</strong> the current dataset is a curated demonstration sample. Per-capita rankings can be inspected, but they should not be read as official country rankings or a complete Michelin market comparison.
</div>`);
```

## Overview

```js
display(Plot.plot({
  theme: "dark",
  height: 320,
  marginLeft: 120,
  x: {grid: true, label: "Stars per 100k residents"},
  y: {label: null},
  marks: [
    Plot.ruleX([0]),
    Plot.barX(countryMetrics.toSorted((a, b) => a.stars_per_100k - b.stars_per_100k), {
      x: "stars_per_100k",
      y: "country_name",
      fill: "#38bdf8",
      title: (d) => `${d.country_name}\nStars: ${d.total_stars}\nRestaurants: ${d.total_restaurants}\nStars/100k: ${d.stars_per_100k.toFixed(3)}`
    }),
    Plot.text(countryMetrics, {
      x: "stars_per_100k",
      y: "country_name",
      text: (d) => d.stars_per_100k.toFixed(3),
      dx: 6,
      fill: "#e2e8f0"
    })
  ]
}));
```

<div class="dashboard-grid">
  <a class="nav-card" href="./pivot"><strong>Pivot Table</strong><span>Filter countries, choose measures, and change aggregations.</span></a>
  <a class="nav-card" href="./gdp-stars"><strong>GDP Analysis</strong><span>Compare density against GDP per capita and economic scale.</span></a>
  <a class="nav-card" href="./global-map"><strong>Map</strong><span>Inspect the restaurant locations included in the compiled sample.</span></a>
  <a class="nav-card" href="./nz"><strong>NZ Records</strong><span>Review the local entries, locations, and source caveats.</span></a>
</div>

## Current Leaders In This Sample

```js
display(Inputs.table([
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
], {
  format: {
    value: (d) => Number(d).toLocaleString(undefined, {maximumFractionDigits: 4})
  }
}));
```

## Methodology And Licensing Boundaries

- Michelin Guide names, distinctions, ratings, text, branding, and related database rights are not open data. This project must not redistribute a comprehensive scraped Michelin database without permission.
- World Bank population and GDP indicators are reused with attribution from World Bank Open Data.
- New Zealand values are benchmark indicators from the local compiled sample; they are not official Michelin Guide New Zealand awards.
- Per-capita metrics are sensitive to guide coverage. Countries where Michelin covers only selected cities are not comparable to countries with broader guide coverage.
