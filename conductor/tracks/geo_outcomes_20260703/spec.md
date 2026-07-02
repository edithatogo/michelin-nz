# Track Specification: Global Choropleth And New Zealand Location-Safe Visualisation

## Overview

This track restores geographic analysis without reverting to restricted restaurant-level
publication. It adds a global choropleth over aggregate country metrics and a New Zealand
location visualisation that fails closed unless exact location data is independently documented
as redistributable.

## Functional Requirements

- Add a `/global-map` route linked from navigation.
- Visualise country-level metrics as a global choropleth, including stars per 100k, stars per
  $10B GDP, aggregate restaurant count, aggregate star count, and coverage status.
- Show missing, withheld, and unverified countries as explicit map states instead of omitting them.
- Use a license-compatible world boundary source and document it in the sources page.
- Add a New Zealand location visualisation on `/nz` or a linked `/nz-locations` route.
- Default New Zealand location mode is city/region aggregate or centroid-level display, not
  public restaurant points, names, addresses, or guide-derived coordinates.
- If exact New Zealand point data is proposed, implementation must first update product and
  source documentation with documented redistribution rights; otherwise the UI must show an
  explicit "no verified public point dataset" state.
- Evaluate additional visual outcomes and implement only aggregate-safe ones, such as regional
  coverage completeness, density bands, GDP/population quadrant views, and New Zealand peer
  benchmarks, restaurants per million people, stars per restaurant, and guide coverage type.

## Non-Functional Requirements

- Maps must remain readable on mobile and desktop.
- Map legends, colour scales, and empty states must be accessible and explain missing data.
- No stale route from older map/network work may ship unless backed by current data and tests.

## Acceptance Criteria

- `/global-map` renders a nonblank choropleth from the refreshed aggregate country metrics.
- The map legend distinguishes supported, missing, withheld, and unverified coverage.
- The New Zealand visualisation either renders documented aggregate-safe locations or clearly
  reports that exact public point data is not available.
- No public route exposes restaurant names, reviews, addresses, booking links, or guide-derived
  row-level coordinates.
- Static smoke tests cover the new route and removed-route expectations.
- Full local build and lint gates pass.

## Out of Scope

- Network graphs over restaurant relationships.
- Scraping or redistributing proprietary Michelin row-level records.
- Live deployment scoring; that is covered by the live quality score track.
