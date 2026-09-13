import Link from "next/link";
import { getStats } from "../../lib/registry";

const siteUrl = "https://repo-source-registry.vercel.app";
const githubBase = "https://github.com/SamoTech/RepoSource-Registry/blob/main/";

export const revalidate = 3600;
export const metadata = {
  title: "Research and reproducibility",
  description: "Use RepoSource Registry snapshots for reproducible GitHub repository metadata analysis.",
  alternates: { canonical: `${siteUrl}/research` },
};

export default async function ResearchPage() {
  const stats = await getStats();
  return <div className="shell page">
    <div className="section-kicker">RESEARCH / REPRODUCIBILITY</div>
    <div className="page-heading"><div><h1>Research from a documented snapshot.</h1><p className="lead small">RepoSource Registry is a secondary, versioned view of public GitHub repository metadata. Use the exact snapshot, record assumptions, and verify consequential claims upstream.</p></div><div className="page-counter"><strong>{stats.repository_count.toLocaleString()}</strong><span>records in current snapshot</span></div></div>

    <section className="section two-col">
      <div><div className="section-kicker">CURRENT SNAPSHOT</div><h2>Record the dataset before analysis.</h2><p>Identify the snapshot timestamp, dataset version, schema version, and canonical data file used by the analysis.</p><dl className="facts"><div><dt>Generated</dt><dd>{stats.generated_at}</dd></div><div><dt>Dataset version</dt><dd>{stats.dataset_version || "1.0.0"}</dd></div><div><dt>Schema version</dt><dd>{stats.schema_version || "1.1.0"}</dd></div><div><dt>Minimum stars</dt><dd>{Number(stats.minimum_stars).toLocaleString()}+</dd></div></dl></div>
      <div className="panel"><div className="section-kicker">REPRODUCIBLE WORKFLOW</div><div className="provenance">{['Snapshot','Verify hash','Load','Analyze','Record assumptions','Publish'].map((step, index) => <span key={step}><i>{String(index + 1).padStart(2, "0")}</i>{step}</span>)}</div></div>
    </section>

    <section className="section data-strip"><div className="section-kicker">RESEARCH QUESTIONS</div><div className="data-strip-grid"><div><strong>Language ecosystems</strong><span>Compare declared primary-language distributions above the inclusion threshold.</span></div><div><strong>Popularity distribution</strong><span>Study star-band concentration without treating stars as quality or security measures.</span></div><div><strong>Metadata completeness</strong><span>Measure missing descriptions, languages, topics, and other optional fields.</span></div></div></section>

    <section className="section callout"><div><div className="section-kicker">SOURCE DISCIPLINE</div><h2>RepoSource is evidence, not upstream authority.</h2><p>GitHub remains the primary source for current repository facts. Search semantics, changing metadata, the star threshold, and snapshot timing constrain inference.</p></div><div className="actions"><Link className="button" href="/data">Inspect data</Link><a className="button secondary" href={`${githubBase}docs/research.md`} rel="noreferrer">Research methodology ↗</a></div></section>

    <section className="section"><div className="section-kicker">REPRODUCIBILITY KIT</div><div className="access-grid">
      <a className="resource" href="https://github.com/SamoTech/RepoSource-Registry/blob/main/data/repositories.json" rel="noreferrer"><span className="resource-index">01</span><strong>Canonical dataset</strong><span>Primary repository snapshot.</span><small>data/repositories.json</small><b>↗</b></a>
      <a className="resource" href="https://github.com/SamoTech/RepoSource-Registry/blob/main/data/manifest.json" rel="noreferrer"><span className="resource-index">02</span><strong>Manifest</strong><span>Snapshot identity and integrity hashes.</span><small>data/manifest.json</small><b>↗</b></a>
      <a className="resource" href="https://github.com/SamoTech/RepoSource-Registry/blob/main/schema/repository.schema.json" rel="noreferrer"><span className="resource-index">03</span><strong>Schema</strong><span>Machine-readable record contract.</span><small>schema/repository.schema.json</small><b>↗</b></a>
      <a className="resource" href="https://github.com/SamoTech/RepoSource-Registry/blob/main/docs/citation.md" rel="noreferrer"><span className="resource-index">04</span><strong>Citation guidance</strong><span>Identify the exact snapshot in published work.</span><small>docs/citation.md</small><b>↗</b></a>
    </div></section>
    <p className="disclaimer">Registry values are snapshot values. Cite the snapshot used and verify consequential current facts against GitHub.</p>
  </div>;
}
