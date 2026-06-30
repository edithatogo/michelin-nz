# Chef & Cuisine Influence Network

WebGL-accelerated mapping of culinary relationships using Cosmograph.

```js
// Load Cosmograph dynamically from UMD bundle
const cosmographLib = await (async () => {
  if (window.Cosmograph) return window.Cosmograph;
  await new Promise((resolve, reject) => {
    const s = document.createElement("script");
    s.src = "https://unpkg.com/cosmograph@1.4.1/dist/cosmograph.min.js";
    s.onload = resolve;
    s.onerror = reject;
    document.head.appendChild(s);
  });
  return window.Cosmograph;
})();
```

Explore nodes representing chefs and restaurants, grouped by geographic hub. Drag nodes to inspect links.

<div class="card" style="padding: 0; overflow: hidden; position: relative; height: 500px;">
  <div id="network-container" style="width: 100%; height: 100%; background: #020617;"></div>
</div>

```js
const container = document.getElementById("network-container");

// Setup sample nodes (chefs & styles) and connection links
const nodes = [
  {id: "Monique Fiso", type: "chef", hub: "NZL"},
  {id: "Hiakai", type: "restaurant", hub: "NZL"},
  {id: "French Bistro", type: "cuisine", hub: "FRA"},
  {id: "Bernard Pacaud", type: "chef", hub: "FRA"},
  {id: "L'Ambroisie", type: "restaurant", hub: "FRA"},
  {id: "Modern Maori", type: "cuisine", hub: "NZL"},
  {id: "Jiro Ono", type: "chef", hub: "JPN"},
  {id: "Sukiyabashi Jiro", type: "restaurant", hub: "JPN"},
  {id: "Sushi", type: "cuisine", hub: "JPN"}
];

const links = [
  {source: "Monique Fiso", target: "Hiakai"},
  {source: "Hiakai", target: "Modern Maori"},
  {source: "Bernard Pacaud", target: "L'Ambroisie"},
  {source: "L'Ambroisie", target: "French Bistro"},
  {source: "Jiro Ono", target: "Sukiyabashi Jiro"},
  {source: "Sukiyabashi Jiro", target: "Sushi"},
  {source: "Monique Fiso", target: "French Bistro"} // Connection link showing French training influence
];

// Initialize Cosmograph canvas
const graph = new cosmographLib(container, {
  nodes: nodes,
  links: links,
  nodeColor: d => d.type === "chef" ? "#fbbf24" : d.type === "restaurant" ? "#06b6d4" : "#f43f5e",
  nodeSize: 10,
  linkWidth: 1,
  linkColor: "#1e293b",
  simulation: {
    linkDistance: 30,
    repulsion: 15
  }
});

// Clean up canvas on page change
invalidation.then(() => graph.destroy());
```
