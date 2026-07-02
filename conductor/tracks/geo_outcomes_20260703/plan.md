# Implementation Plan: Global Choropleth And New Zealand Location-Safe Visualisation

## Phase 1: Mapping Contract And Test Fixtures

- [ ] Task: Define aggregate map data contracts
    - [ ] Add a country geometry source with documented licence and stable build path.
    - [ ] Define the metric fields available to the choropleth from `country_metrics`.
    - [ ] Define the New Zealand location-safe source format as region/city aggregates by default.
- [ ] Task: Write failing map tests
    - [ ] Test that map data joins every supported country by ISO code or records a documented miss.
    - [ ] Test that New Zealand location data rejects restaurant names, addresses, reviews, and guide-derived exact coordinates.
    - [ ] Test that smoke routes expect `/global-map` to be live after implementation.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Mapping Contract And Test Fixtures' (Protocol in workflow.md)

## Phase 2: Global Choropleth Implementation

- [ ] Task: Build the `/global-map` page
    - [ ] Add route navigation and page content for a global choropleth.
    - [ ] Add metric selector controls for aggregate counts, star density, GDP-normalised intensity, and coverage status.
    - [ ] Add missing, withheld, and unverified coverage states to the legend.
    - [ ] Add legends, missing-data treatment, and methodology notes on the page.
- [ ] Task: Keep deployment route behaviour consistent
    - [ ] Update static smoke tests so `/global-map` must return 200.
    - [ ] Keep `/network` returning 404 unless a separate current implementation is added.
    - [ ] Verify the compiled route is present in `dist`.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Global Choropleth Implementation' (Protocol in workflow.md)

## Phase 3: New Zealand Location-Safe Visualisation And Outcome Review

- [ ] Task: Add the New Zealand location visualisation
    - [ ] Render region/city aggregate or centroid-level data only when source and licence notes are present.
    - [ ] Render an explicit no-verified-public-point-data state if exact location rights are not documented.
    - [ ] Link the visualisation from the existing New Zealand page.
- [ ] Task: Add additional aggregate-safe outcomes
    - [ ] Review candidate outcomes for usefulness and source safety.
    - [ ] Implement selected outcomes such as restaurants per million, stars per restaurant, GDP/population quadrants, and guide coverage type.
    - [ ] Document recommendations that are valuable but not yet source-supported.
- [ ] Task: Run full quality gates
    - [ ] Run Python and JavaScript lint/type/test commands required by the workflow.
    - [ ] Build the Observable site and run static smoke tests.
    - [ ] Inspect desktop and mobile map rendering before marking the phase complete.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: New Zealand Location-Safe Visualisation And Outcome Review' (Protocol in workflow.md)
