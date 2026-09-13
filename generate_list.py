from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import time
import uuid
from collections import Counter
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import requests
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent
CONFIG_PATH = ROOT / "config.json"
SCHEMA_PATH = ROOT / "schema" / "repository.schema.json"
DATA_DIR = ROOT / "data"
API_URL = "https://api.github.com/search/repositories"


def load_config() -> dict[str, Any]:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def github_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "RepoSource-Registry/1.1",
    })
    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    if token:
        session.headers["Authorization"] = f"Bearer {token}"
    return session


def request_json(session: requests.Session, url: str, params: dict[str, Any], cfg: dict[str, Any]) -> dict[str, Any]:
    retries = int(cfg["max_retries"])
    timeout = int(cfg["request_timeout_seconds"])
    for attempt in range(retries + 1):
        try:
            response = session.get(url, params=params, timeout=timeout)
            remaining = response.headers.get("X-RateLimit-Remaining")
            if response.status_code == 403 and remaining == "0":
                reset = int(response.headers.get("X-RateLimit-Reset", time.time() + 60))
                sleep_for = max(1, reset - int(time.time()) + 1)
                if attempt >= retries:
                    raise RuntimeError("GitHub API rate limit exhausted after retries")
                time.sleep(min(sleep_for, int(cfg.get("max_rate_limit_wait_seconds", 120))))
                continue
            if response.status_code in {429, 500, 502, 503, 504}:
                if attempt >= retries:
                    response.raise_for_status()
                time.sleep(min(60, 2 ** attempt))
                continue
            response.raise_for_status()
            payload = response.json()
            if not isinstance(payload, dict):
                raise ValueError("GitHub API returned a non-object JSON payload")
            return payload
        except (requests.RequestException, ValueError):
            if attempt >= retries:
                raise
            time.sleep(min(60, 2 ** attempt))
    raise RuntimeError("unreachable")


def search_count(session: requests.Session, query: str, cfg: dict[str, Any]) -> int:
    payload = request_json(session, API_URL, {"q": query, "per_page": 1}, cfg)
    return int(payload.get("total_count", 0))


