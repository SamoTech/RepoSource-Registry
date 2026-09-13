# RepoSource Registry Methodology

## Scope

RepoSource Registry publishes a derived snapshot of public GitHub repository metadata. The current inclusion policy is `stars >= 2000`. It is not a complete GitHub mirror and does not claim real-time completeness.

## Collection

The existing collector uses GitHub's public repository Search API. It partitions star ranges when a query exceeds the safe Search result boundary, then paginates each eligible query.

GitHub Search results are mutable. `total_count` is treated as a snapshot rather than a guarantee that every later page remains full. A short page is handled as a pagination state, while responses marked `incomplete_results` are not silently accepted as complete.

Transport and rate-limit failures use the existing bounded retry behavior.

## Normalization

GitHub repository objects are normalized into the published repository schema. Topics are sorted and deduplicated. The registry adds deterministic classifications for categories, popularity bands, and activity status.

## Validation

Before publication, records are checked against JSON Schema, the minimum-star policy, repository identity uniqueness, deterministic ordering, URL shape, timestamps, statistics consistency, and manifest consistency.

The manifest records SHA-256 hashes for primary generated artifacts so consumers can identify the exact snapshot used.

## Freshness

The scheduled workflow currently runs weekly and can also be dispatched manually. `generated_at` and synchronization metadata identify each snapshot. Repository metadata can change between runs.

## Known limitations

- GitHub Search is a search service, not an immutable historical database.
- Star counts and repository metadata are mutable.
- GitHub topics and language declarations may be absent.
- Category membership is derived from a configured topic vocabulary.
- Archived repositories are currently included.
- The dataset is a secondary discovery source; individual GitHub repository pages remain the upstream reference.

## Reproducibility

Generation code, configuration, schema, tests, workflow, statistics, synchronization metadata, and integrity hashes are published in this repository.
