from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
SCHEMA = ROOT / "schema" / "repository.schema.json"
CONFIG = ROOT / "config.json"


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "other"


def unique_slugs(values: list[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    used: set[str] = set()
    for value in sorted(values, key=str.lower):
        base = slugify(value)
        slug = base
        n = 2
        while slug in used:
            slug = f"{base}-{n}"
            n += 1
        used.add(slug)
        result[value] = slug
    return result


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def source_view(repo: dict[str, Any]) -> str:
    ignored = {"indexed_at", "dataset_version", "categories", "popularity_band", "activity_status"}
    return json.dumps({k: v for k, v in repo.items() if k not in ignored}, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def load_previous(path: Path | None) -> dict[int, dict[str, Any]]:
    if not path or not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return {int(r["repository_id"]): r for r in payload.get("repositories", [])}


def validate_dataset(payload: dict[str, Any], minimum: int) -> None:
    repos = payload.get("repositories")
    if not isinstance(repos, list):
        raise ValueError("repositories.json does not contain a repository list")
    ids: set[int] = set()
    names: set[str] = set()
    for repo in repos:
        rid = repo.get("repository_id")
        name = repo.get("full_name")
        if not isinstance(rid, int) or rid <= 0:
            raise ValueError(f"Invalid repository_id: {rid!r}")
        if rid in ids:
            raise ValueError(f"Duplicate repository_id: {rid}")
        if not isinstance(name, str) or not name:
            raise ValueError("Missing full_name")
        if name in names:
            raise ValueError(f"Duplicate full_name: {name}")
        if int(repo.get("stars", -1)) < minimum:
            raise ValueError(f"Threshold violation: {name}")
        ids.add(rid)
        names.add(name)
    expected = sorted(repos, key=lambda r: (-int(r["stars"]), str(r["full_name"]).lower()))
    if repos != expected:
        raise ValueError("Canonical dataset is not deterministically ordered")


def build_changes(previous: dict[int, dict[str, Any]], current: list[dict[str, Any]]) -> dict[str, Any]:
    now = {int(r["repository_id"]): r for r in current}
    added_ids = sorted(set(now) - set(previous))
    removed_ids = sorted(set(previous) - set(now))
    changed_ids = sorted(i for i in set(now) & set(previous) if source_view(now[i]) != source_view(previous[i]))
    return {
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "summary": {"added": len(added_ids), "removed": len(removed_ids), "changed": len(changed_ids)},
        "added": [now[i] for i in added_ids],
        "removed": [previous[i] for i in removed_ids],
        "changed_repository_ids": changed_ids,
    }


def build_statistics(repos: list[dict[str, Any]], generated_at: str, minimum: int) -> dict[str, Any]:
    stars = sorted(int(r["stars"]) for r in repos)
    median = 0 if not stars else (stars[len(stars)//2] if len(stars) % 2 else (stars[len(stars)//2-1] + stars[len(stars)//2]) / 2)
    languages = Counter(r.get("primary_language") or "No declared language" for r in repos)
    categories = Counter(c for r in repos for c in r.get("categories", []))
    return {
        "generated_at": generated_at,
        "minimum_stars": minimum,
        "repository_count": len(repos),
        "records_fetched": len(repos),
        "records_accepted": len(repos),
        "records_rejected": 0,
        "star_distribution": {"minimum": min(stars) if stars else 0, "maximum": max(stars) if stars else 0, "median": median},
        "forked_repositories": sum(bool(r.get("fork")) for r in repos),
        "archived_repositories": sum(bool(r.get("archived")) for r in repos),
        "no_primary_language": sum(not r.get("primary_language") for r in repos),
        "no_description": sum(not r.get("description") for r in repos),
        "star_bands": dict(Counter(r.get("popularity_band", "unknown") for r in repos)),
        "languages": dict(languages.most_common()),
        "categories": dict(categories.most_common()),
        "created_by_year": dict(sorted(Counter((r.get("created_at") or "unknown")[:4] for r in repos).items())),
        "updated_by_year": dict(sorted(Counter((r.get("updated_at") or "unknown")[:4] for r in repos).items())),
    }


def rebuild_indexes(repos: list[dict[str, Any]]) -> tuple[dict[str, str], list[str]]:
    languages = sorted({r.get("primary_language") or "No declared language" for r in repos}, key=str.lower)
    slugs = unique_slugs(languages)
    language_dir = DATA / "languages"
    category_dir = DATA / "categories"
    language_dir.mkdir(parents=True, exist_ok=True)
    category_dir.mkdir(parents=True, exist_ok=True)
    for old in language_dir.glob("*.json"):
        old.unlink()
    for language in languages:
        subset = [r for r in repos if (r.get("primary_language") or "No declared language") == language]
        (language_dir / f"{slugs[language]}.json").write_text(json.dumps(subset, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    categories = sorted({c for r in repos for c in r.get("categories", [])})
    for old in category_dir.glob("*.json"):
        old.unlink()
    for category in categories:
        subset = [r for r in repos if category in r.get("categories", [])]
        (category_dir / f"{slugify(category)}.json").write_text(json.dumps(subset, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return slugs, categories


def generate_readme(payload: dict[str, Any], stats: dict[str, Any], slugs: dict[str, str], categories: list[str]) -> None:
    repos = payload["repositories"]
    languages = Counter(r.get("primary_language") or "No declared language" for r in repos)
    category_counts = Counter(c for r in repos for c in r.get("categories", []))
    minimum = payload["inclusion_policy"]["minimum_stars"]
    lines = [
        "# RepoSource Registry", "",
        "> **A living, machine-readable index of notable public GitHub repositories.**", ">",
        "> GitHub is the upstream source. RepoSource Registry normalizes, validates, classifies, and publishes the resulting dataset for developers, researchers, applications, and AI agents.", "",
        "[![Update Dataset](https://github.com/SamoTech/RepoSource-Registry/actions/workflows/update.yml/badge.svg)](https://github.com/SamoTech/RepoSource-Registry/actions/workflows/update.yml)",
        "[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)",
        f"[![Minimum Stars](https://img.shields.io/badge/minimum%20stars-{minimum:,}%2B-blue)](config.json)", "", "---", "",
        "## Index at a glance", "", "| Metric | Value |", "|---|---:|",
        f"| Indexed repositories | **{len(repos):,}** |", f"| Minimum stars | **{minimum:,}+** |", f"| Languages represented | **{len(languages):,}** |", f"| Derived categories | **{len(categories):,}** |", f"| Last synchronized | **{stats['generated_at']}** |", "",
        "> **Popularity index, not an endorsement.** Stars indicate popularity, not software quality, security, maintenance quality, or suitability.", "",
        "## Data access", "", "Applications should consume the machine-readable datasets instead of parsing this README.", "",
        "| Resource | Purpose |", "|---|---|",
        "| [`data/repositories.json`](data/repositories.json) | Canonical dataset |", "| [`data/repositories.csv`](data/repositories.csv) | Tabular export |", "| [`data/manifest.json`](data/manifest.json) | Dataset manifest and SHA-256 checksums |", "| [`data/statistics.json`](data/statistics.json) | Dataset statistics |", "| [`data/sync.json`](data/sync.json) | Synchronization audit record |", "| [`data/changes.json`](data/changes.json) | Change feed |", "| [`schema/repository.schema.json`](schema/repository.schema.json) | Schema contract |", "",
        "### Quick consumption", "", "```bash", "curl -L https://raw.githubusercontent.com/SamoTech/RepoSource-Registry/main/data/repositories.json", "```", "",
        "## Most starred", "", "| # | Repository | Stars | Language | Activity |", "|---:|---|---:|---|---|",
    ]
    for i, repo in enumerate(repos[:25], 1):
        lines.append(f"| {i} | [{repo['full_name']}]({repo['html_url']}) | {int(repo['stars']):,} | {repo.get('primary_language') or 'No declared language'} | {repo.get('activity_status', 'unknown')} |")
    lines += ["", "## Language index", "", "| Language | Repositories | Dataset |", "|---|---:|---|"]
    for language, count in sorted(languages.items(), key=lambda x: (-x[1], x[0].lower())):
        slug = slugs[language]
        lines.append(f"| **{language}** | {count:,} | [`{slug}.json`](data/languages/{slug}.json) |")
    lines += ["", "## Category index", "", "| Category | Repositories | Dataset |", "|---|---:|---|"]
    for category, count in sorted(category_counts.items(), key=lambda x: (-x[1], x[0])):
        lines.append(f"| **{category}** | {count:,} | [`{slugify(category)}.json`](data/categories/{slugify(category)}.json) |")
    lines += [
        "", "## Methodology", "", f"The default policy is `stars >= {minimum}` with no fixed maximum repository count. The collector uses GitHub's official Search API, partitions result ranges when necessary, normalizes GitHub-native metadata, applies transparent RepoSource classifications, validates the dataset, and publishes deterministic machine-readable outputs.", "",
        "## Provenance", "", "RepoSource Registry is a derived public dataset based on GitHub public repository metadata. It is not an official GitHub database and is not a real-time feed. Derived categories, popularity bands, and activity status are RepoSource classifications.", "",
        "## AI-agent usage", "", "Start with [`AGENTS.md`](AGENTS.md) and [`llms.txt`](llms.txt). Prefer [`data/manifest.json`](data/manifest.json) and [`data/repositories.json`](data/repositories.json) over README scraping, and validate records against the schema.", "",
        "## Limitations", "", "Stars are a popularity signal, not a quality score. GitHub search indexing and API behavior can change. The pipeline must fail closed when it cannot safely establish the eligible result set.", "",
        "## Contributing", "", "See [`CONTRIBUTING.md`](CONTRIBUTING.md). Security issues should follow [`SECURITY.md`](SECURITY.md).", "",
        "## License", "", "Project code and documentation are MIT licensed. Upstream repository metadata remains subject to GitHub's terms and the respective repositories' licenses.", "", "---", "", "**RepoSource Registry** · Reliable data. Clear provenance. Stable schema. Simple consumption."
    ]
    (ROOT / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--previous", type=Path)
    args = parser.parse_args()
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    payload = json.loads((DATA / "repositories.json").read_text(encoding="utf-8"))
    minimum = int(cfg["min_stars"])
    validate_dataset(payload, minimum)
    repos = payload["repositories"]
    generated_at = payload.get("generated_at") or datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    stats = build_statistics(repos, generated_at, minimum)
    previous = load_previous(args.previous)
    changes = build_changes(previous, repos)
    slugs, categories = rebuild_indexes(repos)
    (DATA / "statistics.json").write_text(json.dumps(stats, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (DATA / "changes.json").write_text(json.dumps(changes, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    sync = {
        "sync_id": datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
        "generated_at": generated_at,
        "source_api": "https://api.github.com/search/repositories",
        "minimum_stars": minimum,
        "dataset_version": payload.get("dataset_version", cfg.get("dataset_version", "1.0.0")),
        "schema_version": cfg.get("schema_version", "1.1.0"),
        "fetched": stats["records_fetched"],
        "accepted": stats["records_accepted"],
        "rejected": stats["records_rejected"],
        "added": changes["summary"]["added"],
        "removed": changes["summary"]["removed"],
        "changed": changes["summary"]["changed"],
        "failure_count": 0,
    }
    (DATA / "sync.json").write_text(json.dumps(sync, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tracked = [DATA / "repositories.json", DATA / "repositories.csv", DATA / "statistics.json", DATA / "changes.json", DATA / "sync.json", SCHEMA]
    manifest = {
        "dataset": "RepoSource Registry",
        "dataset_version": payload.get("dataset_version", cfg.get("dataset_version", "1.0.0")),
        "schema_version": cfg.get("schema_version", "1.1.0"),
        "generated_at": generated_at,
        "source": "github-public-api",
        "inclusion_policy": payload.get("inclusion_policy", {"minimum_stars": minimum}),
        "repository_count": len(repos),
        "languages": sorted(slugs, key=str.lower),
        "categories": categories,
        "files": {str(p.relative_to(ROOT)): {"bytes": p.stat().st_size, "sha256": sha256(p)} for p in tracked if p.exists()},
    }
    (DATA / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    generate_readme(payload, stats, slugs, categories)
    print(json.dumps({"repository_count": len(repos), "changes": changes["summary"], "manifest": "data/manifest.json"}, indent=2))


if __name__ == "__main__":
    main()
