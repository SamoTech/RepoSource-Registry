# Product positioning

## Current verified value

RepoSource Registry is an open, machine-readable GitHub repository discovery dataset and public data infrastructure layer. The current published snapshot contains 33,180 public repositories meeting the configured `stars >= 2,000` inclusion policy.

The project converts upstream GitHub repository Search results into a documented snapshot with normalized records, a versioned schema, focused partitions, validation, provenance, integrity metadata, and change information.

## Problem

GitHub Search is effective for interactive upstream discovery. A downstream application or research workflow may instead need a reproducible snapshot that can be downloaded, inspected, filtered, tested, cited, and processed locally without rebuilding the same collection and normalization layer.

## Target users

- Developers building repository discovery, catalog, or recommendation tools.
- AI/data developers using structured repository metadata in retrieval and analysis workflows.
- Researchers and data scientists studying open-source ecosystems.
- Developer-tool and infrastructure teams building downstream products.
- Open-source maintainers and technical researchers who need structured discovery data.

## Solution

RepoSource publishes the discovery result as open data with explicit scope and source provenance. The canonical registry, schema, manifest, statistics, partitions, and methodology let downstream users inspect what was collected and how it should be interpreted.

## Differentiator

The differentiation is the reusable, reproducible data layer—not a claim to replace GitHub Search. RepoSource combines:

- a public snapshot;
- normalized machine-readable records;
- a versioned schema;
- deterministic derived fields;
- focused language and category partitions;
- validation and duplicate checks;
- manifest hashes and synchronization metadata;
- documented methodology and limitations.

## Why developers may use it

A developer can clone the repository and query the canonical JSON locally with standard tools. Focused partitions reduce the need to scan the full dataset for common discovery tasks.

## Why researchers may use it

The snapshot, version metadata, provenance, and change artifacts provide a clearer basis for reproducible analysis than an undocumented point-in-time search result.

## Why AI/data applications may use it

The project exposes an explicit data contract, machine-readable metadata, canonical paths, provenance, and agent-oriented orientation. Downstream systems can consume structured records while retaining the upstream GitHub URL for verification.

## Why contributors may improve it

The project has a concrete public data contract. Improvements to validation, documentation, examples, interoperability, and reproducibility benefit every downstream consumer without requiring contributors to operate a hosted service.

## Why companies may sponsor it

A company can fund maintenance of reusable public infrastructure it finds useful or wants the ecosystem to have. Sponsorship supports the project; it does not purchase influence over repository inclusion, ranking, classification, or suppression.

## Future potential

Future commercial opportunities are intentionally outside the canonical dataset: professional integration, custom data engineering, research, analytical work, hosted discovery experiences, and organization-specific implementations. These are potential services, not validated market demand.

## Strategic boundary

The public dataset remains open and useful on its own. Revenue must come from sponsorship, expertise, implementation, customization, research, analytics, or hosted experiences—not from artificially restricting the underlying public data.
