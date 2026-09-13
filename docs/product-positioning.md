# RepoSource Registry: product positioning

## Current product

RepoSource Registry is a public, machine-readable discovery dataset of GitHub repositories meeting the configured `stars >= 2000` inclusion policy. It turns mutable GitHub Search results into a documented snapshot with a stable schema, derived discovery partitions, validation, provenance, and integrity metadata.

## Problem

GitHub Search is excellent for interactive discovery, but many applications need a reproducible dataset they can download, inspect, filter, validate, and process without implementing the collection and pagination logic themselves.

## Target users

- Developers building repository discovery and recommendation tools.
- AI and RAG developers that need structured repository metadata.
- Researchers and data scientists studying open-source ecosystems.
- Developer-tool companies building catalogs, integrations, and intelligence products.
- Open-source maintainers who need ecosystem discovery data.

## Differentiator

The useful product is not simply the list of repositories. It is the combination of a public snapshot, explicit provenance, a versioned schema, deterministic output, derived indexes, integrity hashes, and documented limitations.

## Why users can return

The recurring value is the weekly snapshot and the change history: users can compare ecosystem state over time without rebuilding the collection process themselves.

## Sponsorship rationale

A sponsor is funding maintenance of open data infrastructure: collection reliability, validation, documentation, discoverability, historical snapshots, and future interoperability. Sponsorship should support the public resource rather than buy preferential treatment in the registry.

## Commercial extensions

Potential future products include a higher-volume API, historical snapshots, change alerts, trend analysis, repository similarity, enterprise exports, and custom integrations. These are future opportunities, not current product claims.

## Validation status

Current value is supported by the published dataset, schema, generation workflow, tests, manifest, and discovery artifacts. Demand for future paid products must be validated through actual users before substantial infrastructure is built.
