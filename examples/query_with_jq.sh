#!/usr/bin/env bash
set -euo pipefail

# Examples: filter the canonical JSON without downloading a new GitHub dataset.
# Top repositories with at least 50,000 stars:
jq -r '.repositories[] | select(.stars >= 50000) | [.full_name, .stars, (.primary_language // "No declared language"), .html_url] | @tsv' data/repositories.json

# Python repositories with at least 10,000 stars:
jq -r '.repositories[] | select(.primary_language == "Python" and .stars >= 10000) | [.full_name, .stars, .html_url] | @tsv' data/repositories.json
