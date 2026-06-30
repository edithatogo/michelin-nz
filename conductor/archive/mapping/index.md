# Track: WebGL Mapping & Spatial Binning

## Overview
This track implements the geographic and network visualizations. It sets up:
1. Deck.gl maps to display WebGL-accelerated restaurant layers and hexbins.
2. Cosmograph (cosmos.gl) network visualizations showing chef and cuisine connections.
3. Integration of map interactions matching our dark-theme aesthetics.

## Tasks

### [x] Task: WebGL Mapping (Deck.gl)
*   **Action:** Install Deck.gl modules and write the map rendering code in `src/global-map.md`.
*   **Verification:** Run build and confirm the interactive global map compiles cleanly.
*   **Git Action:** Commit as `feat(map): implement global Deck.gl restaurant spatial visualization`.

### [x] Task: GPU Network Graphs (Cosmograph)
*   **Action:** Implement chef and cuisine network graphs in `src/network.md` powered by Cosmograph.
*   **Verification:** Confirm that nodes and links load correctly and layouts render cleanly.
*   **Git Action:** Commit as `feat(network): build GPU accelerated network graph using Cosmograph`.
