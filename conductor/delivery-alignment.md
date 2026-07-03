# Delivery Alignment

This ledger checks delivered work against the current Conductor plan. It is intentionally
conservative: work is marked delivered only when it exists in the repo or has live verification.

## Delivered And Aligned

| Planned Area | Evidence | Alignment |
| --- | --- | --- |
| Aggregate-only dashboard routes | `/`, `/gdp-stars`, `/nz`, `/pivot`, `/sources` live on Hugging Face | Aligned with aggregate public-data boundary |
| Strict Python 3.14 tooling | `pixi.toml`, `pixi.lock`, `pyproject.toml`, GitHub `Verify Code Quality & Testing` | Aligned with build/code quality contract |
| Mojo metric migration slice | `src/data/metrics.mojo`, `src/data/michelin.py`, `tests/test_michelin.py` | Aligned with Mojo Phase 1 and Phase 2 implementation tasks |
| Observable loader compatibility in CI | `src/data/country_metrics.json.sh`, `src/data/michelin.parquet.sh` use Pixi when available | Aligned with strict deployment workflow |
| Live visual contract pass | Chrome checks across `/`, `/gdp-stars`, `/nz`, `/pivot`, `/sources` | Aligned with live quality visual contract for existing routes |
| Hugging Face deployment | Scheduled deployment workflow success and Space runtime `RUNNING` | Aligned with deployment contract |
| Architecture diagram | `conductor/spec.md` and `conductor/design.md` Mermaid diagrams rendered locally | Aligned with design documentation requirement |

## Partially Delivered

| Planned Area | Delivered | Remaining Work |
| --- | --- | --- |
| Live quality scorecard | CI, deployment, route checks, and manual Chrome contract checks are in place | Add repeatable scorecard command and checked-in score reports |
| Mojo migration | Metric calculations and CI checks are migrated | Review future pure numeric transformations after data coverage expansion |
| Repository setup automation | Strict workflows and deployment are green | Zenodo remains an external manual publication gate |

## Planned But Not Yet Delivered

| Track | Planned Outcome | Current Reason |
| --- | --- | --- |
| `data_coverage_20260703` | Canonical Michelin Star country ledger and complete aggregate coverage | Requires source research and redistribution review |
| `geo_outcomes_20260703` | `/global-map` choropleth and New Zealand location-safe visualisation | Depends on refreshed coverage ledger and map source contract |
| `live_quality_score_20260703` | Deterministic scorecards greater than 995/1000 and 100/100 | Needs implemented scoring command and evidence report |

## Current External Gates

- Zenodo DOI has not been minted. The repo contains `.zenodo.json`, but publication requires
  manual Zenodo GitHub integration and a DOI-bearing release.
- Live Hugging Face deployment is current and running, but documentation-only Conductor files are
  not visible on the public Observable site unless a methodology/architecture page is added.
