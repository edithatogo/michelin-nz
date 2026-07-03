# Contracts

This document defines the contracts used to decide whether planned work is complete.

## Data Contract

- Public generated assets may contain only aggregate country-level fields and derived metrics.
- Forbidden public fields include restaurant name, address, latitude, longitude, review text,
  booking URL, photo URL, source row identifier, or guide-like record metadata.
- `country_metrics` rows must preserve stable country code, country name, population, GDP,
  aggregate restaurant count, aggregate star count, stars per 100k residents, GDP per capita, and
  stars per $10B GDP.
- Future coverage rows must include source URL, accessed date, source confidence, redistribution
  note, guide geography classification, and withheld/unverified reason where applicable.
- Build-time data generation must fail closed when required coverage or demographic joins are
  missing without documented exception.

## Build And Code Quality Contract

- Python runs through Pixi with Python 3.14.
- Mojo is installed through Pixi and must pass version, format, build, and metric smoke checks.
- Ruff format, Ruff lint, basedpyright strict typecheck, pytest coverage, ESLint with
  `--max-warnings=0`, Prettier check, npm audit, Observable build, and static smoke tests must
  pass before claiming repo-local completion.
- The repository contract script must use precise pass/fail wording and must not claim broad
  security coverage beyond the checks it runs.

## Visual Contract

- Every public route must return HTTP 200 after deployment.
- Every public route must have a nonempty title, H1, and visible navigation.
- Chart routes must render real nonblank SVG marks or a documented empty state.
- Pages must have no incoherent horizontal overflow on desktop or mobile.
- Visible text must not be clipped by its container.
- Selectors and checkbox groups must be bounded enough to inspect without overwhelming the first
  screen.
- Chrome visual checks must be used for live route verification before claiming visual completion.

## Deployment Contract

- `main`, `origin/main`, and GitHub default branch must point to the same intended commit before
  claiming remote parity.
- Open PRs and issues must be checked before claiming all work has been merged or addressed.
- Hugging Face Spaces must report a public static SDK Space with runtime stage `RUNNING`.
- Live route checks must inspect the static host, not only the Hugging Face repository metadata.
- Zenodo DOI is a manual external publication gate and remains blocked until a DOI-bearing record
  exists.

## Track Completion Contract

- Each active track must have a specification, implementation plan, and metadata.
- Track plan checkboxes must reflect actual delivered work, not intended work.
- Delivered work must cite evidence in `delivery-alignment.md` or an equivalent track closeout.
- Tracks may remain active when future work is real; partial delivery must be labelled explicitly.
