# Research use

RepoSource Registry is suitable for exploratory and reproducible work on public GitHub repository metadata. It is a derived snapshot, so research claims must identify the exact snapshot used.

## Practical research questions

- How are repositories distributed across declared primary languages?
- Which topics or derived categories are represented in a snapshot?
- How are star counts distributed above the inclusion threshold?
- How complete are optional metadata fields such as descriptions and primary language?
- How does repository age vary across the published snapshot?
- How might GitHub Search semantics affect a repository-discovery sample?

## Snapshot discipline

Always record:

- dataset version;
- schema version;
- snapshot timestamp;
- canonical data file;
- SHA-256 hash when reproducibility requires integrity verification;
- analysis code and assumptions.

The registry is not a census of GitHub. The current snapshot uses the configured `stars >= 2,000` inclusion policy and reflects the collection process documented in `docs/methodology.md`.

## Interpretation limits

Stars are a popularity signal, not a quality, security, maintenance, or endorsement measure. GitHub metadata can be missing, stale, or changed upstream. Derived categories are RepoSource classifications, not GitHub-native labels. A result from the registry should not be described as the current live state of a repository without upstream verification.

## Reproducible workflow

`SNAPSHOT → VERIFY HASH → LOAD → ANALYZE → RECORD ASSUMPTIONS → PUBLISH RESULT`

For citation guidance see `docs/citation.md`; for a concrete loading path see `docs/quickstart.md`.
