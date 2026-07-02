# Track Specification: Experimental Mojo Data Processing Migration

## Overview

This track incrementally migrates suitable data-processing work from Python to Mojo. The first
safe migration target is deterministic derived-metric calculation. Python remains responsible for
HTTP access, Polars joins, Parquet output, and Observable asset generation until Mojo replacements
are proven with parity tests.

## Functional Requirements

- Manage Mojo through Pixi with the Modular package channel and a checked-in lockfile.
- Use Python 3.14 for all remaining Python orchestration while the migration is incomplete.
- Keep Python, Mojo, and analysis libraries on the latest compatible locked versions.
- Keep `src/data/metrics.mojo` as the first migrated module for stars-per-capita,
  GDP-per-capita, and stars-per-GDP calculations.
- Expose an experimental Python backend switch using `MICHELIN_METRICS_BACKEND=mojo`.
- Add parity tests proving Mojo-derived metrics match Python-derived metrics.
- Add CI checks for `mojo --version`, Mojo formatting/build, and Python tests that exercise the
  Mojo backend.
- Expand migration only where Mojo can be verified row-for-row against existing Python outputs.

## Non-Functional Requirements

- Do not remove Python/Polars orchestration until data coverage, source handling, and Parquet
  output have Mojo parity.
- Preserve deterministic builds on macOS and Linux.
- Any Mojo output used by Python must be parsed with strict field counts and explicit failures.

## Acceptance Criteria

- Pixi installs Mojo without deprecated manifest warnings.
- `pixi run mojo-build` and `pixi run mojo-metrics` pass.
- Python tests pass with Mojo parity coverage.
- CI installs Pixi and validates Mojo before running the data test suite.
- Data version hashes include Mojo source files that affect generated metrics.

## Out of Scope

- Rewriting the Observable frontend in Mojo.
- Removing Python before replacement code has complete parity tests.
- Migrating network access or Parquet writing before the aggregate data coverage track is stable.
