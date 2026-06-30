# Restaurant Location Map

The map shows only the restaurant records included in the compiled dataset.

```js
const restaurants = await FileAttachment("data/restaurants.json").json();
const countries = ["All", ...new Set(restaurants.map((d) => d.country).sort())];
const selectedCountry = view(Inputs.select(countries, {label: "Country", value: "All"}));
const minStars = view(Inputs.range([1, 3], {step: 1, label: "Minimum stars", value: 1}));

const mappedRestaurants = restaurants
  .filter((d) => selectedCountry === "All" || d.country === selectedCountry)
  .filter((d) => d.stars >= minStars)
  .filter((d) => Number.isFinite(d.lat) && Number.isFinite(d.lng));
```

```js
display(html`<div class="summary-row">
  <div><strong>${mappedRestaurants.length}</strong><span>restaurants shown</span></div>
  <div><strong>${mappedRestaurants.reduce((sum, d) => sum + d.stars, 0)}</strong><span>stars shown</span></div>
  <div><strong>${new Set(mappedRestaurants.map((d) => d.country)).size}</strong><span>countries shown</span></div>
</div>`);
```

```js
display(Plot.plot({
  width: 920,
  height: 520,
  projection: "equal-earth",
  style: {background: "#020617", color: "#f8fafc"},
  color: {legend: true, label: "Country"},
  r: {range: [5, 16], label: "Stars"},
  marks: [
    Plot.sphere({fill: "#020617", stroke: "#334155"}),
    Plot.graticule({stroke: "#1e293b", strokeOpacity: 0.7}),
    Plot.dot(mappedRestaurants, {
      x: "lng",
      y: "lat",
      r: "stars",
      fill: "country",
      stroke: "#f8fafc",
      strokeWidth: 1.2,
      title: (d) => `${d.name}\n${d.location}, ${d.country}\nStars: ${d.stars}\n${d.type}`
    }),
    Plot.text(mappedRestaurants, {
      x: "lng",
      y: "lat",
      text: "country",
      dy: -14,
      fontSize: 11,
      fill: "#f8fafc",
      stroke: "#020617",
      strokeWidth: 4
    })
  ]
}));
```

## Visible Records

Use this page to check whether the compiled restaurant-level geography is plausible before interpreting per-capita or GDP-normalised country metrics. The current sample is intentionally small; missing countries or cities mean they are absent from this repository's compiled sample, not absent from the Michelin Guide.

```js
display(Inputs.table(mappedRestaurants, {
  columns: ["name", "location", "country", "stars", "type", "lat", "lng"]
}));
```

## Coverage Notes

- Coordinates are used for visualization and directions only.
- Country totals elsewhere in the dashboard are calculated from these restaurant records.
- The map does not include Michelin Guide text, reviews, descriptions, images, or proprietary guide metadata.
