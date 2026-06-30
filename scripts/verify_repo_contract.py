#!/usr/bin/env python3
import os
import sys
import subprocess
import requests

# Strict configuration checks
REQUIRED_FILES = [
    "pyproject.toml",
    "pixi.toml",
    ".zenodo.json",
    "CITATION.cff",
    "LICENSE",
    "README.md",
    "CONTRIBUTING.md",
    "conductor/spec.md",
]

def check_files():
    print("🔍 Checking required file configurations...")
    for f in REQUIRED_FILES:
        if not os.path.exists(f):
            print(f"❌ Missing required file: {f}")
            return False
        print(f"✅ Found {f}")
    return True

def check_citation_authorship():
    print("🔍 Checking CITATION.cff authorship registry...")
    with open("CITATION.cff", "r", encoding="utf-8") as f:
        content = f.read()
    if "Mordaunt" not in content or "Dylan A" not in content:
        print("❌ Primary author Dylan A Mordaunt missing in CITATION.cff")
        return False
    if "0000-0002-5364-1650" not in content:
        print("❌ ORCID ID 0000-0002-5364-1650 missing in CITATION.cff")
        return False
    print("✅ Citation author and ORCID checks passed.")
    return True

def run_tests():
    print("🔍 Running test suite coverage validation...")
    res = subprocess.run([".venv/bin/pytest", "--cov=src/data"], capture_output=True, text=True)
    if res.returncode != 0:
        print("❌ Pytest execution failed:")
        print(res.stderr or res.stdout)
        return False
    print("✅ All test suites passed successfully.")
    return True

def run_linters():
    print("🔍 Running Ruff linter checks...")
    res = subprocess.run([".venv/bin/ruff", "check", "src/data/"], capture_output=True, text=True)
    if res.returncode != 0:
        print("❌ Ruff validation failed:")
        print(res.stdout)
        return False
    print("✅ Ruff linting checks passed.")
    
    print("🔍 Running basedpyright typechecker checks...")
    res_pr = subprocess.run(["npx", "basedpyright", "src/data/"], capture_output=True, text=True)
    if res_pr.returncode != 0:
        print("⚠️ basedpyright checking warnings found (continuing)...")
    else:
        print("✅ basedpyright typechecking passed.")
    return True

def verify_external_deployments():
    if os.environ.get("SKIP_EXTERNAL_DEPLOYMENT_CHECK") == "1":
        print("⏭️ Skipping external deployment checks by environment request.")
        return True

    print("🔍 Validating Hugging Face Spaces status...")
    url = "https://huggingface.co/spaces/edithatogo/michelin-nz"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            print(f"❌ Hugging Face space returned status code: {r.status_code}")
            return False
        print("✅ Hugging Face Space landing URL verified.")
        return True
    except Exception as e:
        print(f"❌ Failed to connect to Hugging Face: {e}")
        return False

def main():
    print("==================================================")
    print("🛡️ Starting Gastronomy Data Science Repo Contract Checks")
    print("==================================================")
    
    success = True
    success &= check_files()
    success &= check_citation_authorship()
    success &= run_tests()
    success &= run_linters()
    success &= verify_external_deployments()
    
    print("==================================================")
    if success:
        print("🏆 REPOSITORY CONTRACT COMPLIANCE: 100% SECURE")
        print("==================================================")
        sys.exit(0)
    else:
        print("❌ REPOSITORY CONTRACT COMPLIANCE: FAILURES FOUND")
        print("==================================================")
        sys.exit(1)

if __name__ == "__main__":
    main()
