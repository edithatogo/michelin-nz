#!/usr/bin/env python3
import json
from pathlib import Path

REQUIRED_ROOT_DOCS = [
    "conductor/requirements.md",
    "conductor/design.md",
    "conductor/contracts.md",
    "conductor/delivery-alignment.md",
]

REQUIRED_TRACK_FILES = ["spec.md", "plan.md", "metadata.json", "index.md"]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL {message}")


def main() -> None:
    for doc in REQUIRED_ROOT_DOCS:
        path = Path(doc)
        require(path.exists(), f"Missing required Conductor document: {doc}")
        text = path.read_text(encoding="utf-8")
        require(text.strip(), f"Empty required Conductor document: {doc}")

    requirements = Path("conductor/requirements.md").read_text(encoding="utf-8")
    for heading in ("## Must Have", "## Should Have", "## Could Have", "## Won't Have"):
        require(heading in requirements, f"Missing MoSCoW heading: {heading}")

    design = Path("conductor/design.md").read_text(encoding="utf-8")
    require("```mermaid" in design, "Design document must contain Mermaid diagrams")

    contracts = Path("conductor/contracts.md").read_text(encoding="utf-8")
    for heading in (
        "## Data Contract",
        "## Build And Code Quality Contract",
        "## Visual Contract",
        "## Deployment Contract",
        "## Track Completion Contract",
    ):
        require(heading in contracts, f"Missing contract section: {heading}")

    alignment = Path("conductor/delivery-alignment.md").read_text(encoding="utf-8")
    for heading in (
        "## Delivered And Aligned",
        "## Partially Delivered",
        "## Planned But Not Yet Delivered",
    ):
        require(heading in alignment, f"Missing delivery alignment section: {heading}")

    track_dirs = sorted(
        path
        for path in Path("conductor/tracks").iterdir()
        if path.is_dir() and not path.name.startswith(".")
    )
    require(track_dirs, "No active Conductor tracks found")
    for track_dir in track_dirs:
        for filename in REQUIRED_TRACK_FILES:
            require(
                (track_dir / filename).exists(), f"Missing {filename} for track {track_dir.name}"
            )
        metadata = json.loads((track_dir / "metadata.json").read_text(encoding="utf-8"))
        require(
            metadata.get("track_id") == track_dir.name, f"Track ID mismatch for {track_dir.name}"
        )
        require(
            metadata.get("status") in {"new", "in_progress", "blocked", "archived"},
            f"Bad status for {track_dir.name}",
        )
        plan = (track_dir / "plan.md").read_text(encoding="utf-8")
        require("Task:" in plan, f"Track plan has no tasks: {track_dir.name}")
        spec = (track_dir / "spec.md").read_text(encoding="utf-8")
        for heading in ("## Functional Requirements", "## Acceptance Criteria"):
            require(heading in spec, f"Missing {heading} in {track_dir.name}/spec.md")

    print("OK Conductor requirements, design, contracts, and delivery alignment are present.")


if __name__ == "__main__":
    main()
