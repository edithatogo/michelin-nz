# Implementation Plan: Experimental Mojo Data Processing Migration

## Phase 1: Mojo Toolchain And Metric Parity

- [x] Task: Add Mojo through Pixi
    - [x] Add the Modular channel to Pixi.
    - [x] Add the `mojo` dependency and lockfile.
    - [x] Replace deprecated `[project]` Pixi manifest syntax with `[workspace]`.
- [x] Task: Migrate derived metric calculation
    - [x] Add `src/data/metrics.mojo` for aggregate ratio calculations.
    - [x] Add a Python backend switch for `MICHELIN_METRICS_BACKEND=mojo`.
    - [x] Add tests proving Mojo and Python metric parity.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Mojo Toolchain And Metric Parity' (Protocol in workflow.md)

## Phase 2: CI And Contract Hardening

- [x] Task: Add CI Mojo verification
    - [x] Install Pixi in the verify workflow.
    - [x] Run `pixi run mojo-version`, `pixi run mojo-format-check`, and `pixi run mojo-build`.
    - [x] Ensure Python tests exercise the Mojo backend.
- [x] Task: Update repo contract checks
    - [x] Require `pixi.lock` and `src/data/metrics.mojo`.
    - [x] Run Mojo toolchain checks from the repo contract script.
    - [x] Remove inflated quality language from contract output.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: CI And Contract Hardening' (Protocol in workflow.md)

## Phase 3: Further Migration Review

- [ ] Task: Identify next safe Mojo migration targets
    - [ ] Review pure numeric transformations after data coverage expansion.
    - [ ] Compare Mojo output against Python/Polars for every candidate row.
    - [ ] Keep HTTP, source parsing, and Parquet output in Python until parity is proven.
- [ ] Task: Document migration boundaries
    - [ ] Update the tech stack with the current Mojo/Python split.
    - [ ] Document commands for Mojo formatting, build, and metrics checks.
    - [ ] Record any remaining blockers or performance tradeoffs in the track notes.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Further Migration Review' (Protocol in workflow.md)
