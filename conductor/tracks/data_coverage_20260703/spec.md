# Track Specification: Michelin Star Country Coverage and Aggregate Data Completeness

## Overview

The current dashboard data contains only five country aggregates. This track expands the
aggregate dataset so every country with current Michelin Star awards is either included with
documented aggregate counts or explicitly documented as out of scope because no reliable,
redistributable aggregate source is available.

## Functional Requirements

- Build a canonical Michelin Star country coverage ledger from documented sources, prioritising
  official Michelin Guide pages such as `https://guide.michelin.com/en/michelin-guides-worldwide`
  and current official restaurant/search pages.
- Add a source confidence field for each country, using `official`, `official-derived`,
  `secondary`, `withheld`, or `unverified`.
- Explicitly handle guide geography edge cases such as Hong Kong/Macau, UK/Ireland, Nordic
  countries, Belgium/Luxembourg, and city/state guides in the United States.
- Replace the hard-coded five-country sample with a maintainable aggregate-only input source.
- Preserve the public artifact boundary: publish country-level counts and derived ratios only,
  without restaurant names, review text, booking links, photos, or row-level source records.
- Add a coverage audit that fails when a canonical star country is missing from the aggregate
  input source or when a public row contains restricted restaurant-level fields.
- Refresh World Bank fallback archives or document any country without matched population/GDP
  values so the build fails closed rather than silently dropping countries.
- Update source and methodology notes to state the coverage date, source basis, known limitations,
  and any countries withheld for licensing or evidence reasons.

## Non-Functional Requirements

- Data generation remains deterministic and works without network access by using archived
  fallback files.
- Tests must enforce aggregate-only schema boundaries and coverage completeness.
- Any new source file must include source URL, accessed date, and a short redistribution note.

## Acceptance Criteria

- The local aggregate source includes every current Michelin Star country that can be supported
  by documented aggregate evidence.
- Any excluded country is listed in a repo-local coverage ledger with the reason and source status.
- Country coverage rows include source confidence and guide geography classification.
- `build_country_metrics()` emits only aggregate country metrics and no row-level restaurant
  fields.
- The generated dashboard shows the refreshed country count and totals.
- Ruff, pytest with coverage, basedpyright, npm lint, Observable build, and static smoke checks
  pass.

## Out of Scope

- Restaurant-level records, reviews, exact coordinates, or guide-like search/database features.
- New map routes or visual scoring loops; those are covered by separate tracks.
