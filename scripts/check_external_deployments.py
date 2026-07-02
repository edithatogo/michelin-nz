#!/usr/bin/env python3
import json
import os
import sys
from urllib.parse import quote

import requests

GITHUB_REPO = os.environ.get("GITHUB_REPOSITORY", "edithatogo/michelin-nz")
HF_SPACE = os.environ.get("HF_SPACE", "edithatogo/michelin-nz")
EXPECTED_TITLE = "Michelin Star Per-Capita Dashboard"
HTTP_OK = 200
HTTP_BAD_REQUEST = 400
REQUIRE_GITHUB_RELEASE = os.environ.get("REQUIRE_GITHUB_RELEASE", "1") == "1"
REQUIRE_ZENODO = os.environ.get("REQUIRE_ZENODO", "1") == "1"


def get_json(url: str) -> tuple[int, object]:
    response = requests.get(url, timeout=20)
    try:
        payload: object = response.json()
    except json.JSONDecodeError:
        payload = {"text": response.text[:500]}
    return response.status_code, payload


def check_github() -> bool:
    print("Checking GitHub repository and latest release...")
    repo_url = f"https://api.github.com/repos/{GITHUB_REPO}"
    status, repo = get_json(repo_url)
    if status != HTTP_OK or not isinstance(repo, dict):
        print(f"FAIL GitHub repository API returned {status}")
        return False

    release_url = f"{repo_url}/releases/latest"
    release_status, release = get_json(release_url)
    if release_status != HTTP_OK or not isinstance(release, dict):
        if not REQUIRE_GITHUB_RELEASE:
            print(
                f"WARN GitHub latest release API returned {release_status}; release gate optional",
            )
            return True
        print(f"FAIL GitHub latest release API returned {release_status}")
        return False

    print(f"OK GitHub repository is public with latest release {release.get('tag_name')}")
    return True


def check_hugging_face() -> bool:
    print("Checking Hugging Face Space...")
    status, space = get_json(f"https://huggingface.co/api/spaces/{HF_SPACE}")
    if status != HTTP_OK or not isinstance(space, dict):
        print(f"FAIL Hugging Face Space API returned {status}")
        return False

    checks = {
        "private": space.get("private") is False,
        "sdk": space.get("sdk") == "static",
        "runtime": space.get("runtime", {}).get("stage") == "RUNNING",
        "host": bool(space.get("host")),
    }
    failed = [name for name, ok in checks.items() if not ok]
    if failed:
        print(f"FAIL Hugging Face checks failed: {', '.join(failed)}")
        return False

    host = str(space["host"])
    response = requests.get(host, timeout=20)
    if response.status_code != HTTP_OK or EXPECTED_TITLE not in response.text:
        print(f"FAIL Hugging Face host returned {response.status_code} or missing title")
        return False

    print(f"OK Hugging Face Space is public and running at {host}")
    return True


def check_zenodo() -> bool:
    print("Checking Zenodo record...")
    query = quote(f'"{GITHUB_REPO}" OR "{EXPECTED_TITLE}"')
    status, payload = get_json(f"https://zenodo.org/api/records?q={query}&size=10")
    if status != HTTP_OK or not isinstance(payload, dict):
        print(f"FAIL Zenodo records API returned {status}")
        return False

    hits = payload.get("hits", {}).get("hits", [])
    matching = [
        hit
        for hit in hits
        if isinstance(hit, dict)
        and EXPECTED_TITLE.lower() in json.dumps(hit.get("metadata", {}), sort_keys=True).lower()
    ]
    if not matching:
        message = "No Zenodo record found for this repository/title"
        return report_optional_zenodo_result(message)

    record = matching[0]
    doi = record.get("doi") or record.get("metadata", {}).get("doi")
    if not doi:
        return report_optional_zenodo_result("Zenodo record exists but has no DOI")

    doi_response = requests.get(f"https://doi.org/{doi}", timeout=20)
    if doi_response.status_code >= HTTP_BAD_REQUEST:
        print(f"FAIL DOI {doi} returned {doi_response.status_code}")
        return False

    print(f"OK Zenodo record found with DOI {doi}")
    return True


def report_optional_zenodo_result(message: str) -> bool:
    if not REQUIRE_ZENODO:
        print(f"WARN {message}; Zenodo gate optional")
        return True
    print(f"FAIL {message}")
    return False


def main() -> int:
    checks = [check_github(), check_hugging_face(), check_zenodo()]
    if all(checks):
        print("External deployment check passed.")
        return 0
    print("External deployment check failed.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
