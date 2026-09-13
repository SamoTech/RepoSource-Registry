# First Users

RepoSource Registry should grow through real downstream utility, not artificial engagement.

This document defines practical, evidence-driven experiments for acquiring the first external users.

## 1. Repository-discovery developers

**Problem:** Developers building catalogs, discovery tools, or recommendation interfaces may need a reusable repository snapshot instead of rebuilding upstream search logic.

**RepoSource value:** A documented, normalized public dataset with schema, indexes, provenance, and a canonical JSON artifact.

**Discovery channels:** GitHub search/topics, developer communities, technical blogs, open-source discussions, and direct outreach to maintainers of relevant discovery tools.

**Example message:**

> I maintain RepoSource Registry, an open GitHub repository discovery dataset with a documented schema and reusable JSON/CSV artifacts. I built it for downstream tools that do not want to rebuild the same discovery and normalization layer. Would this be useful for your project?

**Genuine-interest signal:** The recipient tests the dataset, asks for a field/index, opens an issue, creates a fork, or builds a small integration.

**Feedback to collect:** Missing fields, useful filters, performance constraints, desired partitions, and reproducibility requirements.

## 2. AI/RAG developers

**Problem:** AI applications often need structured repository metadata for retrieval, recommendation, or ecosystem analysis.

**RepoSource value:** Machine-readable records, explicit provenance, schema, snapshot identity, and upstream GitHub links.

**Discovery channels:** AI developer communities, RAG examples, GitHub integrations, technical posts, and open-source agent projects.

**Example message:**

> RepoSource Registry publishes a structured snapshot of notable GitHub repositories with schema, provenance, and upstream URLs. It can be used as a retrieval dataset for repository discovery and AI/data workflows. I am looking for developers willing to test whether the public data fits a real use case.

**Genuine-interest signal:** A developer loads the dataset into a retrieval pipeline, requests integration guidance, reports a data issue, or publishes a downstream experiment.

**Feedback to collect:** Record shape, chunking/query needs, freshness requirements, and useful derived indexes.

## 3. Open-source researchers

**Problem:** Researchers studying GitHub ecosystems need reproducible repository metadata rather than undocumented ad-hoc queries.

**RepoSource value:** Snapshot timestamp, dataset version, schema, methodology, statistics, and change artifacts.

**Discovery channels:** Research communities, GitHub discussions, technical blogs, data-science communities, and citations in open research.

**Example message:**

> RepoSource Registry is an open, versioned snapshot of public GitHub repository metadata above the configured popularity threshold. It includes schema, provenance, statistics, and reproducibility documentation. I am interested in feedback from researchers who need a stable discovery dataset.

**Genuine-interest signal:** Reproduction of a result, citation, methodological feedback, or use in a research workflow.

**Feedback to collect:** Required historical context, schema clarity, citation needs, and snapshot/release expectations.

## 4. Language/topic tooling developers

**Problem:** Developer tools often need focused repository sets by language or topic.

**RepoSource value:** Language/category partitions and machine-readable canonical records.

**Discovery channels:** Language-specific communities, developer tooling repositories, topic communities, and integration examples.

**Example message:**

> RepoSource Registry publishes language and category-oriented repository partitions derived from a documented public GitHub snapshot. I am testing whether these partitions can simplify developer-tool discovery workflows without each project implementing its own collection layer.

**Genuine-interest signal:** A tool consumes a partition, requests a new useful index, or contributes an integration/example.

**Feedback to collect:** Partition naming, field needs, update expectations, and interoperability requirements.

## 5. Open-source tooling authors

**Problem:** CLI, catalog, portal, and automation projects may need a reusable repository discovery source.

**RepoSource value:** Public JSON/CSV, schema, metadata, deterministic ordering, and transparent limitations.

**Discovery channels:** Related GitHub repositories, package ecosystems, community forums, and maintainer-to-maintainer outreach.

**Example message:**

> I am maintaining RepoSource Registry as an open repository-data layer: canonical JSON, schema, indexes, provenance, and update metadata. I am looking for open-source tools that could consume it directly and provide feedback on what would make integration easier.

**Genuine-interest signal:** Actual downstream consumption, a pull request, issue feedback, or public integration.

**Feedback to collect:** SDK/CLI demand, stable paths, versioning expectations, and backward compatibility requirements.

## Principles

- Do not mass-contact unrelated users.
- Do not create fake accounts or engagement.
- Do not buy stars or reviews.
- Do not present hypothetical users as current users.
- Prefer a small number of relevant conversations over broad promotion.
- Treat downstream usage, citations, forks, integrations, and quality reports as stronger evidence than vanity metrics.

The goal of this document is to create measurable discovery experiments. It is not evidence that any of these audiences currently use RepoSource Registry.
