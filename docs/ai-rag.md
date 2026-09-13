# AI / RAG integration

RepoSource Registry provides structured repository metadata that can be useful as an input to retrieval, filtering, enrichment, and developer-discovery systems. It is data, not an AI model.

## Useful patterns

### Retrieval
Index repository descriptions, names, languages, topics, and other schema-supported fields. Keep the snapshot identity with each indexed record.

### Filtering
Use structured fields before semantic retrieval when a workflow needs deterministic constraints such as language, stars, category, or owner.

### Metadata enrichment
Use the registry to seed a discovery workflow, then verify important current facts against the upstream GitHub repository.

### RAG grounding
When a response is grounded in registry data, retain the snapshot timestamp and repository `html_url` so the downstream application can distinguish snapshot evidence from live upstream state.

## Minimal architecture

`PUBLIC DATASET → VALIDATION → INDEX → RETRIEVAL/FILTER → APPLICATION`

No RepoSource API is required. Consumers can work directly with the public JSON/CSV artifacts or focused partitions.

## Important limitations

The registry is a snapshot and uses the configured `stars >= 2,000` inclusion policy. It is not a complete mirror of GitHub. Missing metadata should remain missing. Stars are not a quality score. Do not describe RepoSource records as AI-verified or as official GitHub truth.

## Good downstream practice

- pin the dataset version;
- preserve snapshot timestamps;
- store the upstream repository URL;
- validate records against the published schema;
- keep derived embeddings/indexes separate from canonical source data;
- refresh deliberately when a newer snapshot is published.
