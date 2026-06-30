# Project Tracks Index

This index tracks all developmental phases of the Michelin Star Per-Capita Dashboard.

## Tracks Status

| ID | Title | Status | Link |
| :--- | :--- | :--- | :--- |
| `bootstrap` | Project Scaffolding & Observable Bootstrapping | `archived` | [bootstrap/index.md](file:///Volumes/PortableSSD/GitHub/michelin-nz/conductor/archive/bootstrap/index.md) |
| `data_loader` | Data loader Pipeline & Scraping | `archived` | [data_loader/index.md](file:///Volumes/PortableSSD/GitHub/michelin-nz/conductor/archive/data_loader/index.md) |
| `core_viz` | Core Visualizations & DuckDB Integration | `archived` | [core_viz/index.md](file:///Volumes/PortableSSD/GitHub/michelin-nz/conductor/archive/core_viz/index.md) |
| `mapping` | WebGL Mapping & Spatial Binning | `archived` | [mapping/index.md](file:///Volumes/PortableSSD/GitHub/michelin-nz/conductor/archive/mapping/index.md) |
| `linking_cms` | Deep Linking, Community Review CMS & Automation | `active` | [linking_cms/index.md](file:///Volumes/PortableSSD/GitHub/michelin-nz/conductor/tracks/linking_cms/index.md) |

## Development Rules
* Each track must be developed in a dedicated Git feature branch (e.g. `feat/bootstrap`).
* Standard workflow: Task completion -> Local Verify -> `/conductor:review` -> Commit with notes -> Push to origin -> Open PR -> Merge PR -> Verify GH Actions pass.
* Keep GitHub issues updated for each track scope.
