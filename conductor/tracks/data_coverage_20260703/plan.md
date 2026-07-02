# Implementation Plan: Michelin Star Country Coverage and Aggregate Data Completeness

## Phase 1: Coverage Ledger And Tests

- [ ] Task: Define the canonical coverage contract
    - [ ] Add a repo-local aggregate coverage ledger with country code, country name, source URL, accessed date, total restaurant count, total star count, and redistribution note.
    - [ ] Add source confidence values: `official`, `official-derived`, `secondary`, `withheld`, and `unverified`.
    - [ ] Define guide geography classifications for country, region, city/state, and combined guide areas.
    - [ ] Record all unsupported or withheld countries with an explicit reason rather than dropping them silently.
    - [ ] Update product/source documentation to describe the coverage date and aggregate-only boundary.
- [ ] Task: Write failing coverage tests
    - [ ] Test that every supported canonical country appears in aggregate inputs.
    - [ ] Test that withheld countries have source status and reason fields.
    - [ ] Test that aggregate inputs reject restaurant-level fields such as name, address, latitude, longitude, review text, and booking URL.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Coverage Ledger And Tests' (Protocol in workflow.md)

## Phase 2: Aggregate Data Loader Refresh

- [ ] Task: Implement maintainable aggregate country loading
    - [ ] Replace the hard-coded five-row sample with the coverage ledger loader.
    - [ ] Keep public metric output restricted to aggregate country fields and derived ratios.
    - [ ] Make missing demographic joins fail closed unless documented in the ledger.
- [ ] Task: Refresh deterministic fallback data
    - [ ] Update archived World Bank population and GDP fixtures for all supported countries.
    - [ ] Verify the data loader works without live network access.
    - [ ] Regenerate dashboard data artifacts from the refreshed loader.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Aggregate Data Loader Refresh' (Protocol in workflow.md)

## Phase 3: Documentation And Verification

- [ ] Task: Update public methodology surfaces
    - [ ] Update the sources page with coverage date, source hierarchy, and withheld-country handling.
    - [ ] Document Hong Kong/Macau, UK/Ireland, Nordic, Belgium/Luxembourg, and US city/state guide handling.
    - [ ] Update README or Conductor docs where they still imply a small compiled sample.
    - [ ] Ensure the dashboard cards and tables use the refreshed country totals.
- [ ] Task: Run full quality gates
    - [ ] Run `pixi run lint`.
    - [ ] Run `pixi run pytest --cov=src/data --cov-fail-under=85`.
    - [ ] Run `pixi run typecheck`.
    - [ ] Run `npm run lint`, `OBSERVABLE_TELEMETRY_DISABLE=true npm run build`, and `npm run smoke:dist`.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Documentation And Verification' (Protocol in workflow.md)
