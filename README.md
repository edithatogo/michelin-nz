---
title: Michelin Star Per-Capita Dashboard
emoji: 🍳
colorFrom: yellow
colorTo: blue
sdk: static
pinned: false
---

# Michelin Star Per-Capita Dashboard

[![Verify Status](https://github.com/edithatogo/michelin-nz/actions/workflows/verify.yml/badge.svg)](https://github.com/edithatogo/michelin-nz/actions/workflows/verify.yml)
[![Hugging Face Space](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Space-yellow)](https://huggingface.co/spaces/edithatogo/michelin-nz) 
[![ORCID](https://img.shields.io/badge/ORCID-0000--0002--5364--1650-green.svg)](https://orcid.org/0000-0002-5364-1650)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/)

A visually stunning, bleeding-edge dashboard for **open-source gastronomy data science** that visualizes the distribution of Michelin-starred restaurants globally, adjusted for population, GDP, and geographic location.

Live Demo: [Hugging Face Spaces](https://huggingface.co/spaces/edithatogo/michelin-nz)  
Repository: [edithatogo/michelin-nz](https://github.com/edithatogo/michelin-nz)

---

## ⚖️ Data Ownership & Citation

> [!IMPORTANT]
> **Data Ownership Disclaimer:** The underlying restaurant names, coordinates, and star ratings are the intellectual property and copyright of **Manufacture Française des Pneumatiques Michelin (Michelin Group)**. This dashboard is an academic/visual data project using public and scraped records for educational benchmarking.

To cite this repository in academic or journalistic publications, please refer to [CITATION.cff](file:///Volumes/PortableSSD/GitHub/michelin-nz/CITATION.cff) or use:
```bibtex
@software{michelin_nz_dashboard_2026,
  author = {Mordaunt, Dylan A},
  title = {Michelin Star Per-Capita Dashboard},
  url = {https://github.com/edithatogo/michelin-nz},
  year = {2026}
}
```

---

## 🗄️ Zenodo Archive Linkage

To activate permanent DOI minting for releases:
1. Log into your account on [Zenodo](https://zenodo.org/) using your GitHub credentials.
2. Go to your **GitHub Settings** panel on Zenodo and toggle the switch for `edithatogo/michelin-nz` to **On**.
3. Create a new GitHub Release/Tag. Zenodo will automatically mint a permanent DOI using the metadata in `.zenodo.json`!

---

## 🚀 Bleeding-Edge Architecture & Tech Stack

- **Core Engine:** [Observable Framework](https://observablehq.com/framework/) - Static site generator optimized for data-dense dashboards.
- **In-Browser Database:** [DuckDB WASM](https://duckdb.org/) - Executes analytical SQL queries directly on compressed `.parquet` tables inside the browser.
- **WebGL Mapping:** [Deck.gl](https://deck.gl/) - Renders thousands of geographic coordinates at native GPU speeds.
- **GPU Graph Networks:** [Cosmograph](https://cosmograph.app/) (cosmos.gl) - Renders culinary influence networks and chef lineages at 60fps.
- **Scraper & Triangulation Pipeline:** Python loaders fetch demographics (World Bank/UN API) and scrape live restaurant data, saving compressed `.parquet` assets at build time.

---

## 🛠️ Installation & Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/edithatogo/michelin-nz.git
   cd michelin-nz
   ```

2. **Setup Python Virtual Environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install pandas requests beautifulsoup4 pyarrow
   ```

3. **Install Node Packages:**
   ```bash
   npm install
   ```

4. **Run Local Dev Server:**
   ```bash
   npm run dev
   ```
   Open `http://localhost:3000` to preview the dashboard.

---

## 📂 Project Structure

- `src/` - Observable Framework markdown and styles.
- `src/data/` - Build-time data loaders (`michelin.parquet.sh`, `michelin.py`).
- `src/data/reviews/` - Community blog review submissions (`.json` format).
- `conductor/` - Conductor project setup, specs, and workflow guidelines.

---

## 🤝 How to Contribute

We welcome community contributions, particularly from food bloggers, critics, and data enthusiasts:
1. Refer to [CONTRIBUTING.md](file:///Volumes/PortableSSD/GitHub/michelin-nz/CONTRIBUTING.md) to submit pull requests for new restaurant listings or blog reviews.
2. Read the methodology and data matching rules inside the dashboard overlays.

---

## 📄 License & Citation

This project is open-source and licensed under the MIT License. See [LICENSE](file:///Volumes/PortableSSD/GitHub/michelin-nz/LICENSE) for details.

To cite this project, please refer to [CITATION.cff](file:///Volumes/PortableSSD/GitHub/michelin-nz/CITATION.cff).
