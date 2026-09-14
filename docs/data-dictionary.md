# RepoSource Registry Data Dictionary

Field definitions are derived from [`schema/repository.schema.json`](../schema/repository.schema.json).

| Field | Type | Required | Meaning |
|---|---|---|---|
| `repository_id` | `integer` | yes | GitHub repository numeric identifier. |
| `full_name` | `string` | yes | Canonical `owner/repository` identity. |
| `owner` | `string \| null` | no | GitHub owner login. |
| `name` | `string \| null` | no | Repository name. |
| `html_url` | `string` | yes | Canonical GitHub repository URL. |
| `api_url` | `string \| null` | no | GitHub API repository URL. |
| `description` | `string` | no | Repository description; empty string when absent. |
| `stars` | `integer` | yes | GitHub stargazer count at indexing time. |
| `forks` | `integer` | no | GitHub fork count at indexing time. |
| `watchers` | `integer` | no | GitHub watcher/subscriber count at indexing time. |
| `open_issues` | `integer` | no | GitHub open issue count at indexing time. |
| `primary_language` | `string \| null` | no | GitHub-declared primary language; nullable. |
| `topics` | `array` | yes | GitHub repository topics, normalized and deduplicated. |
| `license` | `string \| null` | no | GitHub-reported license identifier when available. |
| `default_branch` | `string \| null` | no | Default branch name. |
| `archived` | `boolean` | yes | Whether GitHub marks the repository archived. |
| `fork` | `boolean` | yes | Whether GitHub marks the repository as a fork. |
| `created_at` | `string \| null` | no | Repository creation timestamp. |
| `updated_at` | `string \| null` | no | GitHub repository metadata update timestamp. |
| `pushed_at` | `string \| null` | no | Most recent push timestamp when available. |
| `indexed_at` | `string` | yes | RepoSource synchronization timestamp. |
| `source_updated_at` | `string \| null` | no | Source repository update timestamp copied from GitHub metadata. |
| `source` | `constant `github-public-api`` | yes | Provenance identifier; currently `github-public-api`. |
| `dataset_version` | `string` | yes | RepoSource dataset contract version. |
| `schema_version` | `string` | no | Repository record schema version. |
| `categories` | `array` | yes | RepoSource-derived topic categories. |
| `popularity_band` | `enum` | yes | RepoSource-derived star band. |
| `activity_status` | `enum` | yes | RepoSource-derived recent-push activity classification. |

`categories`, `popularity_band`, and `activity_status` are derived by RepoSource and must not be presented as GitHub-native fields.
