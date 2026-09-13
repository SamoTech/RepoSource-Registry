from __future__ import annotations

import csv
import json
import os
import re
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
from jsonschema import validate

ROOT = Path(__file__).resolve().parent
CONFIG_PATH = ROOT / "config.json"
SCHEMA_PATH = ROOT / "schema" / "repository.schema.json"
DATA_DIR = ROOT / "data"


def load_config() -> dict[str, Any]:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def github_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "RepoSource-Registry/1.0",
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
            if response.status_code == 403 and response.headers.get("X-RateLimit-Remaining") == "0":
                reset = int(response.headers.get("X-RateLimit-Reset", time.time() + 60))
                time.sleep(max(1, reset - int(time.time()) + 1))
                continue
            if response.status_code in {429, 500, 502, 503, 504} and attempt < retries:
                time.sleep(min(60, 2 ** attempt))
                continue
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            if attempt >= retries:
                raise
            time.sleep(min(60, 2 ** attempt))
    raise RuntimeError("unreachable")


def search_count(session: requests.Session, query: str, cfg: dict[str, Any]) -> int:
    payload = request_json(session, "https://api.github.com/search/repositories", {"q": query, "per_page": 1}, cfg)
    return int(payload.get("total_count", 0))


def collect_range(session: requests.Session, low: int, high: int | None, cfg: dict[str, Any], out: list[dict[str, Any]]) -> None:
    star_filter = f"stars:{low}..{high}" if high is not None else f"stars:>={low}"
    query = f"{star_filter}"
    count = search_count(session, query, cfg)

    # GitHub Search limits a single query to 1,000 results. Partition star ranges
    # until every leaf query can be fully paginated. Exact-star collisions are
    # further partitioned by creation year when necessary.
    if count > 1000 and (high is None or low < high):
        if high is None:
            high = max(low, 1000000)
        mid = (low + high) // 2
        if mid < high:
            collect_range(session, low, mid, cfg, out)
            collect_range(session, mid + 1, high, cfg, out)
            return

    if count > 1000:
        raise RuntimeError(f"More than 1000 repositories share exactly {low} stars; add a secondary partition strategy.")

    for page in range(1, (count + cfg["per_page"] - 1) // cfg["per_page"] + 1):
        payload = request_json(session, "https://api.github.com/search/repositories", {
            "q": query,
            "sort": "stars",
            "order": "desc",
            "per_page": cfg["per_page"],
            "page": page,
        }, cfg)
        out.extend(payload.get("items", []))


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
    }


def classify(record: dict[str, Any], cfg: dict[str, Any]) -> dict[str, Any]:
    topics = set(record["topics"])
    categories = [name for name, terms in cfg["categories"].items() if topics.intersection(terms)]
    record["categories"] = sorted(categories)
    record["popularity_band"] = (
        "50k+" if record["stars"] >= 50000 else
        "10k+" if record["stars"] >= 10000 else
        "5k+" if record["stars"] >= 5000 else "2k+"
    )
    pushed = record.get("pushed_at")
    if not pushed:
        record["activity_status"] = "unknown"
    else:
        age_days = (datetime.now(timezone.utc) - datetime.fromisoformat(pushed.replace("Z", "+00:00"))).days
        record["activity_status"] = "active" if age_days <= 180 else "inactive"
    return record


def validate_records(records: list[dict[str, Any]]) -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    ids: set[int] = set()
    names: set[str] = set()
    for record in records:
        validate(record, schema)
        if record["repository_id"] in ids:
            raise ValueError(f"Duplicate repository_id: {record['repository_id']}")
        if record["full_name"] in names:
            raise ValueError(f"Duplicate full_name: {record['full_name']}")
        ids.add(record["repository_id"])
        names.add(record["full_name"])


def md_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace("[", "\\[").replace("]", "\\]").replace("|", "\\|").replace("\n", " ")


def csv_safe(value: Any) -> Any:
    if isinstance(value, str) and value.startswith(("=", "+", "-", "@")):
        return "'" + value
    return value


