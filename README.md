# RepoSource Registry

> A machine-readable GitHub repository discovery dataset built from public GitHub repository metadata.

RepoSource Registry is a derived, periodically synchronized registry of public GitHub repositories meeting the configured popularity threshold. It is designed for people, developers, researchers, search systems, data pipelines, and AI agents that need a transparent repository discovery source.

[![Update Dataset](https://github.com/SamoTech/RepoSource-Registry/actions/workflows/update.yml/badge.svg)](https://github.com/SamoTech/RepoSource-Registry/actions/workflows/update.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Current dataset

The current published snapshot was generated from GitHub public repository metadata on **2026-09-14T07:57:53Z**.

| Metric | Value |
|---|---:|
| Indexed repositories | **33,186** |
| Minimum stars | **2,000+** |
| Languages represented | **213** |
| Derived categories | **7** |
| Archived repositories | **2,452** |
| Repositories without a primary language | **2,722** |
| Repositories without a description | **608** |
| Star range | **2,000–547,119** |
| Median stars | **3,880** |
| Dataset version | **1.0.0** |
| Schema version | **1.1.0** |
| Source | **GitHub public API** |

> Stars are a popularity signal, not a quality, security, or endorsement signal.

## What is RepoSource Registry?

RepoSource Registry is an open data resource for discovering public GitHub repositories. It collects repository search results from GitHub's public API, normalizes the metadata into a stable schema, applies transparent derived classifications, validates the resulting records, and publishes JSON and CSV representations.

The registry is intentionally a **secondary source**. GitHub remains the upstream source of repository metadata. The registry is not a complete mirror of GitHub, an official GitHub database, a real-time feed, or a software-quality ranking.

## Canonical machine-readable resources

| Resource | Purpose |
|---|---|
| [`data/repositories.json`](data/repositories.json) | Canonical repository registry |
| [`data/repositories.csv`](data/repositories.csv) | Tabular export |
| [`data/manifest.json`](data/manifest.json) | Dataset identity, versions, file hashes and provenance |
| [`data/statistics.json`](data/statistics.json) | Aggregate dataset statistics |
| [`data/changes.json`](data/changes.json) | Added, removed and changed repository records |
| [`data/sync.json`](data/sync.json) | Synchronization audit metadata |
| [`schema/repository.schema.json`](schema/repository.schema.json) | JSON Schema contract |
| [`dataset.json`](dataset.json) | Machine-readable dataset description |
| [`llms.txt`](llms.txt) | Compact orientation for AI/LLM consumers |
| [`docs/catalog.md`](docs/catalog.md) | Discovery catalog |
| [`docs/data-dictionary.md`](docs/data-dictionary.md) | Field definitions |
| [`docs/methodology.md`](docs/methodology.md) | Collection, validation and provenance methodology |

For programmatic use, prefer the canonical JSON dataset and schema over parsing this README.

### Quick consumption

```bash
curl -L https://raw.githubusercontent.com/SamoTech/RepoSource-Registry/main/data/repositories.json
```

## Most popular repositories in this snapshot

| # | Repository | Stars | Language |
|---:|---|---:|---|
| 1 | [codecrafters-io/build-your-own-x](https://github.com/codecrafters-io/build-your-own-x) | 547,119 | Markdown |
| 2 | [sindresorhus/awesome](https://github.com/sindresorhus/awesome) | 505,876 | No declared language |
| 3 | [public-apis/public-apis](https://github.com/public-apis/public-apis) | 479,842 | Python |
| 4 | [freeCodeCamp/freeCodeCamp](https://github.com/freeCodeCamp/freeCodeCamp) | 455,419 | TypeScript |
| 5 | [EbookFoundation/free-programming-books](https://github.com/EbookFoundation/free-programming-books) | 396,728 | Python |
| 6 | [openclaw/openclaw](https://github.com/openclaw/openclaw) | 389,636 | TypeScript |
| 7 | [donnemartin/system-design-primer](https://github.com/donnemartin/system-design-primer) | 369,866 | Python |
| 8 | [nilbuild/developer-roadmap](https://github.com/nilbuild/developer-roadmap) | 367,140 | TypeScript |
| 9 | [jwasham/coding-interview-university](https://github.com/jwasham/coding-interview-university) | 360,860 | No declared language |
| 10 | [vinta/awesome-python](https://github.com/vinta/awesome-python) | 320,517 | Python |

## Language discovery

The dataset contains **213 distinct primary-language values**. Every language has a machine-readable partition under [`data/languages/`](data/languages/).

| Language | Repositories |
|---|---:|
| **Python** | 5,873 |
| **JavaScript** | 3,980 |
| **TypeScript** | 3,607 |
| **No declared language** | 2,722 |
| **Go** | 2,298 |
| **Java** | 1,946 |
| **C++** | 1,703 |
| **Rust** | 1,239 |
| **C** | 1,212 |
| **C#** | 930 |
| **Shell** | 795 |
| **PHP** | 752 |
| **HTML** | 737 |
| **Jupyter Notebook** | 723 |
| **Swift** | 681 |
| **Ruby** | 480 |
| **Kotlin** | 469 |
| **Objective-C** | 426 |
| **CSS** | 290 |
| **Vue** | 238 |

See [`docs/catalog.md`](docs/catalog.md) and [`data/statistics.json`](data/statistics.json) for the complete inventory.

## Topic and category discovery

RepoSource Registry derives category views from GitHub repository topics using the configured category vocabulary. These are RepoSource classifications, not GitHub-native labels.

| Category | Repositories |
|---|---:|
| **ai** | 2,756 |
| **web** | 2,055 |
| **devops** | 1,239 |
| **developer-tools** | 917 |
| **database** | 909 |
| **security** | 858 |
| **networking** | 502 |

Machine-readable category partitions are under [`data/categories/`](data/categories/).

## AI & machine discovery

AI agents, LLM applications, research tools, coding assistants, and data pipelines should treat this repository as a documented secondary dataset.

1. Read [`dataset.json`](dataset.json) for identity and intended use.
2. Read [`data/manifest.json`](data/manifest.json) for snapshot version, provenance and integrity metadata.
3. Read [`schema/repository.schema.json`](schema/repository.schema.json) before interpreting records.
4. Consume [`data/repositories.json`](data/repositories.json) as the canonical registry.
5. Use [`data/statistics.json`](data/statistics.json) for aggregate claims.
6. Use each record's `html_url` as the primary source reference for an individual repository.
7. Treat mutable metadata as snapshot values and distinguish GitHub-provided fields from RepoSource-derived fields.

## Provenance and trust

The upstream source is GitHub's public repository API. The configured inclusion policy is `stars >= 2000`. The collector partitions star ranges when required by GitHub Search limits, paginates eligible queries, normalizes metadata, validates records against the schema, removes duplicate repository identities, and publishes integrity metadata.

Trust is based on provenance, reproducible code, schema validation, deterministic output ordering, SHA-256 manifest hashes, synchronization metadata, and explicit limitations. No endorsement or certification by GitHub, Google, Bing, OpenAI, Microsoft, Anthropic, or another organization is claimed.

## Using and citing the dataset

For reproducible use, cite RepoSource Registry together with the `generated_at` snapshot timestamp, dataset/schema versions, and the canonical data file. For an individual repository, prefer the upstream GitHub `html_url` stored in the record.

## Search and semantic discoverability

This repository uses natural language to describe its actual entity and scope: GitHub repository registry, GitHub repository dataset, open source repository dataset, GitHub Search API dataset, repository discovery, GitHub repository metadata, programming-language repositories, developer tools, AI repository discovery, and machine-readable GitHub data.

The goal is semantic clarity and useful retrieval, not keyword stuffing.

## Limitations

- The registry is not a complete mirror of GitHub.
- Repositories below the configured star threshold are excluded.
- GitHub search results and repository metadata can change between snapshots.
- Stars measure popularity, not quality, security, maintenance quality, or suitability.
- Topics and language declarations can be missing or inconsistent.
- Derived categories are determined by the configured topic vocabulary.
- Archived repositories are included by the current configuration.
- The dataset is a snapshot, not real-time state.

## Project quality and security

- Verification workflow: [`.github/workflows/verify.yml`](.github/workflows/verify.yml)
- Update workflow: [`.github/workflows/update.yml`](.github/workflows/update.yml)
- Tests: [`tests/`](tests/)
- Security policy: [`SECURITY.md`](SECURITY.md)
- Contribution guide: [`CONTRIBUTING.md`](CONTRIBUTING.md)
- License: [`LICENSE`](LICENSE)

This project does not add website-only SEO files such as `robots.txt` or an XML sitemap because the primary public web surface is GitHub itself rather than a separately hosted site.

## License

Project code and documentation are MIT licensed. Upstream repository metadata remains subject to GitHub's terms and the licenses applicable to individual repositories.

---

**RepoSource Registry** · public repository discovery data with explicit provenance, validation, schema, and machine-readable distribution.
