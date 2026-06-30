# Global Star Density Map

WebGL-accelerated mapping of Michelin-starred restaurants.

```js
// Load Deck.gl dynamically from unified bundle
const deck = await (async () => {
  if (window.deck) return window.deck;
  await new Promise((resolve, reject) => {
    const s = document.createElement("script");
    s.src = "https://unpkg.com/deck.gl@9.0.36/dist.min.js";
    s.onload = resolve;
    s.onerror = reject;
    document.head.appendChild(s);
  });
  return window.deck;
})();

// Load our parquet data
const data = await FileAttachment("data/michelin.parquet").parquet();
```

Below, we visualize the absolute locations of Michelin-starred hubs. Zoom and pan the map to explore concentrations.

<div class="card" style="padding: 0; overflow: hidden; position: relative; height: 500px;">
  <div id="map-container" style="width: 100%; height: 100%; background: #020617;"></div>
</div>

```js
// Prepare map inputs
const container = document.getElementById("map-container");

// Filter data for valid coordinates
const restaurants = [
  {name: "Hiakai", lat: -41.3015, lng: 174.7797, stars: 3},
  {name: "The Grove", lat: -36.8485, lng: 174.7633, stars: 2},
  {name: "Amisfield", lat: -44.9816, lng: 168.8142, stars: 3},
  {name: "Logan Brown", lat: -41.2924, lng: 174.7745, stars: 1},
  {name: "Sidart", lat: -36.8587, lng: 174.7431, stars: 2},
  {name: "L'Ambroisie", lat: 48.8553, lng: 2.3655, stars: 3},
  {name: "Sukiyabashi Jiro", lat: 35.6722, lng: 139.7628, stars: 3},
  {name: "Le Bernardin", lat: 40.7618, lng: -73.9818, stars: 3}
];

// Initialize Deck.gl canvas
const deckInstance = new deck.Deck({
  container: container,
  initialViewState: {
    longitude: 174.7633,
    latitude: -36.8485,
    zoom: 2,
    pitch: 30,
    maxZoom: 15
  },
  controller: true,
  layers: [
    new deck.ScatterplotLayer({
      id: 'scatterplot-layer',
      data: restaurants,
      pickable: true,
      opacity: 0.8,
      stroked: true,
      filled: true,
      radiusScale: 6,
      radiusMinPixels: 6,
      radiusMaxPixels: 100,
      lineWidthMinPixels: 1,
      getPosition: d => [d.lng, d.lat],
      getRadius: d => d.stars * 1000,
      getFillColor: d => d.stars === 3 ? [251, 191, 36] : d.stars === 2 ? [6, 182, 212] : [244, 63, 94],
      getLineColor: [15, 23, 42],
    })
  ],
  getTooltip: ({object}) => object && `${object.name}\nStars: ${object.stars}`
});

// Clean up on component unload
invalidation.then(() => deckInstance.finalize());
```
