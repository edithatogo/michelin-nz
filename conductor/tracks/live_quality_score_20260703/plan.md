# Implementation Plan: Live Deployment And Repository Quality Scorecard

## Phase 1: Parity And Scorecard Design

- [ ] Task: Define live parity checks
    - [ ] Check local `HEAD`, `origin/main`, GitHub default branch, open PR state, and Hugging Face route responses.
    - [ ] Check live data asset references from built HTML rather than assuming `/data/*.json` paths are public.
    - [ ] Check a deployed build manifest with git SHA, data hash, build time, and route list.
    - [ ] Define pass/fail outcomes that separate repo defects from external service blockers.
- [ ] Task: Define quality rubrics
    - [ ] Create a 1000-point visual dashboard rubric with route coverage, data freshness, layout, accessibility, mobile behaviour, copy, and chart correctness categories.
    - [ ] Create a 100-point repository rubric with CI, tests, type safety, docs, metadata, licensing, deployment, and source integrity categories.
    - [ ] Document threshold handling: visual score must be greater than 995/1000 and repo score must equal 100/100.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Parity And Scorecard Design' (Protocol in workflow.md)

## Phase 2: Automated Checks And Reports

- [ ] Task: Implement parity and scoring commands
    - [ ] Add a script or documented command bundle that verifies GitHub PR state, branch SHA parity, Hugging Face route status, and live data asset status.
    - [ ] Keep GitHub release, Hugging Face, and Zenodo checks strict in the scheduled external deployment workflow.
    - [ ] Add score output that records component scores, failures, and external blockers.
    - [ ] Ensure the checks can run locally without mutating repo-tracked state.
- [ ] Task: Add tests for scoring behaviour
    - [ ] Test successful live-parity parsing with mocked responses.
    - [ ] Test open PR, stale data asset, route failure, and external-blocker cases.
    - [ ] Test that scores cannot pass when required evidence is missing.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Automated Checks And Reports' (Protocol in workflow.md)

## Phase 3: Score Loop And Final Quality Gate

- [ ] Task: Run the dashboard visual improvement loop
    - [ ] Score the current live and local dashboard.
    - [ ] Fix the highest-impact defects until the visual score is greater than 995/1000.
    - [ ] Preserve evidence for each score iteration in a repo-local report.
- [ ] Task: Run the repository improvement loop
    - [ ] Score the repository against the 100-point rubric.
    - [ ] Fix gaps until the repository score is 100/100 or an external blocker is documented.
    - [ ] Replace overbroad quality or security claims with precise contract-check wording.
    - [ ] Record recommended future improvements that are outside the current track.
- [ ] Task: Run full quality gates
    - [ ] Run `pixi run format-check` and `pixi run mojo-format-check`.
    - [ ] Run `pixi run lint`.
    - [ ] Run `pixi run pytest --cov=src/data --cov-fail-under=85`.
    - [ ] Run `pixi run typecheck`.
    - [ ] Run `npm run lint`, `npm run format:check`, `npm run audit`, `OBSERVABLE_TELEMETRY_DISABLE=true npm run build`, and `npm run smoke:dist`.
    - [ ] Run the external deployment check and the new scorecard command.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Score Loop And Final Quality Gate' (Protocol in workflow.md)