def collect_query(session: requests.Session, query: str, count: int, cfg: dict[str, Any], out: list[dict[str, Any]]) -> None:
    per_page = int(cfg["per_page"])
    if count > 1000:
        raise RuntimeError(f"Unsafe GitHub Search query (>1000 results): {query!r} count={count}")

    # total_count is a snapshot, not a pagination invariant. Search results can
    # change between the count request and subsequent pages. A short page is
    # therefore a normal termination signal unless a refreshed count proves that
    # more results should still be requested.
    expected_count = count
    accumulated = 0
    page = 1
    max_pages = (expected_count + per_page - 1) // per_page

    while page <= max_pages:
        payload = request_json(session, API_URL, {
            "q": query,
            "sort": "stars",
            "order": "desc",
            "per_page": per_page,
            "page": page,
        }, cfg)
        if payload.get("incomplete_results") is True:
            raise RuntimeError(f"GitHub returned incomplete search results: query={query!r} page={page}")

        items = payload.get("items", [])
        if not isinstance(items, list):
            raise ValueError(f"GitHub Search response has malformed items: query={query!r} page={page}")

        out.extend(items)
        accumulated += len(items)

        if not items:
            break

        if len(items) < per_page:
            # The earlier total_count may have become stale. Refresh it once at
            # the pagination boundary so a dataset growth/change cannot cause us
            # to stop merely because this page was short.
            refreshed_count = search_count(session, query, cfg)
            if refreshed_count <= accumulated:
                break
            expected_count = refreshed_count
            max_pages = max(max_pages, (expected_count + per_page - 1) // per_page)

        page += 1


def partition_range(session: requests.Session, low: int, high: int, cfg: dict[str, Any], out: list[dict[str, Any]]) -> None:
    query = f"stars:{low}..{high}"
    count = search_count(session, query, cfg)
    if count <= 1000:
        collect_query(session, query, count, cfg, out)
        return
    if low == high:
        # Secondary partition. GitHub Search supports created-date qualifiers; split the
        # exact-star bucket by calendar year, then fail closed if a leaf is still too large.
        start_year = 2008
        current_year = datetime.now(timezone.utc).year
        for year in range(start_year, current_year + 1):
            subquery = f"stars:{low}..{high} created:{year}-01-01..{year}-12-31"
            subcount = search_count(session, subquery, cfg)
            if subcount > 1000:
                raise RuntimeError(f"Cannot safely partition exact-star bucket: {subquery!r} count={subcount}")
            collect_query(session, subquery, subcount, cfg, out)
        return
    mid = (low + high) // 2
    partition_range(session, low, mid, cfg, out)
    partition_range(session, mid + 1, high, cfg, out)


def collect_all(session: requests.Session, cfg: dict[str, Any], out: list[dict[str, Any]]) -> None:
    minimum = int(cfg["min_stars"])
    # 1,000,000 is a partition ceiling, not an eligibility limit. If GitHub ever
    # reports a repository above it, the collector fails closed instead of truncating.
    ceiling = int(cfg.get("star_partition_ceiling", 1_000_000))
    if search_count(session, f"stars:>={minimum}", cfg) == 0:
        return
    if search_count(session, f"stars:>{ceiling}", cfg) > 0:
        raise RuntimeError("Configured star partition ceiling is below an eligible repository")
    partition_range(session, minimum, ceiling, cfg, out)


def normalize(repo: dict[str, Any], indexed_at: str, cfg: dict[str, Any]) -> dict[str, Any]:
    license_info = repo.get("license") or {}
    owner = repo.get("owner") or {}
    return {
        "repository_id": repo.get("id"),
        "full_name": repo.get("full_name"),
        "owner": owner.get("login"),
        "name": repo.get("name"),
        "html_url": repo.get("html_url"),
        "api_url": repo.get("url"),
        "description": repo.get("description") or "",
        "stars": repo.get("stargazers_count", 0),
        "forks": repo.get("forks_count", 0),
        "watchers": repo.get("watchers_count", 0),
        "open_issues": repo.get("open_issues_count", 0),
        "primary_language": repo.get("language"),
        "topics": sorted(set(repo.get("topics") or [])),
        "license": license_info.get("spdx_id") or license_info.get("key"),
        "default_branch": repo.get("default_branch"),
        "archived": bool(repo.get("archived", False)),
        "fork": bool(repo.get("fork", False)),
        "created_at": repo.get("created_at"),
        "updated_at": repo.get("updated_at"),
        "pushed_at": repo.get("pushed_at"),
        "indexed_at": indexed_at,
        "source": "github-public-api",
        "dataset_version": cfg["dataset_version"],
        "schema_version": cfg.get("schema_version", "1.1.0"),
        "source_updated_at": repo.get("updated_at"),
    }


def classify(record: dict[str, Any], cfg: dict[str, Any], reference_time: datetime) -> dict[str, Any]:
    topics = set(record["topics"])
    record["categories"] = sorted(name for name, terms in cfg["categories"].items() if topics.intersection(terms))
    record["popularity_band"] = (
        "50k+" if record["stars"] >= 50000 else
        "10k+" if record["stars"] >= 10000 else
        "5k+" if record["stars"] >= 5000 else "2k+"
    )
    pushed = record.get("pushed_at")
    if not pushed:
        record["activity_status"] = "unknown"
    else:
        pushed_dt = datetime.fromisoformat(pushed.replace("Z", "+00:00"))
        record["activity_status"] = "active" if (reference_time - pushed_dt).days <= int(cfg.get("active_days", 180)) else "inactive"
    return record


def validate_records(records: list[dict[str, Any]], cfg: dict[str, Any]) -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    ids: set[int] = set()
    names: set[str] = set()
    minimum = int(cfg["min_stars"])
    for record in records:
        errors = sorted(validator.iter_errors(record), key=lambda e: list(e.path))
        if errors:
            raise ValueError(f"Schema validation failed for {record.get('full_name')}: {errors[0].message}")
        if record["stars"] < minimum:
            raise ValueError(f"Threshold violation: {record['full_name']}")
        if record["repository_id"] in ids:
            raise ValueError(f"Duplicate repository_id: {record['repository_id']}")
        if record["full_name"] in names:
            raise ValueError(f"Duplicate full_name: {record['full_name']}")
        ids.add(record["repository_id"])
        names.add(record["full_name"])


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "other"


def unique_slugs(values: set[str]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    used: set[str] = set()
    for value in sorted(values, key=str.lower):
        base = slugify(value)
        slug = base
        index = 2
        while slug in used:
            slug = f"{base}-{index}"
            index += 1
        used.add(slug)
        mapping[value] = slug
    return mapping


def md_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace("[", "\\[").replace("]", "\\]").replace("|", "\\|").replace("\n", " ").replace("\r", " ")


def csv_safe(value: Any) -> Any:
    if isinstance(value, str) and value.startswith(("=", "+", "-", "@")):
        return "'" + value
    return value


def read_previous() -> dict[int, dict[str, Any]]:
    path = DATA_DIR / "repositories.json"
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        return {int(r["repository_id"]): r for r in payload.get("repositories", [])}
    except (OSError, ValueError, KeyError, TypeError):
        return {}


def source_signature(record: dict[str, Any]) -> str:
    source_fields = {k: v for k, v in record.items() if k not in {"indexed_at", "activity_status", "dataset_version", "schema_version"}}
    return json.dumps(source_fields, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def compute_changes(previous: dict[int, dict[str, Any]], current: list[dict[str, Any]]) -> dict[str, Any]:
    current_map = {int(r["repository_id"]): r for r in current}
    added = sorted(set(current_map) - set(previous))
    removed = sorted(set(previous) - set(current_map))
    changed = sorted(i for i in set(current_map) & set(previous) if source_signature(current_map[i]) != source_signature(previous[i]))
    return {
        "added": [current_map[i] for i in added],
        "removed": [previous[i] for i in removed],
        "changed_repository_ids": changed,
        "summary": {"added": len(added), "removed": len(removed), "changed": len(changed)},
    }


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_outputs(records: list[dict[str, Any]], cfg: dict[str, Any], stats: dict[str, Any], changes: dict[str, Any], sync_meta: dict[str, Any]) -> None:
    DATA_DIR.mkdir(exist_ok=True)
    (DATA_DIR / "languages").mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "categories").mkdir(parents=True, exist_ok=True)
    records.sort(key=lambda r: (-r["stars"], r["full_name"].lower()))

    payload = {
        "dataset": "RepoSource Registry",
        "dataset_version": cfg["dataset_version"],
        "schema_version": cfg.get("schema_version", "1.1.0"),
        "generated_at": stats["generated_at"],
        "inclusion_policy": {"minimum_stars": cfg["min_stars"]},
        "repository_count": len(records),
        "repositories": records,
    }
    (DATA_DIR / "repositories.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    fields = list(records[0].keys()) if records else list(payload["repositories"])
    with (DATA_DIR / "repositories.csv").open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for record in records:
            writer.writerow({k: csv_safe(json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v) for k, v in record.items()})

    languages = sorted({r["primary_language"] or "No declared language" for r in records}, key=str.lower)
    language_slugs = unique_slugs(set(languages))
    for language in languages:
        subset = [r for r in records if (r["primary_language"] or "No declared language") == language]
        (DATA_DIR / "languages" / f"{language_slugs[language]}.json").write_text(json.dumps({"language": language, "repository_count": len(subset), "repositories": subset}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    categories = sorted({c for r in records for c in r.get("categories", [])})
    for category in categories:
        subset = [r for r in records if category in r.get("categories", [])]
        (DATA_DIR / "categories" / f"{slugify(category)}.json").write_text(json.dumps({"category": category, "repository_count": len(subset), "repositories": subset}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    statistics = build_statistics(records, cfg, stats)
    (DATA_DIR / "statistics.json").write_text(json.dumps(statistics, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (DATA_DIR / "changes.json").write_text(json.dumps(changes, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (DATA_DIR / "sync.json").write_text(json.dumps(sync_meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    generate_readme(records, cfg, statistics, language_slugs)

    manifest = {
        "dataset": "RepoSource Registry",
        "dataset_version": cfg["dataset_version"],
        "schema_version": cfg.get("schema_version", "1.1.0"),
        "generated_at": statistics["generated_at"],
        "source": "github-public-api",
        "inclusion_policy": {"minimum_stars": cfg["min_stars"]},
        "repository_count": len(records),
        "languages": languages,
        "categories": categories,
        "files": {},
    }
    tracked = [DATA_DIR / "repositories.json", DATA_DIR / "repositories.csv", DATA_DIR / "statistics.json", DATA_DIR / "changes.json", DATA_DIR / "sync.json", SCHEMA_PATH]
    for path in tracked:
        if path.exists():
            manifest["files"][str(path.relative_to(ROOT))] = {"bytes": path.stat().st_size, "sha256": sha256_file(path)}
    (DATA_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def build_statistics(records: list[dict[str, Any]], cfg: dict[str, Any], stats: dict[str, Any]) -> dict[str, Any]:
    stars = sorted(r["stars"] for r in records)
    median = stars[len(stars) // 2] if stars and len(stars) % 2 else ((stars[len(stars)//2-1] + stars[len(stars)//2]) / 2 if stars else 0)
    languages = Counter(r["primary_language"] or "No declared language" for r in records)
    categories = Counter(c for r in records for c in r.get("categories", []))
    created_years = Counter((r["created_at"] or "unknown")[:4] if r["created_at"] else "unknown" for r in records)
    updated_years = Counter((r["updated_at"] or "unknown")[:4] if r["updated_at"] else "unknown" for r in records)
    return {
        **stats,
        "repository_count": len(records),
        "star_distribution": {"minimum": min(stars) if stars else 0, "maximum": max(stars) if stars else 0, "median": median},
        "forked_repositories": sum(1 for r in records if r["fork"]),
        "archived_repositories": sum(1 for r in records if r["archived"]),
        "no_primary_language": sum(1 for r in records if not r["primary_language"]),
        "no_description": sum(1 for r in records if not r["description"]),
        "star_bands": dict(Counter(r["popularity_band"] for r in records)),
        "languages": dict(languages.most_common()),
        "categories": dict(categories.most_common()),
        "created_by_year": dict(sorted(created_years.items())),
        "updated_by_year": dict(sorted(updated_years.items())),
    }


def generate_readme(records: list[dict[str, Any]], cfg: dict[str, Any], stats: dict[str, Any], language_slugs: dict[str, str]) -> None:
    languages = Counter(r["primary_language"] or "No declared language" for r in records)
    categories = Counter(c for r in records for c in r.get("categories", []))
    lines = [
        "# RepoSource Registry", "", 
        "> **A living, machine-readable index of notable public GitHub repositories.**", ">", 
        "> GitHub is the upstream source; RepoSource Registry normalizes, validates, classifies, and publishes the resulting dataset for humans and machines.", "",
        "[![Update Dataset](https://github.com/SamoTech/RepoSource-Registry/actions/workflows/update.yml/badge.svg)](https://github.com/SamoTech/RepoSource-Registry/actions/workflows/update.yml)",
        "[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)",
        f"[![Minimum Stars](https://img.shields.io/badge/minimum%20stars-{cfg['min_stars']:,}%2B-blue)](config.json)", "", "---", "",
        "## Index at a glance", "", "| Metric | Value |", "|---|---:|",
        f"| Indexed repositories | **{len(records):,}** |", f"| Minimum stars | **{cfg['min_stars']:,}+** |", f"| Languages represented | **{len(languages):,}** |", f"| Derived categories | **{len(categories):,}** |", f"| Last synchronized | **{stats['generated_at']}** |", "",
        "> **Popularity index, not an endorsement.** Stars indicate popularity, not software quality, security, or suitability.", "",
        "## Machine-readable data", "", "The README is a presentation layer. Applications should consume the published datasets directly.", "",
        "| Resource | Purpose |", "|---|---|",
        "| [`repositories.json`](data/repositories.json) | Canonical dataset |", "| [`repositories.csv`](data/repositories.csv) | Tabular export |", "| [`manifest.json`](data/manifest.json) | Dataset metadata and SHA-256 integrity data |", "| [`statistics.json`](data/statistics.json) | Dataset analytics |", "| [`sync.json`](data/sync.json) | Synchronization audit record |", "| [`changes.json`](data/changes.json) | Added/removed/changed repository feed |", "| [`schema/repository.schema.json`](schema/repository.schema.json) | Data contract |", "",
        "### Quick consumption", "", "```bash", "curl -L https://raw.githubusercontent.com/SamoTech/RepoSource-Registry/main/data/repositories.json", "```", "",
        "## Most starred", "", "| # | Repository | Stars | Language | Activity |", "|---:|---|---:|---|---|",
    ]
    for index, repo in enumerate(records[:25], 1):
        lines.append(f"| {index} | [{md_escape(repo['full_name'])}]({repo['html_url']}) | {repo['stars']:,} | {md_escape(repo['primary_language'] or 'No declared language')} | {repo['activity_status']} |")
    lines += ["", "## Language index", "", "| Language | Repositories | Dataset |", "|---|---:|---|"]
    for language, count in sorted(languages.items(), key=lambda x: (-x[1], x[0].lower())):
        slug = language_slugs[language]
        lines.append(f"| **{md_escape(language)}** | {count:,} | [`{slug}.json`](data/languages/{slug}.json) |")
    lines += ["", "## Category index", "", "| Category | Repositories | Dataset |", "|---|---:|---|"]
    for category, count in sorted(categories.items(), key=lambda x: (-x[1], x[0])):
        lines.append(f"| **{md_escape(category)}** | {count:,} | [`{slugify(category)}.json`](data/categories/{slugify(category)}.json) |")
    lines += [
        "", "## Methodology", "", f"The default inclusion policy is `stars >= {cfg['min_stars']}` with no fixed maximum repository count. The collector uses GitHub's official Search API, partitions result ranges when required by GitHub's search limits, normalizes source metadata, applies deterministic RepoSource classifications, validates the dataset, and publishes machine-readable outputs.", "",
        "## Provenance", "", "RepoSource Registry is a derived public dataset based on GitHub public repository metadata. It is not an official GitHub database and is not a real-time feed. Repository metadata can change between synchronization runs.", "",
        "Derived fields including categories, popularity bands, and activity status are RepoSource classifications and must not be interpreted as GitHub-provided facts.", "",
        "## AI-agent consumption", "", "AI agents should start with [`AGENTS.md`](AGENTS.md) and [`llms.txt`](llms.txt), then consume [`data/manifest.json`](data/manifest.json) and [`data/repositories.json`](data/repositories.json). Validate records against the published schema. Do not scrape this README when machine-readable data is available.", "",
        "## Limitations", "", "Star counts are popularity signals. Search indexing and GitHub API behavior can change. The collector fails closed when it cannot safely establish a complete eligible result set rather than publishing known-incomplete data.", "",
        "## Contributing", "", "See [`CONTRIBUTING.md`](CONTRIBUTING.md). Security issues should follow [`SECURITY.md`](SECURITY.md).", "",
        "## License", "", "Project code and documentation are MIT licensed. Upstream repository metadata remains subject to GitHub's terms and the respective repositories' licenses.", "", "---", "", "**RepoSource Registry** · Reliable data. Clear provenance. Stable schema. Simple consumption."
    ]
    (ROOT / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    started = datetime.now(timezone.utc)
    cfg = load_config()
    indexed_at = started.replace(microsecond=0).isoformat().replace("+00:00", "Z")
    session = github_session()
    previous = read_previous()
    raw: list[dict[str, Any]] = []
    collect_all(session, cfg, raw)
    dedup: dict[int, dict[str, Any]] = {}
    rejected = 0
    for repo in raw:
        if repo.get("fork") and not cfg["include_forks"]:
            rejected += 1
            continue
        if repo.get("archived") and not cfg["include_archived"]:
            rejected += 1
            continue
        if int(repo.get("stargazers_count", 0)) < int(cfg["min_stars"]):
            rejected += 1
            continue
        normalized = normalize(repo, indexed_at, cfg)
        normalized = classify(normalized, cfg, started)
        dedup[int(normalized["repository_id"])] = normalized
    records = list(dedup.values())
    validate_records(records, cfg)
    changes = compute_changes(previous, records)
    duration = (datetime.now(timezone.utc) - started).total_seconds()
    stats = {
        "generated_at": indexed_at,
        "minimum_stars": cfg["min_stars"],
        "records_fetched": len(raw),
        "records_accepted": len(records),
        "records_rejected": rejected,
        "duplicates_removed": max(0, len(raw) - rejected - len(records)),
    }
    sync_meta = {
        "sync_id": str(uuid.uuid4()),
        "started_at": indexed_at,
        "finished_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "duration_seconds": round(duration, 3),
        "source_api": API_URL,
        "minimum_stars": cfg["min_stars"],
        "dataset_version": cfg["dataset_version"],
        "schema_version": cfg.get("schema_version", "1.1.0"),
        "fetched": len(raw),
        "accepted": len(records),
        "rejected": rejected,
        "duplicates": stats["duplicates_removed"],
        "added": changes["summary"]["added"],
        "removed": changes["summary"]["removed"],
        "changed": changes["summary"]["changed"],
        "failure_count": 0,
    }
    write_outputs(records, cfg, stats, changes, sync_meta)
    print(json.dumps({**sync_meta, "repository_count": len(records)}, indent=2))


if __name__ == "__main__":
    main()
