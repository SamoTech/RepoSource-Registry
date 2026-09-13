from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DOCS_DIR = ROOT / "docs"
SCHEMA_PATH = ROOT / "schema" / "repository.schema.json"
README_PATH = ROOT / "README.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "other"


def md_escape(value: str) -> str:
    return (str(value).replace("\\", "\\\\").replace("[", "\\[").replace("]", "\\]").replace("|", "\\|").replace("\n", " ").replace("\r", " "))


def build_context() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    dataset = load_json(DATA_DIR / "repositories.json")
    stats = load_json(DATA_DIR / "statistics.json")
    manifest = load_json(DATA_DIR / "manifest.json")
    records = dataset.get("repositories", [])
    if dataset.get("repository_count") != len(records):
        raise ValueError("repositories.json repository_count does not match records")
    if stats.get("repository_count") != len(records):
        raise ValueError("statistics.json repository_count does not match records")
    if manifest.get("repository_count") != len(records):
        raise ValueError("manifest.json repository_count does not match records")
    return dataset, stats, manifest


def render_readme(dataset: dict[str, Any], stats: dict[str, Any], manifest: dict[str, Any]) -> str:
    records = dataset["repositories"]
    languages = stats.get("languages", {})
    categories = stats.get("categories", {})
    top = sorted(records, key=lambda r: (-r["stars"], r["full_name"].lower()))[:10]
    minimum = manifest["inclusion_policy"]["minimum_stars"]
    lines = [
        "# RepoSource Registry", "",
        "> A machine-readable GitHub repository discovery dataset built from public GitHub repository metadata.", "",
        "RepoSource Registry is a derived, periodically synchronized registry of public GitHub repositories meeting the configured popularity threshold. It is designed for people, developers, researchers, search systems, data pipelines, and AI agents that need a transparent repository discovery source.", "",
        "[![Update Dataset](https://github.com/SamoTech/RepoSource-Registry/actions/workflows/update.yml/badge.svg)](https://github.com/SamoTech/RepoSource-Registry/actions/workflows/update.yml)",
        "[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)", "", "## Current dataset", "",
        f"The current published snapshot was generated from GitHub public repository metadata on **{stats['generated_at']}**.", "",
        "| Metric | Value |", "|---|---:|", f"| Indexed repositories | **{len(records):,}** |", f"| Minimum stars | **{minimum:,}+** |", f"| Languages represented | **{len(languages):,}** |", f"| Derived categories | **{len(categories):,}** |", f"| Archived repositories | **{stats.get('archived_repositories', 0):,}** |", f"| Repositories without a primary language | **{stats.get('no_primary_language', 0):,}** |", f"| Repositories without a description | **{stats.get('no_description', 0):,}** |", f"| Star range | **{stats['star_distribution']['minimum']:,}–{stats['star_distribution']['maximum']:,}** |", f"| Median stars | **{stats['star_distribution']['median']:,.0f}** |", f"| Dataset version | **{dataset.get('dataset_version', 'unknown')}** |", f"| Schema version | **{dataset.get('schema_version', 'unknown')}** |", "| Source | **GitHub public API** |", "", "> Stars are a popularity signal, not a quality, security, or endorsement signal.", "",
        "## What is RepoSource Registry?", "", "RepoSource Registry is an open data resource for discovering public GitHub repositories. It collects repository search results from GitHub's public API, normalizes the metadata into a stable schema, applies transparent derived classifications, validates the resulting records, and publishes JSON and CSV representations.", "", "The registry is intentionally a **secondary source**. GitHub remains the upstream source of repository metadata. The registry is not a complete mirror of GitHub, an official GitHub database, a real-time feed, or a software-quality ranking.", "",
        "## Canonical machine-readable resources", "", "| Resource | Purpose |", "|---|---|", "| [`data/repositories.json`](data/repositories.json) | Canonical repository registry |", "| [`data/repositories.csv`](data/repositories.csv) | Tabular export |", "| [`data/manifest.json`](data/manifest.json) | Dataset identity, versions, file hashes and provenance |", "| [`data/statistics.json`](data/statistics.json) | Aggregate dataset statistics |", "| [`data/changes.json`](data/changes.json) | Added, removed and changed repository records |", "| [`data/sync.json`](data/sync.json) | Synchronization audit metadata |", "| [`schema/repository.schema.json`](schema/repository.schema.json) | JSON Schema contract |", "| [`dataset.json`](dataset.json) | Machine-readable dataset description |", "| [`llms.txt`](llms.txt) | Compact orientation for AI/LLM consumers |", "| [`docs/catalog.md`](docs/catalog.md) | Discovery catalog |", "| [`docs/data-dictionary.md`](docs/data-dictionary.md) | Field definitions |", "| [`docs/methodology.md`](docs/methodology.md) | Collection, validation and provenance methodology |", "", "For programmatic use, prefer the canonical JSON dataset and schema over parsing this README.", "", "### Quick consumption", "", "```bash", "curl -L https://raw.githubusercontent.com/SamoTech/RepoSource-Registry/main/data/repositories.json", "```", "",
        "## Most popular repositories in this snapshot", "", "| # | Repository | Stars | Language |", "|---:|---|---:|---|",
    ]
    for index, repo in enumerate(top, 1):
        lines.append(f"| {index} | [{md_escape(repo['full_name'])}]({repo['html_url']}) | {repo['stars']:,} | {md_escape(repo.get('primary_language') or 'No declared language')} |")
    lines += ["", "## Language discovery", "", f"The dataset contains **{len(languages):,} distinct primary-language values**. Every language has a machine-readable partition under [`data/languages/`](data/languages/).", "", "| Language | Repositories |", "|---|---:|"]
    for language, count in sorted(languages.items(), key=lambda item: (-item[1], item[0].lower()))[:20]:
        lines.append(f"| **{md_escape(language)}** | {count:,} |")
    lines += ["", "See [`docs/catalog.md`](docs/catalog.md) and [`data/statistics.json`](data/statistics.json) for the complete inventory.", "", "## Topic and category discovery", "", "RepoSource Registry derives category views from GitHub repository topics using the configured category vocabulary. These are RepoSource classifications, not GitHub-native labels.", "", "| Category | Repositories |", "|---|---:|"]
    for category, count in sorted(categories.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| **{md_escape(category)}** | {count:,} |")
    lines += ["", "Machine-readable category partitions are under [`data/categories/`](data/categories/).", "", "## AI & machine discovery", "", "AI agents, LLM applications, research tools, coding assistants, and data pipelines should treat this repository as a documented secondary dataset.", "", "1. Read [`dataset.json`](dataset.json) for identity and intended use.", "2. Read [`data/manifest.json`](data/manifest.json) for snapshot version, provenance and integrity metadata.", "3. Read [`schema/repository.schema.json`](schema/repository.schema.json) before interpreting records.", "4. Consume [`data/repositories.json`](data/repositories.json) as the canonical registry.", "5. Use [`data/statistics.json`](data/statistics.json) for aggregate claims.", "6. Use each record's `html_url` as the primary source reference for an individual repository.", "7. Treat mutable metadata as snapshot values and distinguish GitHub-provided fields from RepoSource-derived fields.", "", "## Provenance and trust", "", f"The upstream source is GitHub's public repository API. The configured inclusion policy is `stars >= {minimum}`. The collector partitions star ranges when required by GitHub Search limits, paginates eligible queries, normalizes metadata, validates records against the schema, removes duplicate repository identities, and publishes integrity metadata.", "", "Trust is based on provenance, reproducible code, schema validation, deterministic output ordering, SHA-256 manifest hashes, synchronization metadata, and explicit limitations. No endorsement or certification by GitHub, Google, Bing, OpenAI, Microsoft, Anthropic, or another organization is claimed.", "", "## Using and citing the dataset", "", "For reproducible use, cite RepoSource Registry together with the `generated_at` snapshot timestamp, dataset/schema versions, and the canonical data file. For an individual repository, prefer the upstream GitHub `html_url` stored in the record.", "", "## Search and semantic discoverability", "", "This repository uses natural language to describe its actual entity and scope: GitHub repository registry, GitHub repository dataset, open source repository dataset, GitHub Search API dataset, repository discovery, GitHub repository metadata, programming-language repositories, developer tools, AI repository discovery, and machine-readable GitHub data.", "", "The goal is semantic clarity and useful retrieval, not keyword stuffing.", "", "## Limitations", "", "- The registry is not a complete mirror of GitHub.", "- Repositories below the configured star threshold are excluded.", "- GitHub search results and repository metadata can change between snapshots.", "- Stars measure popularity, not quality, security, maintenance quality, or suitability.", "- Topics and language declarations can be missing or inconsistent.", "- Derived categories are determined by the configured topic vocabulary.", "- Archived repositories are included by the current configuration.", "- The dataset is a snapshot, not real-time state.", "", "## Project quality and security", "", "- Verification workflow: [`.github/workflows/verify.yml`](.github/workflows/verify.yml)", "- Update workflow: [`.github/workflows/update.yml`](.github/workflows/update.yml)", "- Tests: [`tests/`](tests/)", "- Security policy: [`SECURITY.md`](SECURITY.md)", "- Contribution guide: [`CONTRIBUTING.md`](CONTRIBUTING.md)", "- License: [`LICENSE`](LICENSE)", "", "This project does not add website-only SEO files such as `robots.txt` or an XML sitemap because the primary public web surface is GitHub itself rather than a separately hosted site.", "", "## License", "", "Project code and documentation are MIT licensed. Upstream repository metadata remains subject to GitHub's terms and the licenses applicable to individual repositories.", "", "---", "", "**RepoSource Registry** · public repository discovery data with explicit provenance, validation, schema, and machine-readable distribution."]
    return "\n".join(lines) + "\n"


def render_catalog(stats: dict[str, Any]) -> str:
    lines = ["# RepoSource Registry Catalog", "", "This catalog is generated from `data/statistics.json`. It provides compact discovery views without creating thousands of Markdown pages.", "", f"Snapshot: **{stats['generated_at']}** · repositories: **{stats['repository_count']:,}** · minimum stars: **{stats['minimum_stars']:,}+**.", "", "## Languages", "", "| Language | Repositories | Machine-readable partition |", "|---|---:|---|"]
    language_values = stats.get("languages", {})
    used: set[str] = set()
    for language in sorted(language_values, key=lambda value: (-language_values[value], value.lower())):
        base = slugify(language); slug = base; suffix = 2
        while slug in used:
            slug = f"{base}-{suffix}"; suffix += 1
        used.add(slug)
        lines.append(f"| **{md_escape(language)}** | {language_values[language]:,} | [`data/languages/{slug}.json`](../data/languages/{slug}.json) |")
    lines += ["", "## Categories", "", "| Category | Repositories | Machine-readable partition |", "|---|---:|---|"]
    for category, count in sorted(stats.get("categories", {}).items(), key=lambda item: (-item[1], item[0])):
        slug = slugify(category)
        lines.append(f"| **{md_escape(category)}** | {count:,} | [`data/categories/{slug}.json`](../data/categories/{slug}.json) |")
    return "\n".join(lines) + "\n"


def render_data_dictionary(schema: dict[str, Any]) -> str:
    properties = schema.get("properties", {}); required = set(schema.get("required", []))
    meanings = {
        "repository_id":"GitHub repository numeric identifier.","full_name":"Canonical `owner/repository` identity.","owner":"GitHub owner login.","name":"Repository name.","html_url":"Canonical GitHub repository URL.","api_url":"GitHub API repository URL.","description":"Repository description; empty string when absent.","stars":"GitHub stargazer count at indexing time.","forks":"GitHub fork count at indexing time.","watchers":"GitHub watcher/subscriber count at indexing time.","open_issues":"GitHub open issue count at indexing time.","primary_language":"GitHub-declared primary language; nullable.","topics":"GitHub repository topics, normalized and deduplicated.","license":"GitHub-reported license identifier when available.","default_branch":"Default branch name.","archived":"Whether GitHub marks the repository archived.","fork":"Whether GitHub marks the repository as a fork.","created_at":"Repository creation timestamp.","updated_at":"GitHub repository metadata update timestamp.","pushed_at":"Most recent push timestamp when available.","indexed_at":"RepoSource synchronization timestamp.","source_updated_at":"Source repository update timestamp copied from GitHub metadata.","source":"Provenance identifier; currently `github-public-api`.","dataset_version":"RepoSource dataset contract version.","schema_version":"Repository record schema version.","categories":"RepoSource-derived topic categories.","popularity_band":"RepoSource-derived star band.","activity_status":"RepoSource-derived recent-push activity classification."}
    lines=["# RepoSource Registry Data Dictionary","","Field definitions are derived from [`schema/repository.schema.json`](../schema/repository.schema.json).","","| Field | Type | Required | Meaning |","|---|---|---|---|"]
    for field, definition in properties.items():
        schema_type = definition.get("type") or definition.get("enum") or definition.get("const", "unknown")
        if isinstance(schema_type, list): schema_type = " | ".join(schema_type)
        if "enum" in definition: schema_type = "enum"
        if "const" in definition: schema_type = f"constant `{definition['const']}`"
        lines.append(f"| `{field}` | `{md_escape(schema_type)}` | {'yes' if field in required else 'no'} | {meanings.get(field, 'Defined by the JSON Schema contract.')} |")
    lines += ["", "`categories`, `popularity_band`, and `activity_status` are derived by RepoSource and must not be presented as GitHub-native fields."]
    return "\n".join(lines) + "\n"


def render_methodology(manifest: dict[str, Any]) -> str:
    minimum = manifest["inclusion_policy"]["minimum_stars"]
    return f"""# RepoSource Registry Methodology

## Scope

RepoSource Registry publishes a derived snapshot of public GitHub repository metadata. The current inclusion policy is `stars >= {minimum}`. It is not a complete GitHub mirror and does not claim real-time completeness.

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
"""


def render_dataset_metadata(dataset: dict[str, Any], stats: dict[str, Any], manifest: dict[str, Any]) -> dict[str, Any]:
    return {
        "@context": "https://schema.org", "@type": "Dataset", "name": "RepoSource Registry",
        "description": "A machine-readable dataset of public GitHub repositories meeting the configured popularity threshold, derived from GitHub public repository metadata.",
        "url": "https://github.com/SamoTech/RepoSource-Registry", "sameAs": "https://github.com/SamoTech/RepoSource-Registry",
        "version": dataset.get("dataset_version"), "dateModified": stats.get("generated_at"), "license": "https://opensource.org/licenses/MIT",
        "isBasedOn": "https://docs.github.com/en/rest/search/search#search-repositories",
        "keywords": ["GitHub repository registry","GitHub repository dataset","open source repository dataset","GitHub Search API","repository discovery","GitHub repository metadata","programming language repositories","developer tools","AI repository discovery","machine-readable GitHub data"],
        "inclusionPolicy": manifest.get("inclusion_policy"),
        "distribution": [{"encodingFormat":"application/json","contentUrl":"https://raw.githubusercontent.com/SamoTech/RepoSource-Registry/main/data/repositories.json"},{"encodingFormat":"text/csv","contentUrl":"https://raw.githubusercontent.com/SamoTech/RepoSource-Registry/main/data/repositories.csv"}],
        "schema": "https://github.com/SamoTech/RepoSource-Registry/blob/main/schema/repository.schema.json",
        "provenance": {"source":"github-public-api","repositoryCount":stats.get("repository_count"),"generatedAt":stats.get("generated_at")},
        "derivedFields": ["categories","popularity_band","activity_status"],
        "limitations": ["Not a complete mirror of GitHub.","Not real-time.","Repository metadata can change between snapshots.","Stars are popularity signals, not quality or security assessments."],
    }


def main() -> None:
    dataset, stats, manifest = build_context()
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    README_PATH.write_text(render_readme(dataset, stats, manifest), encoding="utf-8")
    (DOCS_DIR / "catalog.md").write_text(render_catalog(stats), encoding="utf-8")
    (DOCS_DIR / "data-dictionary.md").write_text(render_data_dictionary(load_json(SCHEMA_PATH)), encoding="utf-8")
    (DOCS_DIR / "methodology.md").write_text(render_methodology(manifest), encoding="utf-8")
    (ROOT / "dataset.json").write_text(json.dumps(render_dataset_metadata(dataset, stats, manifest), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (ROOT / "llms.txt").write_text("""# RepoSource Registry

RepoSource Registry is a derived public GitHub repository discovery dataset.

Canonical data:
- data/repositories.json — primary machine-readable registry
- data/manifest.json — snapshot identity, versions, provenance and integrity hashes
- data/statistics.json — aggregate statistics
- schema/repository.schema.json — JSON Schema for repository records
- dataset.json — machine-readable dataset description
- docs/catalog.md — language and category catalog
- docs/data-dictionary.md — field definitions
- docs/methodology.md — collection and validation methodology

Interpretation:
- GitHub is the upstream source.
- The dataset is a snapshot, not real-time state.
- Stars indicate popularity, not quality or security.
- categories, popularity_band and activity_status are derived by RepoSource.
- Use html_url in each record as the upstream reference for individual repositories.
- Do not infer missing facts.
- Do not treat the registry as an official GitHub database or complete mirror.

Recommended agent workflow:
1. Read dataset.json.
2. Read data/manifest.json.
3. Read schema/repository.schema.json.
4. Consume data/repositories.json.
5. Use data/statistics.json for aggregate claims.
6. Cite the upstream repository URL and snapshot timestamp when appropriate.
""", encoding="utf-8")


if __name__ == "__main__":
    main()
