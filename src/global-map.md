# Global Star Density Map

Generated map of Michelin-starred restaurant hubs from the build pipeline.

```js
const restaurants = await FileAttachment("data/restaurants.json").json();
const mappedRestaurants = restaurants.filter((d) => Number.isFinite(d.lat) && Number.isFinite(d.lng));
```

## Restaurant Locations

Each point is sized by star count and labelled by country. This SVG map is generated at build/runtime from `data/restaurants.json`, so it is covered by the deployment smoke tests.

```js
const mapChart = Plot.plot({
  width: 900,
  height: 520,
  projection: "equal-earth",
  style: {
    background: "#020617",
    color: "#f8fafc"
  },
  color: {
    legend: true,
    label: "Country"
  },
  r: {
    range: [4, 14],
    label: "Stars"
  },
  marks: [
    Plot.sphere({fill: "#020617", stroke: "#334155"}),
    Plot.graticule({stroke: "#1e293b", strokeOpacity: 0.7}),
    Plot.dot(mappedRestaurants, {
      x: "lng",
      y: "lat",
      r: "stars",
      fill: "country",
      stroke: "#f8fafc",
      strokeWidth: 1,
      title: (d) => `${d.name}\n${d.location}, ${d.country}\nStars: ${d.stars}`
    }),
    Plot.text(mappedRestaurants, {
      x: "lng",
      y: "lat",
      text: "country",
      dy: -12,
      fontSize: 10,
      fill: "#f8fafc",
      stroke: "#020617",
      strokeWidth: 3
    })
  ]
});

display(mapChart);
```

## Source Records

```js
display(Inputs.table(mappedRestaurants));
```
