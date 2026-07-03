# Implementation Plan: Live Deployment And Repository Quality Scorecard

## Phase 1: Parity And Scorecard Design

- [x] Task: Define live parity checks
    - [x] Check local `HEAD`, `origin/main`, GitHub default branch, open PR state, and Hugging Face route responses.
    - [x] Check live data asset references from built HTML rather than assuming `/data/*.json` paths are public.
    - [ ] Check a deployed build manifest with git SHA, data hash, build time, and route list.
    - [x] Define pass/fail outcomes that separate repo defects from external service blockers.
- [ ] Task: Define quality rubrics
    - [x] Create a visual contract covering route coverage, layout, mobile behaviour, copy, and chart correctness categories.
    - [x] Create a repository contract covering CI, tests, type safety, docs, metadata, licensing, deployment, and source integrity categories.
    - [ ] Convert those contracts into scored 1000-point and 100-point rubric outputs.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Parity And Scorecard Design' (Protocol in workflow.md)

## Phase 2: Automated Checks And Reports

- [ ] Task: Implement parity and scoring commands
    - [x] Add documented command evidence that verifies GitHub PR state, branch SHA parity, Hugging Face route status, and live data asset status.
    - [x] Keep GitHub release, Hugging Face, and Zenodo checks explicit in the external deployment workflow and checker.
    - [ ] Add score output that records component scores, failures, and external blockers.
    - [x] Ensure the current checks can run locally without mutating repo-tracked state.
- [ ] Task: Add tests for scoring behaviour
    - [ ] Test successful live-parity parsing with mocked responses.
    - [ ] Test open PR, stale data asset, route failure, and external-blocker cases.
    - [ ] Test that scores cannot pass when required evidence is missing.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Automated Checks And Reports' (Protocol in workflow.md)

## Phase 3: Score Loop And Final Quality Gate

- [ ] Task: Run the dashboard visual improvement loop
    - [x] Evaluate the current live and local dashboard against the visual contract.
    - [x] Fix the highest-impact visual defects found on `/gdp-stars` and `/pivot`.
    - [ ] Preserve evidence for each score iteration in a repo-local report.
- [ ] Task: Run the repository improvement loop
    - [x] Evaluate repository quality against the current contract.
    - [x] Fix CI/deployment gaps until latest workflows pass.
    - [x] Replace overbroad quality or security claims with precise contract-check wording.
    - [x] Record recommended future improvements that are outside the current delivered slice.
- [x] Task: Run full quality gates
    - [x] Run `pixi run format-check` and `pixi run mojo-format-check`.
    - [x] Run `pixi run lint`.
    - [x] Run `pixi run pytest --cov=src/data --cov-fail-under=85`.
    - [x] Run `pixi run typecheck`.
    - [x] Run `npm run lint`, `npm run format:check`, `npm run audit`, `OBSERVABLE_TELEMETRY_DISABLE=true npm run build`, and `npm run smoke:dist`.
    - [x] Run the external deployment check and live visual contract checks.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Score Loop And Final Quality Gate' (Protocol in workflow.md)
