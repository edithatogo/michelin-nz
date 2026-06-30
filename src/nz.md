# New Zealand Records

New Zealand currently has local benchmark entries in the compiled sample. These are not official Michelin Guide New Zealand awards.

```js
const reviews = await FileAttachment("data/community_reviews.json").json();
const allRestaurants = await FileAttachment("data/restaurants.json").json();
const restaurants = allRestaurants
  .filter((d) => d.country === "NZL")
  .toSorted((a, b) => b.stars - a.stars || a.name.localeCompare(b.name));

const minStars = view(Inputs.range([1, 3], {step: 1, label: "Minimum stars", value: 1}));
const locations = ["All", ...new Set(restaurants.map((d) => d.location).sort())];
const location = view(Inputs.select(locations, {label: "Location", value: "All"}));
const visibleRestaurants = restaurants
  .filter((d) => d.stars >= minStars)
  .filter((d) => location === "All" || d.location === location);
```

```js
display(html`<div class="summary-row">
  <div><strong>${visibleRestaurants.length}</strong><span>visible records</span></div>
  <div><strong>${visibleRestaurants.reduce((sum, d) => sum + d.stars, 0)}</strong><span>visible stars</span></div>
  <div><strong>${new Set(visibleRestaurants.map((d) => d.location)).size}</strong><span>locations</span></div>
</div>`);
```

```js
display(Plot.plot({
  height: 320,
  marginLeft: 110,
  theme: "dark",
  x: {grid: true, label: "Stars"},
  y: {label: null},
  marks: [
    Plot.ruleX([0]),
    Plot.barX(visibleRestaurants.toSorted((a, b) => a.stars - b.stars), {
      x: "stars",
      y: "name",
      fill: "location",
      title: (d) => `${d.name}\n${d.location}\n${d.type}`
    }),
    Plot.text(visibleRestaurants, {
      x: "stars",
      y: "name",
      text: (d) => "star".repeat(0) || d.stars,
      dx: 8,
      fill: "#e2e8f0"
    })
  ]
}));
```

## Records And Links

The table exposes the compiled local fields used elsewhere in the dashboard. Map links are generated from latitude and longitude only; review links are counted from community JSON submissions in this repository.

```js
display(Inputs.table(visibleRestaurants.map((r) => ({
  name: r.name,
  location: r.location,
  stars: r.stars,
  type: r.type,
  google_maps: `https://www.google.com/maps/search/?api=1&query=${r.lat},${r.lng}`,
  openstreetmap: `https://www.openstreetmap.org/?mlat=${r.lat}&mlon=${r.lng}#map=17/${r.lat}/${r.lng}`,
  community_reviews: reviews.filter((review) => review.restaurantId === r.id).length
}))));
```

```js
display(html`<div class="dashboard-grid">
  ${visibleRestaurants.map((r) => html`<div class="card compact-card">
    <div class="card-heading">
      <h3>${r.name}</h3>
      <span class="star-rating">${"★".repeat(r.stars)}</span>
    </div>
    <p>${r.type}</p>
    <p><strong>${r.location}</strong></p>
    <p class="link-row">
      <a target="_blank" href="https://www.google.com/maps/search/?api=1&query=${r.lat},${r.lng}">Google Maps</a>
      <a target="_blank" href="https://www.openstreetmap.org/?mlat=${r.lat}&mlon=${r.lng}#map=17/${r.lat}/${r.lng}">OpenStreetMap</a>
    </p>
  </div>`)}
</div>`);
```

## Interpretation Notes

- These entries are local benchmark records, not a claim that Michelin currently awards stars in New Zealand.
- The star-like score is a dashboard normalization input used for cross-country calculations.
- If this project is used publicly, the local source and permission basis for each New Zealand record should be documented before treating the data as production-grade.
