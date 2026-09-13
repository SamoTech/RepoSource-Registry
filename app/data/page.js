import { DatasetStructuredData } from "../seo-schema";
import { getStats } from "../../lib/registry";

export const metadata = {
  title: "GitHub Repository Dataset",
  description: "Open, machine-readable GitHub repository discovery dataset with provenance, schema, snapshot metadata, and direct public access.",
  alternates: { canonical: "https://repo-source-registry.vercel.app/data" },
};

export default async function DataPage() {
  const stats = await getStats();
  const resources = [
    ["Canonical dataset", "Primary machine-readable repository snapshot.", "https://github.com/SamoTech/RepoSource-Registry/blob/main/data/repositories.json"],
    ["CSV export", "Tabular export for spreadsheet and ETL workflows.", "https://github.com/SamoTech/RepoSource-Registry/blob/main/data/repositories.csv"],
    ["Schema", "JSON Schema for repository records.", "https://github.com/SamoTech/RepoSource-Registry/blob/main/schema/repository.schema.json"],
    ["Manifest", "Snapshot identity, versions, provenance, and integrity hashes.", "https://github.com/SamoTech/RepoSource-Registry/blob/main/data/manifest.json"],
    ["Statistics", "Aggregate counts and distributions for the snapshot.", "https://github.com/SamoTech/RepoSource-Registry/blob/main/data/statistics.json"],
    ["Changes", "Snapshot-to-snapshot change information when published.", "https://github.com/SamoTech/RepoSource-Registry/blob/main/data/changes.json"],
    ["Sync audit", "Synchronization metadata for the published snapshot.", "https://github.com/SamoTech/RepoSource-Registry/blob/main/data/sync.json"],
    ["Dataset metadata", "Scope, provenance, licensing, and distribution metadata.", "https://github.com/SamoTech/RepoSource-Registry/blob/main/dataset.json"],
    ["Methodology", "Collection, normalization, validation, and limitations.", "https://github.com/SamoTech/RepoSource-Registry/blob/main/docs/methodology.md"],
    ["Data dictionary", "Definitions for fields exposed by the registry.", "https://github.com/SamoTech/RepoSource-Registry/blob/main/docs/data-dictionary.md"],
    ["Agent orientation", "Machine-readable guidance for automated consumers.", "https://github.com/SamoTech/RepoSource-Registry/blob/main/llms.txt"],
  ];

  return <div className="shell page">
    <DatasetStructuredData stats={stats} />
    <div className="section-kicker">PUBLIC DATA / ACCESS</div>
    <div className="page-heading"><div><h1>Dataset & provenance</h1><p className="lead small">The website is a discovery layer. The public dataset remains directly accessible from GitHub without an account, payment, or API key.</p></div><div className="page-counter"><strong>1.0.0</strong><span>dataset version</span></div></div>

    <div className="data-summary"><div><span>REPOSITORIES</span><strong>{stats.repository_count.toLocaleString()}</strong><small>accepted records</small></div><div><span>GENERATED</span><strong>{stats.generated_at}</strong><small>UTC snapshot</small></div><div><span>SCHEMA</span><strong>1.1.0</strong><small>repository schema</small></div></div>

    <section className="access-panel"><div><span className="section-kicker">CANONICAL ACCESS</span><h2>Everything needed to consume the data.</h2><p>Use the canonical files for analysis, indexing, research, and downstream tooling. Each repository record retains an upstream GitHub reference. Supporting artifacts describe the same snapshot; they do not replace the canonical dataset.</p></div><div className="access-grid">{resources.map(([title, desc, url], index) => <a className="resource" href={url} key={title} rel="noreferrer"><span className="resource-index">{String(index + 1).padStart(2, "0")}</span><strong>{title}</strong><span>{desc}</span><small>{url.replace("https://github.com/SamoTech/RepoSource-Registry/blob/main/", "")}</small><b aria-hidden="true">↗</b></a>)}</div></section>

    <section className="detail-note provenance-note"><span className="section-kicker">TRUST MODEL</span><strong>GitHub source → collection → normalization → validation → snapshot → public data → upstream verification.</strong><p>RepoSource Registry is a secondary snapshot. Stars, descriptions, topics, and other mutable values may differ from current GitHub state. Stars indicate popularity, not quality, security, or endorsement.</p></section>
  </div>;
}
