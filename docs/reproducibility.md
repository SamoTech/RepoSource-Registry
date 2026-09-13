# Reproducibility

A reproducible RepoSource analysis is defined by the data artifact, its identity, the transformation steps, and the assumptions.

## Analysis record

Use this compact record in research notes or downstream repositories:

```text
Dataset: RepoSource Registry
Dataset version: <version>
Schema version: <version>
Snapshot generated: <UTC timestamp>
Canonical artifact: data/repositories.json
SHA-256: <hash from data/manifest.json>
Filters: <analysis filters>
Transformations: <analysis transformations>
Code: <repository/path or release>
Limitations: <known limitations>
```

## Recommended workflow

1. Pin a published snapshot.
2. Verify the manifest and hash when integrity matters.
3. Validate records against `schema/repository.schema.json`.
4. Run analysis code without changing source records.
5. Export derived results separately from the canonical dataset.
6. Publish the snapshot identity alongside the result.

## What not to do

Do not overwrite the canonical dataset with analysis output. Do not silently mix multiple snapshots. Do not present snapshot values as live GitHub facts. Do not infer missing fields.

Historical comparisons are meaningful only when multiple actual snapshots are available. The project must not manufacture historical data to support a trend claim.
