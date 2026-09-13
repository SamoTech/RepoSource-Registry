# RepoSource Registry

> An open, machine-readable GitHub repository discovery dataset for developers, researchers, AI/data applications, and open-source tooling.

[![Update Dataset](https://github.com/SamoTech/RepoSource-Registry/actions/workflows/update.yml/badge.svg)](https://github.com/SamoTech/RepoSource-Registry/actions/workflows/update.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

RepoSource Registry turns public GitHub repository search results into a documented, validated, reusable snapshot. It provides normalized repository metadata, a published schema, provenance, integrity metadata, focused partitions, statistics, and change information so downstream users can inspect, filter, cite, and integrate the data locally.

GitHub remains the upstream source of repository facts. RepoSource Registry is a secondary snapshot: it is not an official GitHub database, complete mirror, real-time feed, or quality ranking.

## Public discovery

The public discovery interface is deployed on Vercel:

**[Open RepoSource Registry Discovery →](https://repo-source-registry.vercel.app/)**

The web application is a presentation and discovery layer. GitHub remains the canonical project and public data distribution.

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

- Canonical JSON dataset with normalized repository records.
- CSV export for tabular workflows.
- Language and category partitions for focused consumption.
- Statistics and snapshot change information.
- Manifest, synchronization metadata, and SHA-256 integrity hashes.
- JSON Schema defining the repository record contract.
- Machine-readable dataset metadata and [`llms.txt`](llms.txt) for automated consumers.
- Public discovery UI source under `app/` for Vercel deployment.

The canonical registry is [`data/repositories.json`](data/repositories.json). Supporting artifacts do not replace it.

## Why it exists

GitHub Search is useful for interactive upstream discovery. A downstream application or research workflow may instead need a reproducible public snapshot that can be downloaded, tested, processed locally, cited, and compared over time.

RepoSource Registry provides that secondary data layer without claiming to replace GitHub.

## Quick start

```bash
git clone https://github.com/SamoTech/RepoSource-Registry.git
cd RepoSource-Registry
```

Read the canonical dataset:

```python
import json

with open("data/repositories.json", encoding="utf-8") as f:
    dataset = json.load(f)

print("repositories:", dataset["repository_count"])
for repo in dataset["repositories"][:10]:
    print(repo["full_name"], repo["stars"], repo["html_url"])
```

Or use `jq`:

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

See [`docs/data-dictionary.md`](docs/data-dictionary.md) for fields and [`docs/catalog.md`](docs/catalog.md) for discovery partitions.

## Developer, research, and integration paths

- [`docs/quickstart.md`](docs/quickstart.md) — consume the dataset quickly.
- [`docs/developer-adoption.md`](docs/developer-adoption.md) — downstream adoption experiments.
- [`docs/data-engineering.md`](docs/data-engineering.md) — ETL, validation, indexing, and interoperability.
- [`docs/ai-rag.md`](docs/ai-rag.md) — retrieval and RAG integration patterns.
- [`docs/analytics.md`](docs/analytics.md) — factual descriptive analysis patterns.
- [`docs/research.md`](docs/research.md) — research questions and limitations.
- [`docs/reproducibility.md`](docs/reproducibility.md) — snapshot-based reproducibility.
- [`docs/citation.md`](docs/citation.md) — citation guidance.
- [`docs/data-quality.md`](docs/data-quality.md) — validation and known limitations.
- [`docs/showcase.md`](docs/showcase.md) — future community showcase criteria.
- [`docs/community-growth.md`](docs/community-growth.md) — contribution and community growth model.
- [`docs/outreach.md`](docs/outreach.md) — maintainer-to-maintainer outreach guidance.
- [`docs/content-strategy.md`](docs/content-strategy.md) — technical content priorities.
- [`docs/feedback.md`](docs/feedback.md) — data, documentation, and UX feedback.
- [`docs/research-partnerships.md`](docs/research-partnerships.md) — collaboration model.
- [`docs/services.md`](docs/services.md) — professional services around the open data.
- [`docs/sponsoring.md`](docs/sponsoring.md) — sponsorship and independence.

## AI and data-agent usage

Automated consumers should:

1. Read [`dataset.json`](dataset.json) for scope and provenance.
2. Read [`data/manifest.json`](data/manifest.json) for snapshot identity and integrity.
3. Read [`schema/repository.schema.json`](schema/repository.schema.json) before interpreting records.
4. Consume the canonical dataset or a focused partition.
5. Use `data/statistics.json` for aggregate claims.
6. Treat mutable values as snapshot values.
7. Use each record's `html_url` as the upstream repository reference.
8. Verify consequential current facts against GitHub.

The project makes no claims of AI endorsement, certification, indexing, or official trust status.

## Vercel discovery architecture

The public web layer uses Next.js App Router and server-rendered pages. It reads the existing canonical snapshot and statistics from the public GitHub distribution with revalidation caching; it does not create a database or regenerate the dataset during deployment.

The interface provides repository search, language/category/topic/star filters, repository detail views, upstream GitHub links, and direct dataset/schema/manifest/methodology navigation.

See [`docs/vercel.md`](docs/vercel.md) for architecture, deployment, caching, security, and limitations.

## Provenance, quality, and trust

**GitHub source → collection → partitioning/pagination → normalization → validation → deterministic classification → published snapshot → manifest/schema → downstream verification**

The scheduled collection process uses GitHub repository Search API results and the configured minimum-star threshold. Published artifacts include deterministic ordering, duplicate and threshold validation, schema validation, hashes, synchronization metadata, and explicit dataset/schema versions.

GitHub is the primary source for current repository facts. RepoSource Registry is a structured secondary snapshot.

See [`docs/methodology.md`](docs/methodology.md) and [`docs/data-quality.md`](docs/data-quality.md).

## Freshness and limitations

The scheduled update workflow targets a weekly snapshot. The registry is not real-time and does not represent every GitHub repository.

Repositories below the configured star threshold are excluded. GitHub Search semantics and repository metadata can change. Stars are a popularity signal, not a measure of quality, security, maintenance, or endorsement. Language/topic metadata can be missing or inconsistent upstream, and RepoSource categories are derived labels rather than GitHub-native labels.

## Open-data commercial boundary

The canonical dataset remains public and directly consumable. There is no paid access tier and no monetization based on dataset request volume.

Commercial value is created around the open data through engineering, integration, custom research/data work, analytics, AI/RAG implementation, developer tooling, hosted custom experiences, consulting, and sponsorship. Sponsor identity does not influence inclusion, ranking, classification, or data integrity.

See [`docs/services.md`](docs/services.md), [`docs/sponsoring.md`](docs/sponsoring.md), and [`docs/monetization.md`](docs/monetization.md).

## Sponsorship

Sponsorship supports maintenance of the public infrastructure: dataset updates, validation, CI, documentation, research capability, and developer tooling. Sponsorship does not buy inclusion, ranking, classification, suppression, or influence over the registry.

See [`docs/sponsoring.md`](docs/sponsoring.md) or the repository's **Sponsor** button when GitHub Sponsors is available for the maintainer account.

## Citation

For reproducible work, cite the project together with the snapshot timestamp, dataset version, schema version when relevant, and canonical data file. A verified [`CITATION.cff`](CITATION.cff) is included for project citation metadata. For individual repositories, use the record's `html_url` as the upstream reference.

## License

Project code and documentation are released under the [MIT License](LICENSE). Upstream repository metadata remains subject to GitHub's terms and the licenses applicable to individual repositories.

---

**RepoSource Registry** — open repository discovery data with explicit provenance, validation, schema, and machine-readable distribution.
