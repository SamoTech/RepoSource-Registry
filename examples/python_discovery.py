from __future__ import annotations

import json
from pathlib import Path

DATASET = Path(__file__).resolve().parents[1] / "data" / "repositories.json"

with DATASET.open(encoding="utf-8") as handle:
    data = json.load(handle)

repositories = data["repositories"]

# Example: discover Python repositories with at least 10,000 stars.
results = [
    repo
    for repo in repositories
    if repo.get("primary_language") == "Python" and repo.get("stars", 0) >= 10_000
]

for repo in results[:20]:
    print(f"{repo['full_name']}: {repo['stars']:,} stars — {repo['html_url']}")

print(f"Matched {len(results):,} repositories")
