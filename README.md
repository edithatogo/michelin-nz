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

A static Observable dashboard for gastronomy data analysis that visualizes selected Michelin Guide-style restaurant indicators alongside population, GDP, and geographic context.

Live Demo: [Hugging Face Spaces](https://huggingface.co/spaces/edithatogo/michelin-nz)  
Repository: [edithatogo/michelin-nz](https://github.com/edithatogo/michelin-nz)

---

## ⚖️ Data Ownership & Citation

> [!IMPORTANT]
> **Data Ownership Disclaimer:** Michelin Guide names, distinctions, ratings, text, branding, and related database rights are owned by **Manufacture Française des Pneumatiques Michelin (Michelin Group)** or its licensors. This repository's MIT license applies to the dashboard code only; it does not license Michelin-derived data. Do not redistribute a comprehensive scraped Michelin database from this repository without confirming permission or another valid legal basis.
>
> World Bank indicators are reused from World Bank Open Data and require source attribution under the World Bank dataset terms.

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

No Zenodo DOI has been minted yet. The repository includes `.zenodo.json` metadata so Zenodo can create a DOI after the GitHub integration is enabled.

To activate permanent DOI minting for releases:
1. Log into your account on [Zenodo](https://zenodo.org/) using your GitHub credentials.
2. Go to your **GitHub Settings** panel on Zenodo and toggle the switch for `edithatogo/michelin-nz` to **On**.
3. Create a new GitHub Release/Tag. Zenodo will automatically mint a permanent DOI using the metadata in `.zenodo.json`.
4. Replace this note with the minted DOI badge/link after Zenodo publishes the record.

See [Release Checklist](docs/release-checklist.md) before publishing DOI-bearing releases.

---

## 🚀 Architecture & Tech Stack

- **Core Engine:** [Observable Framework](https://observablehq.com/framework/) - Static site generator optimized for data-dense dashboards.
- **Visualization:** [Observable Plot](https://observablehq.com/plot/) renders deterministic SVG charts that are covered by headless deployment smoke tests.
- **Build-Time Data Pipeline:** Python loaders compile selected restaurant records, World Bank demographics, and GDP indicators into JSON and Parquet assets at build time.
- **Interactive Analysis:** Observable Inputs provide country filters, measure selectors, aggregation controls, and data tables.

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
   pip install polars requests beautifulsoup4 pyarrow pytest pytest-cov hypothesis ruff basedpyright
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

This project's source code is licensed under the MIT License. See [LICENSE](file:///Volumes/PortableSSD/GitHub/michelin-nz/LICENSE) for details. Third-party data, names, marks, and ratings remain subject to their original owners' terms.

To cite this project, please refer to [CITATION.cff](file:///Volumes/PortableSSD/GitHub/michelin-nz/CITATION.cff).
