# RepoSource Registry

> An open, machine-readable GitHub repository discovery dataset for developers, researchers, AI/data applications, and open-source tooling.

[![Update Dataset](https://github.com/SamoTech/RepoSource-Registry/actions/workflows/update.yml/badge.svg)](https://github.com/SamoTech/RepoSource-Registry/actions/workflows/update.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

RepoSource Registry turns public GitHub repository search results into a documented, validated, reusable snapshot. It provides normalized repository metadata, a published schema, provenance, integrity metadata, focused partitions, statistics, and change information so downstream users can inspect, filter, cite, and integrate the data locally.

GitHub remains the upstream source of repository facts. RepoSource Registry is a secondary snapshot: it is not an official GitHub database, complete mirror, real-time feed, or quality ranking.

## Public discovery

The project includes a Vercel-ready public discovery interface that makes the open dataset easier to explore. **Public web interface: pending deployment.** The website is a presentation and discovery layer; GitHub remains the canonical project and data distribution.

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
- Public discovery UI source under `app/` for optional Vercel deployment.

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

The optional web layer uses Next.js App Router and server-rendered pages. It reads the existing canonical snapshot and statistics from the public GitHub distribution with revalidation caching; it does not create a database or regenerate the dataset during deployment.

The interface provides:

- repository search across the published snapshot;
- language, category, and minimum-star filters;
- repository detail views;
- direct upstream GitHub links;
- dataset, schema, manifest, and methodology navigation;
- generated robots and sitemap metadata when a deployment origin is available.

See [`docs/vercel.md`](docs/vercel.md) for architecture, deployment, caching, security, and limitations.

## Provenance, quality, and trust

**GitHub source → collection → partitioning/pagination → normalization → validation → deterministic classification → published snapshot → manifest/schema → downstream verification**

The scheduled collection process uses GitHub repository Search API results and the configured minimum-star threshold. Published artifacts include deterministic ordering, duplicate and threshold validation, schema validation, hashes, synchronization metadata, and explicit dataset/schema versions.

GitHub is the primary source for current repository facts. RepoSource Registry is a structured secondary snapshot.

See [`docs/methodology.md`](docs/methodology.md).

## Freshness and limitations

The scheduled update workflow targets a weekly snapshot. The registry is not real-time and does not represent every GitHub repository.

Repositories below the configured star threshold are excluded. GitHub Search semantics and repository metadata can change. Stars are a popularity signal, not a measure of quality, security, maintenance, or endorsement. Language/topic metadata can be missing or inconsistent upstream, and RepoSource categories are derived labels rather than GitHub-native labels.

## Documentation

- [`docs/quickstart.md`](docs/quickstart.md) — use the dataset in five minutes.
- [`docs/use-cases.md`](docs/use-cases.md) — downstream applications and limitations.
- [`docs/catalog.md`](docs/catalog.md) — language and category discovery.
- [`docs/data-dictionary.md`](docs/data-dictionary.md) — field definitions.
- [`docs/methodology.md`](docs/methodology.md) — collection and validation methodology.
- [`docs/product-positioning.md`](docs/product-positioning.md) — product definition.
- [`docs/roadmap.md`](docs/roadmap.md) — staged roadmap.
- [`docs/vercel.md`](docs/vercel.md) — public discovery deployment.
- [`docs/sponsoring.md`](docs/sponsoring.md) — community support.
- [`docs/corporate-sponsorship.md`](docs/corporate-sponsorship.md) — corporate support.
- [`docs/services.md`](docs/services.md) — professional services.
- [`docs/monetization.md`](docs/monetization.md) — open-data commercial boundaries.
- [`docs/commercial-use.md`](docs/commercial-use.md) — commercial-use guidance.
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — contribution workflow.
- [`SECURITY.md`](SECURITY.md) — security reporting.

## Sponsoring and commercial work

The public dataset remains open and useful independently of sponsorship or commercial services. Sponsorship supports maintenance, validation, CI, documentation, public indexes, research infrastructure, and developer tooling.

Commercial opportunities are intentionally around the open data: consulting, integration, custom data engineering, AI/RAG integration, custom research, analytics, hosted discovery experiences, reporting, and implementation support.

The project does not monetize access to the canonical dataset, request volume, or restricted data tiers. Revenue, if achieved, comes from sponsorship, expertise, implementation, customization, research, analytics, or hosted convenience around the open data.

See [`docs/sponsoring.md`](docs/sponsoring.md), [`docs/services.md`](docs/services.md), and [`docs/monetization.md`](docs/monetization.md).

## Roadmap

**Now:** dependable public data, validation, documentation, reproducibility, and discovery.

**Next:** stronger static indexes, examples, integrations, and contributor tooling based on real usage.

**Later:** historical snapshots, trends, similarity, recommendations, and richer research tooling where justified.

**Future:** hosted discovery, analytics, organization intelligence, and commercial integrations around the open dataset.

No roadmap stage depends on restricting access to the public dataset.

## Citation

For reproducible work, cite the project together with the snapshot timestamp, dataset version, and canonical data file. For individual repositories, use the record's `html_url` as the upstream reference.

A `CITATION.cff` file is not currently published because verified citation metadata is not yet available in the repository.

## License

Project code and documentation are released under the [MIT License](LICENSE). Upstream repository metadata remains subject to GitHub's terms and the licenses applicable to individual repositories.

---

**RepoSource Registry** — open repository discovery data with explicit provenance, validation, schema, and machine-readable distribution.
