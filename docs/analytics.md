# Analytics

The registry supports descriptive analytics over the published snapshot. Treat all results as snapshot-scoped unless live GitHub verification is performed.

## Examples

### Repositories by language

Use `data/statistics.json` for the published language counts or compute them directly from `data/repositories.json` when a custom filter is required.

### Repositories by category

Use the derived category counts in `data/statistics.json`. Categories are RepoSource classifications and should not be described as GitHub-native taxonomy.

### Star distribution

The current statistics include minimum, maximum, median, and star-band counts. These can support descriptive summaries but do not establish repository quality or popularity beyond the measured snapshot.

### Metadata completeness

The current snapshot records missing primary language and missing description counts. These are useful quality indicators and should be reported as missingness, not filled with inferred values.

### Repository age

`created_by_year` can support descriptive age analysis when the field exists in the generated statistics. Avoid treating repository age as an activity or quality measure.

## Reproducible analysis

Record dataset version, schema version, snapshot timestamp, filters, transformations, and hash when needed. Publish derived outputs separately from the canonical data.

## Interpretation rule

A chart can summarize the snapshot; it cannot turn a snapshot into live truth. For current repository facts, use the upstream GitHub URL stored in each record.
