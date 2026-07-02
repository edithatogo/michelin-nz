# Release Checklist

Use this checklist before publishing a release intended for Zenodo archival.

1. Confirm GitHub Actions are passing on `main`.
2. Confirm the Hugging Face Space is public and the static host loads.
3. Confirm `.zenodo.json` has current title, creators, version, publication date, license, and keywords.
4. Enable `edithatogo/michelin-nz` in Zenodo GitHub settings before publishing the GitHub release.
5. Publish a new GitHub release or tag after Zenodo integration is enabled.
6. Confirm Zenodo minted a DOI for the release.
7. Add the DOI to `CITATION.cff` and replace the README Zenodo note with a DOI badge/link.
8. Run the `External Deployment Check` workflow manually.
