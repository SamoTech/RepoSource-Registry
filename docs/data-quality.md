# Data quality

RepoSource Registry treats the published snapshot as a data product with an explicit validation contract.

## Current published quality summary

The snapshot generated on 2026-09-13T06:39:43Z reports:

- 33,180 records fetched;
- 33,180 records accepted;
- 0 records rejected;
- 0 duplicates removed;
- 2,451 archived repositories;
- 2,726 records without a primary language;
- 612 records without a description;
- minimum stars: 2,000;
- maximum stars: 546,891.

These values are from `data/statistics.json` and describe this snapshot only.

## Validation layers

The publishing workflow is expected to validate the generated artifacts before publication. The repository includes tests and publishing tooling for threshold, duplicate, schema, deterministic-output, metadata, and publication checks. See the implementation in `tests/` and `tools/` rather than assuming a validation property that is not implemented.

## Known quality limitations

Upstream GitHub metadata may be missing, stale, or inconsistent. Language values can be absent. Descriptions can be absent. Stars can change after collection. Derived categories are classification outputs. Search results are influenced by GitHub Search semantics and the configured collection policy.

## Consumer guidance

Treat required schema fields as contractual and optional fields as nullable where the schema permits. Preserve missingness instead of inventing values. For consequential current facts, follow the record's GitHub URL and verify upstream.

## Future quality work

Potential improvements include richer field-level quality summaries, historical quality comparison, and stronger downstream interoperability. These should be added only when supported by actual generated artifacts and tests.
