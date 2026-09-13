# Quick start

RepoSource Registry can be consumed without an API key. The public snapshot is distributed as JSON and CSV; the JSON dataset is the canonical source.

## 1. Download the canonical dataset

```bash
curl -L https://raw.githubusercontent.com/SamoTech/RepoSource-Registry/main/data/repositories.json -o repositories.json
```

## 2. Inspect the snapshot

```bash
python - <<'PY'
import json

with open("repositories.json", encoding="utf-8") as f:
    dataset = json.load(f)

print("repositories:", dataset["repository_count"])
print("version:", dataset["dataset_version"])
print("generated:", dataset["generated_at"])
PY
```

## 3. Find popular Python repositories

```python
import json

with open("repositories.json", encoding="utf-8") as f:
    records = json.load(f)["repositories"]

for repo in records:
    if repo.get("primary_language") == "Python":
        print(repo["full_name"], repo["stars"], repo["html_url"])
```

## 4. Use the smaller indexes

Language partitions are available under `data/languages/` and category partitions under `data/categories/`. Use these when you need a focused subset rather than loading the approximately 40 MB canonical JSON file.

Example:

```bash
python - <<'PY'
import json

with open("data/languages/python.json", encoding="utf-8") as f:
    data = json.load(f)

for repo in data["repositories"][:20]:
    print(repo["full_name"], repo["stars"])
PY
```

## 5. Query with jq

```bash
jq '.repositories[] | select(.stars >= 10000) | [.full_name, .stars, .primary_language] | @tsv' data/repositories.json
```

## 6. Verify the contract

Read `schema/repository.schema.json` before building a long-lived integration. Use `data/manifest.json` to identify the snapshot and verify published SHA-256 hashes when integrity matters.

## 7. Cite correctly

Use the snapshot timestamp in `data/manifest.json` or `data/statistics.json`, identify the dataset version, and use each record's `html_url` as the upstream reference for an individual repository.

## What this is not

The registry is not a real-time API, a complete mirror of GitHub, or a quality/security ranking. Important facts about an individual repository should be verified against GitHub itself.
