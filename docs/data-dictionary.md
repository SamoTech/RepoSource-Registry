# RepoSource Registry Data Dictionary

Field definitions are derived from [`schema/repository.schema.json`](../schema/repository.schema.json).

| Field | Type | Required | Meaning |
|---|---|---|---|
| `repository_id` | integer | yes | GitHub repository numeric identifier. |
| `full_name` | string | yes | Canonical `owner/repository` identity. |
| `owner` | string or null | no | GitHub owner login. |
| `name` | string or null | no | Repository name. |
| `html_url` | URI | yes | Canonical GitHub repository URL. |
| `api_url` | URI or null | no | GitHub API repository URL. |
| `description` | string | yes | Repository description; empty when absent. |
| `stars` | integer | yes | GitHub stargazer count at indexing time. |
| `forks` | integer | yes | GitHub fork count at indexing time. |
| `watchers` | integer | yes | GitHub watcher/subscriber count at indexing time. |
| `open_issues` | integer | yes | GitHub open issue count at indexing time. |
| `primary_language` | string or null | no | GitHub-declared primary language. |
| `topics` | array | yes | GitHub topics, normalized and deduplicated. |
| `license` | string or null | no | GitHub-reported license identifier when available. |
| `default_branch` | string or null | no | Default branch name. |
| `archived` | boolean | yes | Whether GitHub marks the repository archived. |
| `fork` | boolean | yes | Whether GitHub marks the repository as a fork. |
| `created_at` | date-time or null | no | Repository creation timestamp. |
| `updated_at` | date-time or null | no | Repository metadata update timestamp. |
| `pushed_at` | date-time or null | no | Most recent push timestamp when available. |
| `indexed_at` | date-time | yes | RepoSource synchronization timestamp. |
| `source_updated_at` | date-time or null | no | Source update timestamp copied from GitHub metadata. |
| `source` | constant | yes | `github-public-api`. |
| `dataset_version` | string | yes | RepoSource dataset contract version. |
| `schema_version` | string | yes | Repository record schema version. |
| `categories` | array | yes | RepoSource-derived topic categories. |
| `popularity_band` | enum | yes | RepoSource-derived star band. |
| `activity_status` | enum | yes | RepoSource-derived recent-push activity classification. |

`categories`, `popularity_band`, and `activity_status` are derived by RepoSource and must not be presented as GitHub-native fields.
