# New Zealand Aggregate

This page shows only aggregate New Zealand benchmark metrics. It intentionally does not publish individual restaurant names, reviews, coordinates, or row-level source records.

The comparison is a compact peer benchmark: New Zealand is highlighted against the current
aggregate country set so population-normalised and GDP-normalised intensity can be read without
exposing restricted guide-level detail.

```js
const countryMetrics = await FileAttachment("data/country_metrics.json").json();
const nz = countryMetrics.find((d) => d.country === "NZL");
const peers = countryMetrics
  .filter((d) => d.country !== "NZL")
  .toSorted((a, b) => b.stars_per_100k - a.stars_per_100k);
```

```js
display(
  html`<div class="kpi-grid">
    <div class="metric-card">
      <span>Aggregate Records</span><strong>${nz.total_restaurants}</strong
      ><small>count only</small>
    </div>
    <div class="metric-card">
      <span>Aggregate Stars</span><strong>${nz.total_stars}</strong><small>count only</small>
    </div>
    <div class="metric-card">
      <span>Stars per 100k</span><strong>${nz.stars_per_100k.toFixed(3)}</strong
      ><small>population-normalised</small>
    </div>
    <div class="metric-card">
      <span>Stars per $10B GDP</span><strong>${nz.stars_per_10b_gdp.toFixed(3)}</strong
      ><small>GDP-normalised</small>
    </div>
  </div>`
);
```

```js
display(
  Plot.plot({
    theme: "dark",
    height: 360,
    marginLeft: 120,
    x: { grid: true, label: "Stars per 100k residents" },
    y: { label: null },
    marks: [
      Plot.ruleX([0]),
      Plot.barX(
        [nz, ...peers].toSorted((a, b) => a.stars_per_100k - b.stars_per_100k),
        {
          x: "stars_per_100k",
          y: "country_name",
          fill: (d) => (d.country === "NZL" ? "#fbbf24" : "#38bdf8"),
          title: (d) => `${d.country_name}\nStars/100k: ${d.stars_per_100k.toFixed(4)}`
        }
      ),
      Plot.text([nz, ...peers], {
        x: "stars_per_100k",
        y: "country_name",
        text: (d) => d.stars_per_100k.toFixed(3),
        dx: 6,
        fill: "#e2e8f0"
      })
    ]
  })
);
```

## Interpretation Notes

- The New Zealand values are aggregate benchmark inputs, not official Michelin Guide New Zealand awards.
- The page does not redistribute individual Michelin-derived or review-derived records.
- A production version should attach source notes and permissions to each aggregate input before public release.
