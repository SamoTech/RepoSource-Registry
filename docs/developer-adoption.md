# Developer adoption

RepoSource Registry should grow through downstream utility, not promotional volume. This playbook defines the audiences, entry points, experiments, and evidence that matter.

## Priority audiences

| Audience | Problem | RepoSource value | Entry point | Genuine signal |
|---|---|---|---|---|
| Repository-discovery developers | Rebuilding repository search and normalization repeatedly | Reusable snapshot, schema, partitions, provenance | Dataset + quickstart | Local consumption or integration |
| Data engineers | Need structured repository metadata for ETL and indexing | JSON/CSV plus schema and integrity metadata | Canonical dataset | Pipeline or derived analysis |
| AI/RAG builders | Need repository metadata for retrieval and filtering | Structured records with upstream references | Dataset + AI/RAG guide | Retrieval prototype or issue feedback |
| Researchers | Need reproducible repository metadata | Snapshot identity, statistics, methodology | Research + citation docs | Reproducible analysis or citation |
| Tooling authors | Need focused repository sets | Language/category partitions | Catalog + examples | Downstream tool integration |

## Adoption loop

`DISCOVER → DOWNLOAD → FIRST ANALYSIS → BUILD → FEEDBACK → RETURN → CONTRIBUTE → CITE`

Stars are useful only as a secondary outcome of usefulness. Do not optimize for stars before there is evidence of use.

## First-use standard

A first-use experiment is successful when a real person outside the maintainer workflow does at least one of the following:

- downloads the dataset;
- runs an example;
- reports a concrete data-quality issue;
- creates a downstream analysis or integration;
- cites a snapshot;
- contributes documentation, tests, or examples.

Do not count impressions, generic reactions, or unsolicited page views as product adoption.

## Experiment template

For each experiment record:

1. Hypothesis
2. Target maintainer or researcher
3. Specific problem
4. Useful resource to send
5. Channel
6. Expected action
7. Evidence collected
8. What changed as a result

Keep experiments small and attributable. Do not mass-message unrelated accounts.
