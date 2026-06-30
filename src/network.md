# Cuisine And Country Network

This network is derived from the compiled restaurant records. It connects each country to its restaurants and each restaurant to its cuisine/type label.

```js
const restaurants = await FileAttachment("data/restaurants.json").json();

const countryNodes = Array.from(new Set(restaurants.map((d) => d.country))).map((country, index) => ({
  id: country,
  label: country,
  kind: "country",
  x: 0,
  y: index
}));

const restaurantNodes = restaurants.map((restaurant, index) => ({
  id: restaurant.id,
  label: restaurant.name,
  kind: "restaurant",
  country: restaurant.country,
  stars: restaurant.stars,
  x: 1.4,
  y: index * 0.45
}));

const cuisineNodes = Array.from(new Set(restaurants.map((d) => d.type))).map((type, index) => ({
  id: `type-${index}`,
  label: type,
  kind: "cuisine",
  x: 3,
  y: index * 0.8
}));

const cuisineByLabel = new Map(cuisineNodes.map((node) => [node.label, node]));
const nodes = [...countryNodes, ...restaurantNodes, ...cuisineNodes];
const nodeById = new Map(nodes.map((node) => [node.id, node]));

const links = [
  ...restaurants.map((restaurant) => ({source: restaurant.country, target: restaurant.id, relation: "country"})),
  ...restaurants.map((restaurant) => ({source: restaurant.id, target: cuisineByLabel.get(restaurant.type).id, relation: "cuisine"}))
];

const linkRows = links.map((link) => ({
  ...link,
  x1: nodeById.get(link.source).x,
  y1: nodeById.get(link.source).y,
  x2: nodeById.get(link.target).x,
  y2: nodeById.get(link.target).y
}));
```

```js
display(Plot.plot({
  width: 940,
  height: 620,
  marginLeft: 60,
  marginRight: 260,
  x: {axis: null, domain: [-0.2, 3.6]},
  y: {axis: null},
  color: {
    legend: true,
    domain: ["country", "restaurant", "cuisine"],
    range: ["#38bdf8", "#fbbf24", "#fb7185"]
  },
  style: {background: "#020617", color: "#f8fafc"},
  marks: [
    Plot.link(linkRows, {
      x1: "x1",
      y1: "y1",
      x2: "x2",
      y2: "y2",
      stroke: "#475569",
      strokeOpacity: 0.8
    }),
    Plot.dot(nodes, {
      x: "x",
      y: "y",
      fill: "kind",
      r: (d) => d.kind === "restaurant" ? Math.max(5, d.stars * 3) : 8,
      stroke: "#f8fafc"
    }),
    Plot.text(nodes, {
      x: "x",
      y: "y",
      text: "label",
      dx: 12,
      fill: "#f8fafc",
      fontSize: 11,
      textAnchor: "start"
    })
  ]
}));
```

## Nodes

```js
display(Inputs.table(nodes));
```
