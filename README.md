# RepoSource Registry

> An open, machine-readable GitHub repository discovery dataset for developers, researchers, AI/data applications, and open-source tooling.

[![Update Dataset](https://github.com/SamoTech/RepoSource-Registry/actions/workflows/update.yml/badge.svg)](https://github.com/SamoTech/RepoSource-Registry/actions/workflows/update.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

RepoSource Registry turns public GitHub repository search results into a documented, validated, reusable snapshot. It is designed to be downloaded, inspected, filtered, cited, and integrated into downstream tools without requiring every consumer to rebuild the same collection and normalization layer.

GitHub remains the upstream source of repository facts. RepoSource Registry is a secondary snapshot, not an official GitHub database, complete mirror, real-time feed, or quality ranking.

## Why RepoSource Registry?

GitHub Search is excellent for interactive, upstream discovery. Applications and research workflows often need something different: a reproducible dataset with a published schema, provenance, integrity metadata, focused partitions, and a stable snapshot that can be processed locally.

RepoSource packages that reusable discovery layer as open data. The goal is simple: make structured repository metadata easier to consume and easier to verify.

## Current dataset

The current published snapshot was generated on **2026-09-13T06:39:43Z** and contains repositories meeting the configured `stars >= 2,000` inclusion policy.

| Metric | Value |
|---|---:|
| Repositories | **33,180** |
| Primary languages | **213** |
| Derived categories | **7** |
| Minimum stars | **2,000** |
| Star range | **2,000–546,891** |
| Median stars | **3,879** |
| Archived repositories | **2,451** |
| Without primary language | **2,726** |
| Without description | **612** |
| Dataset version | **1.0.0** |
| Schema version | **1.1.0** |

Snapshot aggregates are maintained in [`data/statistics.json`](data/statistics.json); snapshot identity and integrity metadata are in [`data/manifest.json`](data/manifest.json).

## What you get

- **Canonical JSON dataset** with normalized repository records.
- **CSV export** for tabular workflows.
- **Language partitions** under `data/languages/`.
- **Category partitions** under `data/categories/`.
- **Statistics and change data** for snapshot analysis.
- **Manifest and synchronization metadata** for provenance and integrity checks.
- **JSON Schema** defining the repository record contract.
- **Machine-readable dataset metadata** and [`llms.txt`](llms.txt) for automated consumers.

The canonical published registry is [`data/repositories.json`](data/repositories.json). The other artifacts are supporting exports, indexes, metadata, or validation surfaces.

## What can you build with it?

RepoSource Registry is a data foundation, not a hosted application. The published data can support:

- repository discovery and recommendation tools;
- programming-language and topic-oriented research;
- open-source ecosystem analysis;
- developer catalogs and internal engineering tools;
- AI/RAG retrieval over structured repository metadata;
- popularity and distribution analysis;
- reproducible data-science experiments;
- downstream applications that need a local repository index.

See [`docs/use-cases.md`](docs/use-cases.md) for practical patterns and limitations.

## Quick start

```bash
git clone https://github.com/SamoTech/RepoSource-Registry.git
cd RepoSource-Registry
```

Read the canonical JSON dataset:

```python
import json

with open("data/repositories.json", encoding="utf-8") as f:
    dataset = json.load(f)

print("repositories:", dataset["repository_count"])

for repo in dataset["repositories"][:10]:
    print(repo["full_name"], repo["stars"], repo["html_url"])
```

Or query it directly with `jq`:

```bash
jq -r '.repositories[] | select(.stars >= 50000) | [.full_name, .stars, (.primary_language // "No declared language"), .html_url] | @tsv' data/repositories.json
```

For a five-minute integration path, see [`docs/quickstart.md`](docs/quickstart.md).

## Machine-readable resources

| Resource | Purpose |
|---|---|
| [`data/repositories.json`](data/repositories.json) | **Canonical dataset** |
| [`data/repositories.csv`](data/repositories.csv) | Tabular export |
| [`data/manifest.json`](data/manifest.json) | Snapshot identity, versions, provenance, hashes |
| [`data/statistics.json`](data/statistics.json) | Aggregate statistics |
| [`data/changes.json`](data/changes.json) | Snapshot change information |
| [`data/sync.json`](data/sync.json) | Synchronization audit metadata |
| [`schema/repository.schema.json`](schema/repository.schema.json) | Record schema |
| [`dataset.json`](dataset.json) | Dataset metadata and provenance |
| [`llms.txt`](llms.txt) | Compact agent orientation |

See [`docs/data-dictionary.md`](docs/data-dictionary.md) for field definitions and [`docs/catalog.md`](docs/catalog.md) for the available discovery partitions.

## AI and data-agent usage

Automated consumers should follow the same source discipline as human consumers:

1. Read [`dataset.json`](dataset.json) to understand scope.
2. Read [`data/manifest.json`](data/manifest.json) for snapshot identity and integrity.
3. Read [`schema/repository.schema.json`](schema/repository.schema.json) before interpreting records.
4. Consume [`data/repositories.json`](data/repositories.json), or a focused partition when appropriate.
5. Use [`data/statistics.json`](data/statistics.json) for aggregate claims.
6. Use each record's `html_url` as the upstream reference for an individual repository.
7. Treat mutable fields such as stars, topics, descriptions, and timestamps as snapshot values.
8. Distinguish GitHub-provided fields from RepoSource-derived fields such as `categories`, `popularity_band`, and `activity_status`.
9. Verify important current facts against GitHub before making consequential decisions.

RepoSource Registry does not claim endorsement, certification, indexing, or trust status from any AI company or other organization.

## Provenance, quality, and trust

The trust chain is:

**GitHub public API → search collection → partitioning/pagination → normalization → validation → deterministic classification → published snapshot → manifest/schema → downstream verification**

The collection process uses GitHub repository Search API results and a configured minimum-star threshold. Search ranges may be partitioned to operate within upstream search constraints. The published artifacts include deterministic ordering, duplicate and threshold validation, schema validation, SHA-256 hashes, synchronization metadata, and explicit dataset/schema versions.

GitHub is the primary source for current repository facts. RepoSource Registry is a structured secondary snapshot and should be treated accordingly.

See [`docs/methodology.md`](docs/methodology.md) for the collection and validation model.

## Freshness and limitations

The scheduled update workflow targets a **weekly** snapshot. This is not a real-time service and the registry is not a complete mirror of GitHub.

Key limitations:

- repositories below the configured star threshold are excluded;
- GitHub Search semantics and repository metadata can change between requests and snapshots;
- stars are a popularity signal, not a measure of quality, security, maintenance, or endorsement;
- language and topic metadata can be missing or inconsistent upstream;
- RepoSource categories are derived from a configured topic vocabulary and are not GitHub-native labels;
- archived repositories are included by the current configuration;
- important current facts should be verified against the upstream GitHub repository.

## Documentation

- [`docs/quickstart.md`](docs/quickstart.md) — use the dataset in five minutes.
- [`docs/use-cases.md`](docs/use-cases.md) — practical downstream applications.
- [`docs/catalog.md`](docs/catalog.md) — language and category discovery.
- [`docs/data-dictionary.md`](docs/data-dictionary.md) — field definitions.
- [`docs/methodology.md`](docs/methodology.md) — collection and validation methodology.
- [`docs/product-positioning.md`](docs/product-positioning.md) — current product definition.
- [`docs/roadmap.md`](docs/roadmap.md) — staged roadmap.
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — contributor workflow.
- [`SECURITY.md`](SECURITY.md) — security reporting.

## Roadmap

**Now** — keep the public dataset dependable, documented, validated, reproducible, and easy to consume.

**Next** — improve static discovery indexes, examples, integrations, contribution tooling, and research usability based on real usage.

**Later** — add historical snapshots, trend analysis, repository similarity, recommendations, and richer developer tooling where demand justifies the maintenance cost.

**Future** — consider a hosted discovery experience, visual analytics, research tooling, organization intelligence, and commercial integrations around the open data.

See [`docs/roadmap.md`](docs/roadmap.md) for the evidence-driven roadmap.

## Sponsoring

RepoSource Registry is intended to remain useful as open infrastructure regardless of whether it generates revenue. Sponsorship helps fund:

- dataset maintenance and CI;
- data-quality validation and regression testing;
- schema, documentation, and examples;
- public indexes and reproducibility work;
- historical preservation and research infrastructure;
- open developer integrations.

GitHub Sponsors is configured for `SamoTech` in [`.github/FUNDING.yml`](.github/FUNDING.yml). Actual sponsorship availability depends on the maintainer account's GitHub Sponsors eligibility and activation.

If the dataset is useful to your work, consider starring the repository so other developers can discover it. A star is a discovery signal, not the project's success criterion.

See [`docs/sponsoring.md`](docs/sponsoring.md) and [`docs/corporate-sponsorship.md`](docs/corporate-sponsorship.md).

## Commercial opportunities around the open data

The public dataset remains the foundation. RepoSource Registry does **not** depend on restricting access to the canonical dataset for monetization.

Potential commercial work includes:

- professional data integration and engineering;
- AI/RAG and developer-tool integration;
- custom repository research and derived datasets;
- ecosystem analysis and analytical reports;
- hosted discovery and visualization products;
- organization-specific research and integrations;
- technical implementation and support.

These are future or service opportunities, not claims of current revenue or demand. Commercial work should add expertise, customization, implementation, research, analytics, or hosted convenience without secretly altering the public registry.

See [`docs/services.md`](docs/services.md), [`docs/monetization.md`](docs/monetization.md), and [`docs/commercial-use.md`](docs/commercial-use.md).

## Citation

For reproducible work, cite RepoSource Registry together with the snapshot timestamp, dataset version, and canonical data file. For individual repositories, use the record's `html_url` as the upstream reference.

See [`docs/CONSUMING.md`](docs/CONSUMING.md) for consumption guidance. A `CITATION.cff` file is not currently published because verified citation metadata is not yet available in the repository.

## License

Project code and documentation are released under the [MIT License](LICENSE). Upstream repository metadata remains subject to GitHub's terms and the licenses applicable to individual repositories.

---

**RepoSource Registry** — open repository discovery data with explicit provenance, validation, schema, and machine-readable distribution.
