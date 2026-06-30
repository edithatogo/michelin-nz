# Chef & Cuisine Influence Network

Static SVG network of chef, restaurant, cuisine, and geography relationships. The page no longer depends on an external WebGL bundle, so deployment checks can verify that the image renders reliably.

```js
const nodes = [
  {id: "Monique Fiso", type: "chef", hub: "NZL", x: 0, y: 0},
  {id: "Hiakai", type: "restaurant", hub: "NZL", x: 1, y: 0.25},
  {id: "Modern Maori", type: "cuisine", hub: "NZL", x: 2, y: 0},
  {id: "The Grove", type: "restaurant", hub: "NZL", x: 1, y: -0.65},
  {id: "French technique", type: "cuisine", hub: "FRA", x: 2.4, y: -0.95},
  {id: "Bernard Pacaud", type: "chef", hub: "FRA", x: 0, y: 1.35},
  {id: "L'Ambroisie", type: "restaurant", hub: "FRA", x: 1.1, y: 1.35},
  {id: "French haute cuisine", type: "cuisine", hub: "FRA", x: 2.25, y: 1.35},
  {id: "Jiro Ono", type: "chef", hub: "JPN", x: 0, y: 2.65},
  {id: "Sukiyabashi Jiro", type: "restaurant", hub: "JPN", x: 1.2, y: 2.65},
  {id: "Sushi", type: "cuisine", hub: "JPN", x: 2.25, y: 2.65}
];

const links = [
  {source: "Monique Fiso", target: "Hiakai"},
  {source: "Hiakai", target: "Modern Maori"},
  {source: "The Grove", target: "French technique"},
  {source: "Monique Fiso", target: "French technique"},
  {source: "Bernard Pacaud", target: "L'Ambroisie"},
  {source: "L'Ambroisie", target: "French haute cuisine"},
  {source: "Jiro Ono", target: "Sukiyabashi Jiro"},
  {source: "Sukiyabashi Jiro", target: "Sushi"}
];

const nodeById = new Map(nodes.map((node) => [node.id, node]));
const linkRows = links.map((link) => ({
  ...link,
  x1: nodeById.get(link.source).x,
  y1: nodeById.get(link.source).y,
  x2: nodeById.get(link.target).x,
  y2: nodeById.get(link.target).y
}));
```

## Influence Graph

```js
const networkChart = Plot.plot({
  width: 900,
  height: 520,
  marginLeft: 120,
  marginRight: 180,
  x: {axis: null, domain: [-0.3, 2.7]},
  y: {axis: null, domain: [-1.2, 3]},
  color: {
    legend: true,
    domain: ["chef", "restaurant", "cuisine"],
    range: ["#fbbf24", "#06b6d4", "#f43f5e"]
  },
  style: {
    background: "#020617",
    color: "#f8fafc"
  },
  marks: [
    Plot.link(linkRows, {
      x1: "x1",
      y1: "y1",
      x2: "x2",
      y2: "y2",
      stroke: "#475569",
      strokeWidth: 2
    }),
    Plot.dot(nodes, {
      x: "x",
      y: "y",
      fill: "type",
      r: 10,
      stroke: "#f8fafc"
    }),
    Plot.text(nodes, {
      x: "x",
      y: "y",
      text: "id",
      dx: 14,
      fill: "#f8fafc",
      fontSize: 12,
      textAnchor: "start"
    })
  ]
});

display(networkChart);
```

## Network Data

```js
display(Inputs.table(nodes));
```
