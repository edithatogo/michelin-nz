# Aggregate Gastronomy Indicator Dashboard Specification

This document defines the current aggregate-only requirements for the dashboard. The canonical
MoSCoW register is [requirements.md](./requirements.md); this specification keeps the core
product scope and architecture summary close to the original Conductor setup.

## Requirements

### Must Have

* Country-level analysis of aggregate star counts against population and GDP.
* Build-time data preparation that emits compact Parquet assets for Observable Framework.
* Client-side charts and pivot controls over aggregate country metrics only.
* Clear source, license, and methodology notes for every redistributed metric.
* Explicit exclusion of restricted third-party source rows and submitted review content.
* Verified authorship and ORCID connection (`0000-0002-5364-1650`) for Dylan A. Mordaunt.

### Should Have

* Ruff, Pytest, property tests, basedpyright, npm lint, and static smoke checks in CI.
* Fail-closed data handling when upstream demographic APIs fail.
* Deterministic build artifacts for Hugging Face Spaces deployment.
* Repository documentation that keeps legal/data-scope limitations visible.

### Could Have

* A future Zenodo release after manual record review and DOI minting.
* Additional aggregate public indicators where redistribution rights are documented.
* More pivot dimensions if they remain aggregate and license-compatible.

### Won't Have

* Public individual restaurant records.
* Public review ingestion or review-derived analysis.
* Public guide text, coordinates, booking metadata, photos, or scraped source rows.

## Architecture And Data Flow

```mermaid
%%{init: {"flowchart": {"curve": "basis", "nodeSpacing": 55, "rankSpacing": 80}}}%%
flowchart LR
    classDef source fill:#e0f2fe,stroke:#0284c7,color:#0f172a
    classDef process fill:#ede9fe,stroke:#7c3aed,color:#0f172a
    classDef output fill:#dcfce7,stroke:#16a34a,color:#0f172a
    classDef deploy fill:#fef3c7,stroke:#d97706,color:#0f172a

    subgraph inputs["Aggregate Inputs"]
        direction TB
        WB["World Bank API<br/>Population and GDP"]
        AR["Local Archive<br/>Fallback indicators"]
        AG["Curated Aggregate Counts<br/>Country-level star totals"]
    end

    DL["Data Loader<br/>Python 3.14 + Polars"]
    MX["Metric Calculation<br/>Mojo parity backend"]
    AS["Versioned Assets<br/>Parquet + JSON"]
    OB["Observable Static Build<br/>Charts, tables, maps"]
    HF["Hugging Face Spaces<br/>Public dashboard"]

    WB -- "success" --> DL
    AR -. "fallback" .-> DL
    AG -- "counts" --> DL
    DL --> MX
    MX -- "per-capita + GDP ratios" --> AS
    AS --> OB
    OB --> HF

    class WB,AR,AG source
    class DL,MX process
    class AS,OB output
    class HF deploy
```
