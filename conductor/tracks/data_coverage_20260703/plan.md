# Implementation Plan: Michelin Star Country Coverage and Aggregate Data Completeness

## Phase 1: Coverage Ledger And Tests

- [x] Task: Define the canonical coverage contract
    - [x] Add a repo-local aggregate coverage ledger with country code, country name, source URL, accessed date, total restaurant count, total star count, and redistribution note.
    - [x] Add source confidence values for the delivered snapshot.
    - [x] Define guide geography classifications for country, region, city/state, and combined guide areas.
    - [ ] Record all unsupported or withheld countries with an explicit reason rather than dropping them silently.
    - [ ] Update product/source documentation to describe the coverage date and aggregate-only boundary.
- [ ] Task: Write failing coverage tests
    - [x] Test that the supported canonical country set is no longer the five-row sample.
    - [ ] Test that withheld countries have source status and reason fields.
    - [ ] Test that aggregate inputs reject restaurant-level fields such as name, address, latitude, longitude, review text, and booking URL.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Coverage Ledger And Tests' (Protocol in workflow.md)

## Phase 2: Aggregate Data Loader Refresh

- [x] Task: Implement maintainable aggregate country loading
    - [x] Replace the hard-coded five-row sample with the coverage ledger loader.
    - [x] Keep public metric output restricted to aggregate country fields and derived ratios.
    - [x] Make missing demographic joins fail closed unless documented in the ledger.
- [ ] Task: Refresh deterministic fallback data
    - [x] Add ledger-level population and GDP fallbacks for all supported rows.
    - [ ] Verify the data loader works without live network access.
    - [x] Regenerate dashboard data artifacts from the refreshed loader.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Aggregate Data Loader Refresh' (Protocol in workflow.md)

## Phase 3: Documentation And Verification

- [ ] Task: Update public methodology surfaces
    - [x] Update the sources page with coverage date and source hierarchy for the delivered snapshot.
    - [ ] Document Hong Kong/Macau, UK/Ireland, Nordic, Belgium/Luxembourg, and US city/state guide handling.
    - [ ] Update README or Conductor docs where they still imply a small compiled sample.
    - [x] Ensure the dashboard cards and tables use the refreshed country totals.
- [ ] Task: Run full quality gates
    - [x] Run `pixi run lint`.
    - [x] Run `pixi run pytest --cov=src/data --cov-fail-under=85`.
    - [x] Run `pixi run typecheck`.
    - [x] Run `npm run lint`, `OBSERVABLE_TELEMETRY_DISABLE=true npm run build`, and `npm run smoke:dist`.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Documentation And Verification' (Protocol in workflow.md)
