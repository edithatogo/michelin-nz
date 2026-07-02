# Track Specification: Live Deployment And Repository Quality Scorecard

## Overview

This track makes live quality auditable. It verifies that the Hugging Face dashboard reflects the
latest merged GitHub state and introduces scorecards that drive visual quality above 995/1000 and
repository quality to 100/100.

## Functional Requirements

- Verify that local `main`, `origin/main`, GitHub default branch, and live Hugging Face assets all
  represent the same intended code and data state.
- Verify that the remote repository has no open pull requests before claiming the live dashboard
  reflects all merged work.
- Extend deployment checks so active routes, expected 404 routes, static asset hashes, repo
  metadata, source pages, and generated data files are all verified.
- Add or verify a deployed build manifest containing git SHA, data hash, build time, and route list.
- Create a visual quality rubric scored out of 1000 with an acceptance threshold of greater than
  995/1000. Interpret the original `>995/100` request as `>995/1000`.
- Create a repository quality rubric scored out of 100 with an acceptance target of 100/100.
- Run an improvement loop: score, record defects, fix the highest-impact defects, rebuild, and
  rescore until both thresholds are met or a blocker is documented.
- Add a concise recommendations report covering additional improvements discovered during the
  score loop.
- Keep strict external gates such as Zenodo, GitHub releases, Hugging Face outages, and
  authentication separate from repo-local score claims.

## Non-Functional Requirements

- Score outputs must be deterministic enough for CI or manual reruns.
- Failures must distinguish repo-local defects from external gates such as Hugging Face outages,
  GitHub API limits, authentication, or pending remote deployment.
- Reports must not claim live parity without checking both route content and data assets.

## Acceptance Criteria

- A repeatable command reports live parity status, PR state, route status, data asset status, and
  deployment metadata.
- Dashboard visual score is greater than 995/1000 with evidence attached or checked into an
  appropriate repo-local report.
- Repository score is 100/100 with the scoring rubric documented.
- Any remaining external blocker is explicit and does not inflate the score.
- Existing format, lint, type, test, audit, build, smoke, and external deployment checks pass or
  report a documented external blocker.
- Repo contract output uses precise pass/fail wording and does not claim security coverage beyond
  the checks actually run.

## Out of Scope

- Implementing new data coverage or map features; those are covered by separate tracks.
- Publishing or pushing a deployment unless the implementation workflow explicitly reaches that
  step.
