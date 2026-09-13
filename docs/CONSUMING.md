# Consuming RepoSource Registry

The preferred integration target is `data/repositories.json`. Do not parse README.md as a data interface.

## JSON

```bash
curl -L https://raw.githubusercontent.com/SamoTech/RepoSource-Registry/main/data/repositories.json
```

The top-level object contains dataset metadata and a `repositories` array.

## Python

```python
import json
from urllib.request import urlopen

URL = "https://raw.githubusercontent.com/SamoTech/RepoSource-Registry/main/data/repositories.json"
with urlopen(URL, timeout=30) as response:
    payload = json.load(response)

for repo in payload["repositories"]:
    print(repo["full_name"], repo["stars"])
```

## JavaScript / TypeScript

```javascript
const response = await fetch(
  "https://raw.githubusercontent.com/SamoTech/RepoSource-Registry/main/data/repositories.json"
);
const payload = await response.json();
console.log(payload.repositories);
```

## CSV

Use `data/repositories.csv` for spreadsheet and simple analytical workflows. JSON remains the preferred machine interface because arrays such as topics and categories retain their structure.

## Schema and compatibility

Validate records against `schema/repository.schema.json`. The `dataset_version` field identifies the public data contract version. Consumers should tolerate new optional fields and should not assume that the repository count is fixed.

## Provenance

The registry is derived from GitHub public repository metadata. It is not an official GitHub dataset and should not be treated as authoritative for repository state at the instant of consumption.
