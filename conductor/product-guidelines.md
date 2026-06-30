# Product Guidelines: Michelin Star Per-Capita Dashboard

## Design & Aesthetics
* **Theme:** Sleek Dark Mode (Deep slate `#0f172a` and midnight navy `#020617` backgrounds).
* **Color Palette:**
  - Backgrounds: Dark slate/blue values.
  - Michelin Stars: Neon Gold/Yellow glow effects (`#fbbf24`, `drop-shadow`).
  - Data Gradients: High-visibility neon accents (e.g., cyan `#06b6d4`, violet `#8b5cf6`, rose `#f43f5e`) to represent varying densities of stars or GDP per capita.
* **Typography:** Modern, clean sans-serif (e.g., *Outfit* or *Inter* from Google Fonts) to project a premium, state-of-the-art feel.

## User Experience (UX) & Interactions
* **Micro-interactions:** Smooth hover triggers on maps, chart elements, and scatter points with detailed, custom tooltips.
* **View Transitions API:** Implement native browser View Transitions so components visually morph and transition smoothly when switching tabs or views.
* **Map Controls:** High-performance, zoomable global map (Deck.gl/Maplibre GL) allowing seamless transitions from world-level views down to city and restaurant level.
* **GPU-Accelerated Spatial Hexbins:** Support 3D hexagonal density columns using Deck.gl to represent star concentrations in dense metropolitan hubs.
* **Natural Language Query Interface:** Integration of a simple search box translating client requests to client-side SQL executing on DuckDB WASM via a lightweight LLM agent.
* **Interactive Controls:** Sliders to filter records dynamically (e.g., filtering by GDP per capita range, population, or number of stars), instantly updating all visible charts.
* **Animations:** Playable timeline transition animations showing geographic expansion of the Michelin Guide globally over time.

## Data Interpretation, Methodology & Integrity
* **ISO-Standardized Keys:** Use ISO 3166-1 alpha-3 codes for countries and ISO 3166-2 for regional boundaries to guarantee matching.
* **Methodology Overlay:** Informative guidelines outlining regional coverage restrictions of the Michelin Guide and details on the Hat-to-Star NZ translation weight.
* **Visual Density & Lineage:** Clear grouping of controls. Add an interactive "Data Lineage Graph" mapping origin verification (original source APIs -> build compilation -> current visualization).
* **Performance First:** Heavy datasets should be pre-aggregated or processed into optimized static JSON/Parquet assets so that page loads and transitions are instantaneous.
