import { getStats } from "../../lib/registry";

export const metadata = { title: "Dataset", description: "RepoSource Registry public dataset, provenance, schema, and access points." };

export default async function DataPage() {
  const stats = await getStats();
  const resources = [
    ["Canonical dataset", "The authoritative RepoSource Registry snapshot.", "https://github.com/SamoTech/RepoSource-Registry/blob/main/data/repositories.json"],
    ["Schema", "JSON Schema for repository records.", "https://github.com/SamoTech/RepoSource-Registry/blob/main/schema/repository.schema.json"],
    ["Manifest", "Snapshot identity, versions, provenance, and hashes.", "https://github.com/SamoTech/RepoSource-Registry/blob/main/data/manifest.json"],
    ["Statistics", "Aggregate dataset statistics.", "https://github.com/SamoTech/RepoSource-Registry/blob/main/data/statistics.json"],
    ["Methodology", "Collection, normalization, validation, and limitations.", "https://github.com/SamoTech/RepoSource-Registry/blob/main/docs/methodology.md"],
    ["Data dictionary", "Definitions for fields exposed by the registry.", "https://github.com/SamoTech/RepoSource-Registry/blob/main/docs/data-dictionary.md"],
    ["Agent orientation", "Compact guidance for automated consumers.", "https://github.com/SamoTech/RepoSource-Registry/blob/main/llms.txt"],
  ];
  return <div className="shell page"><div className="section-kicker">PUBLIC DATA</div><h1>Dataset & provenance</h1><p className="lead small">The web interface is a convenience layer. The public dataset remains directly accessible from GitHub without an account or payment.</p>
    <div className="data-summary"><div><span>Repositories</span><strong>{stats.repository_count.toLocaleString()}</strong></div><div><span>Generated</span><strong>{stats.generated_at}</strong></div><div><span>Minimum stars</span><strong>{stats.minimum_stars.toLocaleString()}+</strong></div></div>
    <div className="resource-list">{resources.map(([title, desc, url]) => <a className="resource" href={url} key={title}><strong>{title}</strong><span>{desc}</span><small>{url.replace("https://github.com/SamoTech/RepoSource-Registry/blob/main/", "")}</small></a>)}</div>
    <section className="detail-note"><strong>Trust model</strong><p>GitHub source → collection → normalization → validation → snapshot → public data → downstream use → upstream verification.</p><p>RepoSource Registry is a secondary snapshot. Stars, descriptions, topics, and other mutable values may differ from current GitHub state.</p></section>
  </div>;
}
