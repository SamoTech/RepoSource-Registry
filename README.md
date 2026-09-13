# RepoSource Registry

> A machine-readable GitHub repository discovery dataset built from public GitHub repository metadata.

RepoSource Registry is a derived, periodically synchronized registry of public GitHub repositories meeting the configured popularity threshold. It is designed for people, developers, researchers, search systems, data pipelines, and AI agents that need a transparent repository discovery source.

[![Update Dataset](https://github.com/SamoTech/RepoSource-Registry/actions/workflows/update.yml/badge.svg)](https://github.com/SamoTech/RepoSource-Registry/actions/workflows/update.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Current dataset

The current published snapshot was generated from GitHub public repository metadata on **2026-09-13T06:39:43Z**.

| Metric | Value |
|---|---:|
| Indexed repositories | **33,180** |
| Minimum stars | **2,000+** |
| Languages represented | **213** |
| Derived categories | **7** |
| Archived repositories | **2,451** |
| Repositories without a primary language | **2,726** |
| Repositories without a description | **612** |
| Star range | **2,000–546,891** |
| Median stars | **3,879** |
| Dataset version | **1.0.0** |
| Schema version | **1.1.0** |
| Source | **GitHub public API** |

> Stars are a popularity signal, not a quality, security, or endorsement signal.

## What is RepoSource Registry?

RepoSource Registry is an open data resource for discovering public GitHub repositories. It collects repository search results from GitHub's public API, normalizes the metadata into a stable schema, applies transparent derived classifications, validates the resulting records, and publishes JSON and CSV representations.

The registry is intentionally a **secondary source**. GitHub remains the upstream source of repository metadata. The registry does not claim to be a complete mirror of GitHub, an official GitHub database, a real-time feed, or a software-quality ranking.

## Why this dataset exists

GitHub repository search is useful but inconvenient to consume as a reusable dataset. RepoSource Registry turns the discovery layer into explicit, inspectable artifacts that can be used for:

- GitHub repository discovery and research
- open source project exploration
- programming-language and topic-oriented discovery
- developer-tool and software catalog applications
- data analysis and ranking experiments
- AI/LLM retrieval and agent workflows
- reproducible snapshots of repository metadata

## Canonical machine-readable resources

| Resource | Purpose |
|---|---|
| [`data/repositories.json`](data/repositories.json) | Canonical repository registry |
| [`data/repositories.csv`](data/repositories.csv) | Tabular export |
| [`data/manifest.json`](data/manifest.json) | Dataset identity, versions, file hashes and provenance |
| [`data/statistics.json`](data/statistics.json) | Aggregate dataset statistics |
| [`data/changes.json`](data/changes.json) | Added, removed and changed repository records |
| [`data/sync.json`](data/sync.json) | Synchronization audit metadata |
| [`schema/repository.schema.json`](schema/repository.schema.json) | JSON Schema contract for repository records |
| [`dataset.json`](dataset.json) | Machine-readable dataset description |
| [`llms.txt`](llms.txt) | Compact orientation document for AI/LLM consumers |
| [`docs/catalog.md`](docs/catalog.md) | Human-readable discovery catalog |
| [`docs/data-dictionary.md`](docs/data-dictionary.md) | Field definitions |
| [`docs/methodology.md`](docs/methodology.md) | Collection, validation and provenance methodology |

For programmatic use, prefer the canonical JSON dataset and schema over parsing this README.

### Quick consumption

```bash
curl -L https://raw.githubusercontent.com/SamoTech/RepoSource-Registry/main/data/repositories.json
```

The canonical JSON payload contains dataset metadata plus a `repositories` array. Each record follows the published JSON Schema.

## Most popular repositories in this snapshot

Popularity is ordered by GitHub star count at synchronization time.

| # | Repository | Stars | Language |
|---:|---|---:|---|
| 1 | [codecrafters-io/build-your-own-x](https://github.com/codecrafters-io/build-your-own-x) | 546,891 | Markdown |
| 2 | [sindresorhus/awesome](https://github.com/sindresorhus/awesome) | 505,537 | No declared language |
| 3 | [public-apis/public-apis](https://github.com/public-apis/public-apis) | 479,508 | Python |
| 4 | [freeCodeCamp/freeCodeCamp](https://github.com/freeCodeCamp/freeCodeCamp) | 455,371 | TypeScript |
| 5 | [EbookFoundation/free-programming-books](https://github.com/EbookFoundation/free-programming-books) | 396,641 | Python |
| 6 | [openclaw/openclaw](https://github.com/openclaw/openclaw) | 389,546 | TypeScript |
| 7 | [donnemartin/system-design-primer](https://github.com/donnemartin/system-design-primer) | 369,659 | Python |
| 8 | [nilbuild/developer-roadmap](https://github.com/nilbuild/developer-roadmap) | 367,012 | TypeScript |
| 9 | [jwasham/coding-interview-university](https://github.com/jwasham/coding-interview-university) | 360,809 | No declared language |
| 10 | [vinta/awesome-python](https://github.com/vinta/awesome-python) | 320,304 | Python |

## Language discovery

The dataset contains **213 distinct primary-language values**. High-volume language partitions include:

| Language | Repositories |
|---|---:|
| Python | 5,871 |
| JavaScript | 3,980 |
| TypeScript | 3,607 |
| No declared language | 2,726 |
| Go | 2,298 |
| Java | 1,945 |
| C++ | 1,702 |
| Rust | 1,238 |
| C | 1,211 |
| C# | 930 |
| Shell | 793 |
| PHP | 752 |
| HTML | 737 |
| Jupyter Notebook | 722 |
| Swift | 680 |

Every language has a dedicated machine-readable partition under [`data/languages/`](data/languages/). The complete language inventory and counts are available in [`data/statistics.json`](data/statistics.json) and [`docs/catalog.md`](docs/catalog.md).

## Topic and category discovery

RepoSource Registry derives seven category views from GitHub repository topics using the configured category vocabulary:

| Category | Repositories |
|---|---:|
| AI | 2,752 |
| Web | 2,054 |
| DevOps | 1,238 |
| Developer Tools | 915 |
| Database | 909 |
| Security | 857 |
| Networking | 501 |

These categories are **RepoSource-derived classifications**, not GitHub-native labels. Each category has a machine-readable partition under [`data/categories/`](data/categories/).

## AI & machine discovery

AI agents, LLM applications, research tools, coding assistants, and automated data pipelines should treat RepoSource Registry as a documented secondary dataset rather than as an authority claim.

Recommended consumption order:

1. Read [`dataset.json`](dataset.json) for dataset identity and intended use.
2. Read [`data/manifest.json`](data/manifest.json) for the current snapshot, version and file integrity metadata.
3. Read [`schema/repository.schema.json`](schema/repository.schema.json) before interpreting records.
4. Consume [`data/repositories.json`](data/repositories.json) as the canonical registry.
5. Use [`data/statistics.json`](data/statistics.json) for aggregate claims.
6. Use the repository's `html_url` as the primary source reference when citing an individual project.
7. Treat `indexed_at`, `source_updated_at`, stars and other mutable metadata as snapshot values, not permanent facts.
8. Preserve the distinction between GitHub-provided fields and RepoSource-derived fields such as `categories`, `popularity_band`, and `activity_status`.

[`llms.txt`](llms.txt) provides a compact machine-oriented orientation without replacing the canonical data or schema.

## Provenance and methodology

The upstream source is GitHub's public repository API, specifically repository Search API results. The configured inclusion policy is `stars >= 2000`. The collector partitions star ranges when required by GitHub's search limits, paginates each eligible query, normalizes repository metadata, removes duplicate repository identities, applies deterministic classifications, validates every record against the schema, and publishes integrity metadata.

The dataset is regenerated by the existing scheduled GitHub Actions workflow. The current schedule is weekly; repository metadata can change between snapshots.

GitHub Search pagination is treated as a mutable search result set rather than as an immutable database cursor. The collector does not treat `total_count` as a guarantee that every future page will remain full. Search responses marked `incomplete_results` are treated as incomplete rather than silently published.

## Trust model

The registry earns trust through:

- explicit upstream provenance
- reproducible generation code
- a versioned JSON Schema
- duplicate and threshold validation
- deterministic output ordering
- SHA-256 hashes in the manifest
- synchronization audit metadata
- documented limitations
- transparent distinction between source fields and derived classifications

No claim is made that Google, Bing, OpenAI, Microsoft, Anthropic, GitHub, or another organization endorses or certifies this dataset.

## Using and citing the dataset

For a reproducible citation, reference:

- **Dataset:** RepoSource Registry
- **Snapshot:** the `generated_at` value in `data/manifest.json`
- **Version:** `dataset_version` and `schema_version`
- **Canonical dataset:** [`data/repositories.json`](data/repositories.json)
- **Upstream provenance:** GitHub public repository metadata
- **Individual repository source:** the record's `html_url`

When reporting statistics, cite the snapshot date because stars, descriptions, topics, activity, and other repository metadata are mutable.

## Search and semantic discoverability

The repository is intentionally written so that humans and retrieval systems can identify its entity, scope, source, schema, freshness, limitations, and canonical files without relying on keyword stuffing.

Relevant search concepts include GitHub repository registry, GitHub repository dataset, open source repository dataset, GitHub Search API dataset, repository discovery, GitHub repository metadata, programming-language repositories, developer tools, AI repository discovery, and machine-readable GitHub data.

These concepts describe the actual resource and are used only where they improve clarity.

## Web crawler considerations

This project is currently a GitHub repository rather than a separately hosted website. Website-only mechanisms such as `robots.txt`, XML sitemaps, HTML canonical tags, and Open Graph pages are therefore not added as if they controlled GitHub's rendering or indexing.

GitHub's repository page and README are the primary human-facing web surface; the JSON, schema, catalog, and machine metadata provide the crawlable data layer.

## Limitations

- The registry is not a complete mirror of GitHub.
- The minimum-star policy excludes repositories below the configured threshold.
- Search results and repository metadata can change between synchronization runs.
- Star counts measure popularity, not quality, security, maintenance quality, or suitability.
- GitHub topics and language declarations can be missing or inconsistent.
- Derived categories are determined by the configured topic vocabulary.
- Archived repositories are included by the current configuration.
- The dataset is a snapshot and should not be treated as real-time state.

## Project quality and security

- Tests: [`tests/`](tests/)
- CI verification: [`.github/workflows/verify.yml`](.github/workflows/verify.yml)
- Scheduled update workflow: [`.github/workflows/update.yml`](.github/workflows/update.yml)
- Security policy: [`SECURITY.md`](SECURITY.md)
- Contribution guide: [`CONTRIBUTING.md`](CONTRIBUTING.md)
- License: [`LICENSE`](LICENSE)

Do not place secrets, access tokens, private repository metadata, or internal runner information in generated discovery artifacts.

## License

Project code and documentation are released under the MIT License. Upstream repository metadata remains subject to GitHub's terms and the licenses applicable to the individual repositories.

---

**RepoSource Registry** · public repository discovery data with explicit provenance, validation, schema, and machine-readable distribution.
