# RepoSource Registry

> An open, machine-readable GitHub repository discovery dataset for developers, researchers, AI applications, and open-source tooling.

[![Update Dataset](https://github.com/SamoTech/RepoSource-Registry/actions/workflows/update.yml/badge.svg)](https://github.com/SamoTech/RepoSource-Registry/actions/workflows/update.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

RepoSource Registry turns public GitHub repository search results into a documented, validated, reusable dataset. The current snapshot contains **33,180 public repositories** meeting the configured `stars >= 2,000` inclusion policy.

It is a **secondary data source**: GitHub remains the upstream source of repository facts. RepoSource does not claim to be a complete GitHub mirror, a real-time feed, an official GitHub database, or a quality ranking.

## Why this exists

GitHub Search is excellent for interactive discovery, but applications that repeatedly need repository metadata often have to implement their own search, pagination, normalization, filtering, and validation. RepoSource Registry packages that discovery layer as an inspectable snapshot with a published schema, provenance, integrity metadata, and focused indexes.

The result is useful when you want to **discover, analyze, filter, cite, or feed GitHub repository metadata into another tool without rebuilding the collection layer yourself**.

## Current dataset

The published snapshot was generated on **2026-09-13T06:39:43Z**.

| Metric | Value |
|---|---:|
| Repositories | **33,180** |
| Owners | **See `data/statistics.json`** |
| Primary languages | **213** |
| Derived categories | **7** |
| Minimum stars | **2,000** |
| Star range | **2,000–546,891** |
| Median stars | **3,879** |
| Archived repositories | **2,451** |
| Without a description | **612** |
| Without a primary language | **2,726** |
| Dataset version | **1.0.0** |
| Schema version | **1.1.0** |
| Source | **GitHub public API** |

Aggregate values that can change with each snapshot are maintained in [`data/statistics.json`](data/statistics.json) and identified by [`data/manifest.json`](data/manifest.json). The README intentionally avoids duplicating every statistic.

## What you get

- **Canonical JSON registry** containing normalized repository records.
- **CSV export** for spreadsheet and tabular workflows.
- **Language partitions** under `data/languages/` for focused consumption.
- **Category partitions** under `data/categories/` for RepoSource-derived discovery views.
- **Statistics** for aggregate analysis.
- **Change data** showing added, removed, and changed records between snapshots.
- **Manifest and synchronization metadata** for provenance and integrity verification.
- **JSON Schema** defining the repository record contract.
- **Machine-readable dataset metadata** and a compact `llms.txt` orientation file.

## What can you build with it?

RepoSource Registry is intentionally a data foundation rather than a hosted application. It can support:

- repository discovery and recommendation tools;
- programming-language and topic-oriented research;
- open-source ecosystem analysis;
- developer catalogs and internal engineering tools;
- AI/RAG retrieval over structured repository metadata;
- repository popularity and distribution analysis;
- data-science experiments and reproducible snapshots;
- downstream applications that need a local, queryable repository index.

See [`docs/use-cases.md`](docs/use-cases.md) for concrete patterns and limitations.

## Quick start

Clone the repository and query the canonical JSON locally:

```bash
git clone https://github.com/SamoTech/RepoSource-Registry.git
cd RepoSource-Registry
```

```python
import json

with open("data/repositories.json", encoding="utf-8") as f:
    dataset = json.load(f)

print("repositories:", dataset["repository_count"])

for repo in dataset["repositories"][:10]:
    print(repo["full_name"], repo["stars"], repo["html_url"])
```

For a five-minute integration guide, see [`docs/quickstart.md`](docs/quickstart.md).

### Query without Python

```bash
jq -r '.repositories[] | select(.stars >= 50000) | [.full_name, .stars, (.primary_language // "No declared language"), .html_url] | @tsv' data/repositories.json
```

For a smaller language-specific subset, use the generated partitions under [`data/languages/`](data/languages/).

## Canonical resources

| Resource | Role |
|---|---|
| [`data/repositories.json`](data/repositories.json) | **Canonical dataset** |
| [`data/repositories.csv`](data/repositories.csv) | Tabular export |
| [`data/manifest.json`](data/manifest.json) | Snapshot identity, versions, provenance, hashes |
| [`data/statistics.json`](data/statistics.json) | Aggregate statistics |
| [`data/changes.json`](data/changes.json) | Snapshot change information |
| [`data/sync.json`](data/sync.json) | Synchronization audit metadata |
| [`schema/repository.schema.json`](schema/repository.schema.json) | Record contract |
| [`dataset.json`](dataset.json) | Dataset metadata and provenance |
| [`llms.txt`](llms.txt) | Compact AI/LLM orientation |

When building an integration, treat `data/repositories.json` as the authoritative published registry and use the schema and manifest to interpret and verify it.

## Data model

The repository record schema currently includes identity and source metadata such as:

`repository_id`, `full_name`, `owner`, `name`, `html_url`, `api_url`, `description`, `stars`, `forks`, `watchers`, `open_issues`, `primary_language`, `topics`, `license`, `default_branch`, `archived`, `fork`, `created_at`, `updated_at`, `pushed_at`, `indexed_at`, `source_updated_at`, `source`, `dataset_version`, `schema_version`, `categories`, `popularity_band`, and `activity_status`.

See [`schema/repository.schema.json`](schema/repository.schema.json) and [`docs/data-dictionary.md`](docs/data-dictionary.md) for the contract and field meanings. Do not infer facts for fields that are null or absent.

## AI & data-agent usage

RepoSource Registry is designed to be legible to automated consumers without making authority claims.

Recommended workflow:

1. Read [`dataset.json`](dataset.json) to identify the dataset and its scope.
2. Read [`data/manifest.json`](data/manifest.json) for snapshot identity and integrity metadata.
3. Read [`schema/repository.schema.json`](schema/repository.schema.json) before interpreting records.
4. Consume [`data/repositories.json`](data/repositories.json), or a focused generated partition when appropriate.
5. Use [`data/statistics.json`](data/statistics.json) for aggregate claims.
6. Use a record's `html_url` as the upstream reference for an individual repository.
7. Treat stars, descriptions, topics, activity timestamps, and other mutable fields as snapshot values.
8. Distinguish GitHub-provided fields from RepoSource-derived fields such as `categories`, `popularity_band`, and `activity_status`.
9. Verify important current facts against GitHub before making consequential decisions.

[`llms.txt`](llms.txt) provides a compact orientation for agents that need the project structure before loading the larger dataset.

No claim is made that Google, Bing, OpenAI, Microsoft, Anthropic, GitHub, or another organization endorses or certifies RepoSource Registry.

## Provenance and trust model

The trust chain is:

**GitHub public API → search collection → star-range partitioning → pagination → normalization → validation → deterministic classification → published snapshot → manifest/schema → downstream verification**

The collector uses GitHub repository Search API results and a configured minimum-star threshold. Search ranges may be partitioned to work within search constraints. Pagination is implemented against the actual responses rather than assuming that `total_count` guarantees future pages will remain full. Responses marked `incomplete_results` are not silently published as complete results.

The published artifacts include deterministic ordering, duplicate/threshold validation, schema validation, SHA-256 file hashes, synchronization metadata, and explicit dataset/schema versions.

See [`docs/methodology.md`](docs/methodology.md) for the detailed collection and validation model.

## Freshness and limitations

The scheduled update workflow currently targets a **weekly** snapshot. This is not a real-time service.

Important limitations:

- The registry is not a complete mirror of GitHub.
- Repositories below the configured star threshold are excluded.
- GitHub Search and repository metadata can change between requests and between snapshots.
- Stars are a popularity signal, not a measure of quality, security, maintenance, or endorsement.
- Language and topic metadata may be missing or inconsistent upstream.
- RepoSource categories are derived from a configured topic vocabulary and are not GitHub-native labels.
- Archived repositories are included by the current configuration.
- The registry is a secondary source; GitHub is the primary source for current repository facts.

## Developer documentation

- [`docs/quickstart.md`](docs/quickstart.md) — use the dataset in five minutes.
- [`docs/use-cases.md`](docs/use-cases.md) — practical downstream applications.
- [`docs/catalog.md`](docs/catalog.md) — language and category discovery.
- [`docs/data-dictionary.md`](docs/data-dictionary.md) — field definitions.
- [`docs/methodology.md`](docs/methodology.md) — collection and validation methodology.
- [`docs/product-positioning.md`](docs/product-positioning.md) — current product definition.
- [`docs/roadmap.md`](docs/roadmap.md) — staged product roadmap.
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — contributor workflow.
- [`SECURITY.md`](SECURITY.md) — security reporting.

## Adoption roadmap

**Now** — keep the public dataset dependable, documented, validated, and easy to consume.

**Next** — grow real downstream usage through examples, integrations, research references, and data-quality contributions.

**Later** — add developer tooling such as a CLI/SDK or static query helpers only where repeated usage demonstrates the need.

**Future** — consider historical intelligence, trends, similarity, alerts, APIs, and enterprise integrations when there is evidence of recurring demand.

The roadmap is deliberately evidence-driven. See [`docs/roadmap.md`](docs/roadmap.md) and [`docs/growth-strategy.md`](docs/growth-strategy.md).

## Sponsoring and commercial use

RepoSource Registry is intended to remain useful as open infrastructure regardless of whether it generates revenue.

Sponsorship can fund:

- dataset maintenance and CI infrastructure;
- data-quality and regression testing;
- schema and documentation work;
- historical snapshots and change analysis;
- future public APIs and integrations.

GitHub Sponsors is configured in [`.github/FUNDING.yml`](.github/FUNDING.yml) for `SamoTech`; actual sponsorship availability depends on the maintainer account's GitHub Sponsors status.

Future commercial services may include higher-volume API access, historical feeds, advanced analytics, alerts, enterprise exports, support, or custom integrations. These are **potential products, not current revenue claims**. Sponsorship or payment must never buy repository ranking, inclusion, suppression, or classification changes.

See [`docs/sponsoring.md`](docs/sponsoring.md), [`docs/corporate-sponsorship.md`](docs/corporate-sponsorship.md), and [`docs/monetization.md`](docs/monetization.md).

## How to cite

For reproducible work, cite the project together with the snapshot timestamp, dataset version, and canonical data file. For individual repositories, use the record's `html_url` as the upstream reference.

See [`docs/CONSUMING.md`](docs/CONSUMING.md) for consumption guidance.

## Quality and security

- Automated test suite under [`tests/`](tests/).
- CI verification workflow: [`.github/workflows/verify.yml`](.github/workflows/verify.yml).
- Scheduled update workflow: [`.github/workflows/update.yml`](.github/workflows/update.yml).
- Versioned JSON Schema and generated validation artifacts.
- Dataset manifest with SHA-256 hashes.
- Documented provenance and limitations.
- Open-source contribution and security policies.

Never place tokens, credentials, private repository data, or runner secrets in the generated dataset or documentation.

## License

Project code and documentation are released under the [MIT License](LICENSE). Upstream repository metadata remains subject to GitHub's terms and the licenses applicable to individual repositories.

---

**RepoSource Registry** — open repository discovery data with explicit provenance, validation, schema, and machine-readable distribution.