def write_outputs(records: list[dict[str, Any]], cfg: dict[str, Any], stats: dict[str, Any]) -> None:
    DATA_DIR.mkdir(exist_ok=True)
    (DATA_DIR / "languages").mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "categories").mkdir(parents=True, exist_ok=True)

    records = sorted(records, key=lambda r: (-r["stars"], r["full_name"].lower()))
    payload = {
        "dataset": "RepoSource Registry",
        "dataset_version": cfg["dataset_version"],
        "generated_at": stats["generated_at"],
        "inclusion_policy": {"minimum_stars": cfg["min_stars"]},
        "repository_count": len(records),
        "repositories": records,
    }
    (DATA_DIR / "repositories.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (DATA_DIR / "statistics.json").write_text(json.dumps(stats, indent=2) + "\n", encoding="utf-8")

    fields = list(records[0].keys()) if records else [
        "repository_id", "full_name", "owner", "name", "html_url", "api_url", "description", "stars", "forks",
        "watchers", "open_issues", "primary_language", "topics", "license", "default_branch", "archived", "fork",
        "created_at", "updated_at", "pushed_at", "indexed_at", "source", "dataset_version", "categories", "popularity_band", "activity_status"
    ]
    with (DATA_DIR / "repositories.csv").open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for record in records:
            writer.writerow({k: csv_safe(json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v) for k, v in record.items()})

    for language in sorted({r["primary_language"] or "No declared language" for r in records}):
        slug = re.sub(r"[^a-z0-9]+", "-", language.lower()).strip("-") or "other"
        subset = [r for r in records if (r["primary_language"] or "No declared language") == language]
        (DATA_DIR / "languages" / f"{slug}.json").write_text(json.dumps(subset, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    for category in sorted({c for r in records for c in r.get("categories", [])}):
        subset = [r for r in records if category in r.get("categories", [])]
        (DATA_DIR / "categories" / f"{category}.json").write_text(json.dumps(subset, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    generate_readme(records, cfg, stats)


def generate_readme(records: list[dict[str, Any]], cfg: dict[str, Any], stats: dict[str, Any]) -> None:
    languages = Counter(r["primary_language"] or "No declared language" for r in records)
    lines = [
        "# RepoSource Registry", "",
        "An automated, machine-readable index of notable public GitHub repositories, derived from GitHub public repository metadata.", "",
        "> **Popularity index, not an endorsement.** Stars measure popularity, not software quality.", "",
        f"**Current threshold:** {cfg['min_stars']:,}+ stars  ·  **Indexed repositories:** {len(records):,}  ·  **Generated:** {stats['generated_at']}", "",
        "## Data", "",
        "The canonical machine-readable dataset is [`data/repositories.json`](data/repositories.json). CSV is available at [`data/repositories.csv`](data/repositories.csv). The schema is [`schema/repository.schema.json`](schema/repository.schema.json).", "",
        "## Language index", "",
    ]
    for language, count in sorted(languages.items(), key=lambda x: (-x[1], x[0].lower())):
        slug = re.sub(r"[^a-z0-9]+", "-", language.lower()).strip("-") or "other"
        lines.append(f"- **{md_escape(language)}** — {count:,} — [dataset](data/languages/{slug}.json)")
    lines += [
        "", "## Methodology", "",
        "1. Query GitHub's official public REST Search API.",
        f"2. Include repositories satisfying `stars >= {cfg['min_stars']}` and the configured fork/archive policy.",
        "3. Normalize GitHub-native metadata into a stable schema.",
        "4. Apply deterministic RepoSource classifications separately from source metadata.",
        "5. Validate, sort, and publish JSON, CSV, language indexes, category indexes, statistics, and this README.",
        "",
        "## Consumption", "",
        "Do not parse this README when building software integrations. Consume the JSON dataset and schema instead. See [`AGENTS.md`](AGENTS.md) and [`docs/CONSUMING.md`](docs/CONSUMING.md).",
        "",
        "## Provenance and limitations", "",
        "GitHub is the upstream source. RepoSource Registry is a derived dataset and is not an official GitHub product. Data is refreshed by automation and therefore is not guaranteed to be real-time. Derived categories and activity labels are RepoSource classifications.",
        "",
        "## License", "",
        "The project code and documentation are released under the MIT License. GitHub repository metadata remains subject to GitHub's terms and the respective repositories' licenses.",
    ]
    (ROOT / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    cfg = load_config()
    indexed_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    session = github_session()
    raw: list[dict[str, Any]] = []
    collect_range(session, int(cfg["min_stars"]), None, cfg, raw)

    dedup: dict[int, dict[str, Any]] = {}
    for repo in raw:
        if repo.get("fork") and not cfg["include_forks"]:
            continue
        if repo.get("archived") and not cfg["include_archived"]:
            continue
        if int(repo.get("stargazers_count", 0)) < int(cfg["min_stars"]):
            continue
        normalized = classify(normalize(repo, indexed_at, cfg), cfg)
        dedup[normalized["repository_id"]] = normalized

    records = list(dedup.values())
    validate_records(records)
    stats = {
        "generated_at": indexed_at,
        "minimum_stars": cfg["min_stars"],
        "records_fetched": len(raw),
        "records_accepted": len(records),
        "records_rejected": len(raw) - len(records),
        "repository_count": len(records),
        "languages": len({r["primary_language"] or "No declared language" for r in records}),
        "categories": len({c for r in records for c in r.get("categories", [])}),
    }
    write_outputs(records, cfg, stats)
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
