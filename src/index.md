# Michelin Star Per-Capita Dashboard

Welcome to the **Michelin Star Per-Capita Dashboard**. This project visualizes global fine dining density metrics by normalising Michelin ratings with demographic and economic data.

<div class="dashboard-grid">
  <div class="card">
    <h2>NZ Analysis</h2>
    <p>Localised look at New Zealand's top culinary establishments, matching Hat indicators to Star metrics across cities.</p>
    <a href="./nz">Explore NZ Data &rarr;</a>
  </div>
  <div class="card">
    <h2>Global Map</h2>
    <p>Zoomable WebGL globe representing culinary star density adjusted per 100,000 residents.</p>
    <a href="./global-map">View Globe &rarr;</a>
  </div>
  <div class="card">
    <h2>GDP vs. Stars</h2>
    <p>Interactive scatter plot and metrics correlating culinary intensity against national economic size.</p>
    <a href="./gdp-stars">Analyze Economic Data &rarr;</a>
  </div>
</div>

---

## 📊 Methodology & Disclaimers

<div class="card" style="border-left: 4px solid var(--theme-accent); background: rgba(15, 23, 42, 0.4); margin-top: 1.5rem;">
  <h3>⚠️ Fine Dining Density Normalization</h3>
  <p>Please note the following constraints when interpreting the demographic metrics on this dashboard:</p>
  <ul>
    <li><strong>Michelin Guide Coverage:</strong> The Michelin Guide is city/region-based and does not cover all territories within listed countries (e.g. only select metropolitan areas in the United States or Japan are graded). Comparison values represent guide density rather than absolute country capacity.</li>
    <li><strong>New Zealand "Hats" translation:</strong> New Zealand cuisine guides historically utilize the "Cuisine Good Food Awards" Hat indicators. For cross-border benchmarking on this dashboard, Hats are translated to Stars using an equivalence ratio of: <em>3 Hats = 3 Stars, 2 Hats = 2 Stars, 1 Hat = 1 Star</em>.</li>
    <li><strong>Demographics Sources:</strong> Population and GDP stats are pulled dynamically from the official World Bank Open API data sets (2024 records).</li>
  </ul>
</div>

