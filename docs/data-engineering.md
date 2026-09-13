# Data engineering

RepoSource Registry is designed for local and downstream data workflows without requiring a database or service endpoint.

## Source hierarchy

1. `data/repositories.json` — canonical repository records.
2. `data/repositories.csv` — tabular export.
3. `data/languages/` — language-focused partitions.
4. `data/categories/` — derived category partitions.
5. `data/manifest.json` — identity, provenance, and integrity metadata.
6. `schema/repository.schema.json` — record contract.

## ETL pattern

`DOWNLOAD → VERIFY → VALIDATE → TRANSFORM → INDEX → ANALYZE`

Keep transformations downstream. Do not edit the canonical published file in place.

## Large-file handling

The canonical JSON is substantially larger than the focused partitions. When a workflow needs only one language or category, prefer the corresponding partition. For repeated analytics, load once into a local analytical format rather than repeatedly parsing the full JSON.

## Interoperability

Use stable field names from the schema and preserve the snapshot identity alongside derived tables. If a field is missing, preserve null/missing semantics instead of substituting a guessed value.

## Integrity

When reproducibility matters, read `data/manifest.json` and verify the published SHA-256 hash before processing. Schema validation should be performed against the exact schema version associated with the snapshot.

## Operational boundary

The public dataset is directly consumable. No API, authentication, database, or paid access layer is required for normal use.
