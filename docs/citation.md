# Citation and reproducibility

RepoSource Registry is a snapshot dataset. Cite the project and identify the exact snapshot used so another reader can reproduce the analysis.

## Minimum citation record

Include:

- RepoSource Registry;
- dataset version;
- schema version when relevant;
- snapshot timestamp;
- canonical data file (`data/repositories.json`) or the exact focused partition;
- dataset SHA-256 hash when integrity verification matters;
- access date for published work.

For an individual repository, use the record's `html_url` as the upstream GitHub reference and verify current facts directly on GitHub.

## Example citation text

> RepoSource Registry, dataset version 1.0.0, snapshot generated 2026-09-13T06:39:43Z, `data/repositories.json`, schema 1.1.0. Accessed from the public RepoSource Registry repository.

This example describes the currently published snapshot; update it when citing a later release.

## Reproducibility checklist

1. Preserve the dataset version and snapshot timestamp.
2. Preserve the dataset hash from `data/manifest.json` when required.
3. Record the schema version.
4. Preserve analysis code and dependency versions where relevant.
5. State filters, exclusions, and transformations.
6. Distinguish registry values from live GitHub values.

No DOI, publisher, journal, or institutional affiliation is claimed by this project unless such metadata is added from a verified source.
