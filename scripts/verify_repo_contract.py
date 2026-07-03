#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

import requests

HTTP_OK = 200

# Strict configuration checks
REQUIRED_FILES = [
    "pyproject.toml",
    "pixi.toml",
    "pixi.lock",
    ".zenodo.json",
    "CITATION.cff",
    "LICENSE",
    "README.md",
    "CONTRIBUTING.md",
    "conductor/spec.md",
    "conductor/requirements.md",
    "conductor/design.md",
    "conductor/contracts.md",
    "conductor/delivery-alignment.md",
    "src/data/metrics.mojo",
    "src/data/aggregate_country_ledger.csv",
    "src/data/official_michelin_guide_coverage.csv",
]


def check_files():
    print("Checking required file configurations...")
    for f in REQUIRED_FILES:
        if not Path(f).exists():
            print(f"FAIL Missing required file: {f}")
            return False
        print(f"OK Found {f}")
    return True


def check_citation_authorship():
    print("Checking CITATION.cff authorship registry...")
    with open("CITATION.cff", encoding="utf-8") as f:
        content = f.read()
    if "Mordaunt" not in content or "Dylan A" not in content:
        print("FAIL Primary author Dylan A Mordaunt missing in CITATION.cff")
        return False
    if "0000-0002-5364-1650" not in content:
        print("FAIL ORCID ID 0000-0002-5364-1650 missing in CITATION.cff")
        return False
    print("OK Citation author and ORCID checks passed.")
    return True


def run_format_checks():
    print("Running formatter validation...")
    for command in (["pixi", "run", "format-check"], ["pixi", "run", "mojo-format-check"]):
        res = subprocess.run(command, capture_output=True, check=False, text=True)
        if res.returncode != 0:
            print(f"FAIL Formatter command failed: {' '.join(command)}")
            print(res.stderr or res.stdout)
            return False
    print("OK Formatter validation passed.")
    return True


def run_tests():
    print("Running test suite coverage validation...")
    res = subprocess.run(
        ["pixi", "run", "pytest", "--cov=src/data", "--cov-fail-under=85"],
        capture_output=True,
        check=False,
        text=True,
    )
    if res.returncode != 0:
        print("FAIL Pytest execution failed:")
        print(res.stderr or res.stdout)
        return False
    print("OK All test suites passed successfully.")
    return True


def run_linters():
    print("Running Ruff linter checks...")
    res = subprocess.run(
        ["pixi", "run", "lint"],
        capture_output=True,
        check=False,
        text=True,
    )
    if res.returncode != 0:
        print("FAIL Ruff validation failed:")
        print(res.stdout)
        return False
    print("OK Ruff linting checks passed.")

    print("Running basedpyright typechecker checks...")
    res_pr = subprocess.run(
        ["pixi", "run", "typecheck"],
        capture_output=True,
        check=False,
        text=True,
    )
    if res_pr.returncode != 0:
        print("FAIL basedpyright typechecking failed:")
        print(res_pr.stderr or res_pr.stdout)
        return False
    print("OK basedpyright typechecking passed.")
    return True


def run_mojo_checks():
    print("Running Mojo toolchain checks...")
    for command in (["pixi", "run", "mojo-version"], ["pixi", "run", "mojo-build"]):
        res = subprocess.run(command, capture_output=True, check=False, text=True)
        if res.returncode != 0:
            print(f"FAIL Mojo command failed: {' '.join(command)}")
            print(res.stderr or res.stdout)
            return False
    print("OK Mojo toolchain checks passed.")
    return True


def run_conductor_contract_checks():
    print("Running Conductor contract checks...")
    res = subprocess.run(
        ["pixi", "run", "conductor-contracts"],
        capture_output=True,
        check=False,
        text=True,
    )
    if res.returncode != 0:
        print("FAIL Conductor contract checks failed:")
        print(res.stderr or res.stdout)
        return False
    print("OK Conductor contract checks passed.")
    return True


def run_official_coverage_checks():
    print("Running official Michelin coverage reconciliation checks...")
    res = subprocess.run(
        ["pixi", "run", "official-coverage"],
        capture_output=True,
        check=False,
        text=True,
    )
    if res.returncode != 0:
        print("FAIL Official coverage reconciliation failed:")
        print(res.stderr or res.stdout)
        return False
    print("OK Official coverage reconciliation passed.")
    return True


def verify_external_deployments():
    print("Validating Hugging Face Spaces status...")
    url = "https://huggingface.co/spaces/edithatogo/michelin-nz"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code != HTTP_OK:
            print(f"FAIL Hugging Face space returned status code: {r.status_code}")
            return False
        print("OK Hugging Face Space landing URL verified.")
        return True
    except Exception as e:
        print(f"FAIL Failed to connect to Hugging Face: {e}")
        return False


def main():
    print("==================================================")
    print("Starting Gastronomy Data Science Repo Contract Checks")
    print("==================================================")

    success = True
    success &= check_files()
    success &= check_citation_authorship()
    success &= run_format_checks()
    success &= run_tests()
    success &= run_linters()
    success &= run_mojo_checks()
    success &= run_conductor_contract_checks()
    success &= run_official_coverage_checks()
    success &= verify_external_deployments()

    print("==================================================")
    if success:
        print("Repository contract checks passed.")
        print("==================================================")
        sys.exit(0)
    else:
        print("Repository contract checks failed.")
        print("==================================================")
        sys.exit(1)


if __name__ == "__main__":
    main()
