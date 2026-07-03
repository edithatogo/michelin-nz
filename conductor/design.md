# Design

This document records the Conductor design model for the dashboard and its planned extensions.

## System Data Flow

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

## Track Dependency Design

```mermaid
flowchart TD
    R["Requirements<br/>MoSCoW scope"] --> C["Contracts<br/>data, visual, CI, deployment"]
    C --> M["Mojo Migration<br/>metric parity"]
    C --> D["Data Coverage<br/>country ledger"]
    D --> G["Geo Outcomes<br/>choropleth + NZ safe view"]
    M --> Q["Live Quality Score<br/>repo + visual scorecards"]
    G --> Q
    Q --> HF["Hugging Face deployment<br/>live contract proof"]
```

## Visualisation Design

```mermaid
flowchart LR
    CM["country_metrics.json"] --> Home["/ index<br/>summary chart + table"]
    CM --> GDP["/gdp-stars<br/>bounded country selector + scatter"]
    CM --> NZ["/nz<br/>NZ aggregate benchmark"]
    CM --> Pivot["/pivot<br/>bounded star-country pivot"]
    CM --> Sources["/sources<br/>source ledger"]
    CM -. "planned" .-> Map["/global-map<br/>choropleth"]
    CM -. "planned" .-> NZLoc["/nz-locations<br/>location-safe aggregate view"]
```

## Design Rules

- Public pages must communicate aggregate analysis first, not marketing copy.
- Controls must be bounded enough to remain inspectable on desktop and mobile.
- Charts must render nonblank SVG marks or provide explicit empty states.
- Geographic views must distinguish supported, missing, withheld, and unverified data.
- Exact public point data for New Zealand is blocked unless source and redistribution rights are
  documented first.
