# Track: Deep Linking, Community Review CMS & Automation

## Overview
This track implements external integrations and automation routines. It sets up:
1. Deep links to mapping options (Google, Apple, OpenStreetMap) and official booking guides for each restaurant.
2. Flat-file blog/review system (`src/data/reviews/`) where external bloggers submit reviews via PRs.
3. Scheduled GitHub Action workflows to fetch daily data updates and verify deployment.

## Tasks

### [x] Task: External Map Deep Links
*   **Action:** Write interactive links on the NZ restaurant lists to route coordinates to Google Maps, Apple Maps, and OpenStreetMap.
*   **Verification:** Confirm that clicked URLs match the target coordinates patterns.
*   **Git Action:** Commit as `feat(ux): add external maps deep linking support`.

### [x] Task: Community Review CMS
*   **Action:** Create a Markdown directory parser (`src/data/reviews/`) matching restaurant keys so bloggers can check in reviews via PR.
*   **Verification:** Ensure compiled pages display community reviews when local files match the restaurant ID.
*   **Git Action:** Commit as `feat(cms): implement PR-driven community review database`.

### [x] Task: CI/CD & Automation Workflow
*   **Action:** Build `.github/workflows/data_sync.yml` to trigger daily scraper builds, compile, and deploy to Hugging Face Spaces.
*   **Verification:** Ensure YAML actions parse cleanly.
*   **Git Action:** Commit as `ci: add scheduled build sync automation`.
