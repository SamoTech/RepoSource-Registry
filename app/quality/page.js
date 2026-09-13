import Link from "next/link";
import { getStats } from "../../lib/registry";

const siteUrl = "https://repo-source-registry.vercel.app";

export const revalidate = 3600;
export const metadata = {
  title: "Data quality and validation",
  description: "Snapshot-level quality metrics, validation signals, and limitations for RepoSource Registry.",
  alternates: { canonical: `${siteUrl}/quality` },
};

function pct(part, total) {
  const value = Number(total) > 0 ? (Number(part) / Number(total)) * 100 : 0;
  return `${value.toFixed(1)}%`;
}

export default async function QualityPage() {
  const stats = await getStats();
  const total = Number(stats.repository_count) || 0;
  const accepted = Number(stats.records_accepted) || 0;
  const rejected = Number(stats.records_rejected) || 0;
  const duplicates = Number(stats.duplicates_removed) || 0;
  const archived = Number(stats.archived_repositories) || 0;
  const noLanguage = Number(stats.no_primary_language) || 0;
  const noDescription = Number(stats.no_description) || 0;

  const checks = [
    ["Records accepted", `${accepted.toLocaleString()} / ${total.toLocaleString()}`, pct(accepted, total)],
    ["Records rejected", rejected.toLocaleString(), pct(rejected, total)],
    ["Duplicates removed", duplicates.toLocaleString(), pct(duplicates, total)],
    ["Archived repositories", archived.toLocaleString(), pct(archived, total)],
    ["No primary language", noLanguage.toLocaleString(), pct(noLanguage, total)],
    ["No description", noDescription.toLocaleString(), pct(noDescription, total)],
  ];

  return <div className="shell page">
    <div className="section-kicker">QUALITY / VALIDATION</div>
    <div className="page-heading">
      <div>
        <h1>Data quality you can inspect.</h1>
        <p className="lead small">A snapshot-level view of acceptance, missingness, and validation signals. These metrics describe the published registry snapshot; they are not a live assessment of GitHub.</p>
      </div>
      <div className="page-counter"><strong>{total.toLocaleString()}</strong><span>records in snapshot</span></div>
    </div>

    <section className="section two-col">
      <div>
        <div className="section-kicker">SNAPSHOT IDENTITY</div>
        <h2>Quality is tied to a specific publication.</h2>
        <dl className="facts">
          <div><dt>Generated</dt><dd>{stats.generated_at}</dd></div>
          <div><dt>Minimum stars</dt><dd>{Number(stats.minimum_stars).toLocaleString()}+</dd></div>
          <div><dt>Star median</dt><dd>{Number(stats.star_distribution?.median || 0).toLocaleString()}</dd></div>
          <div><dt>Star maximum</dt><dd>{Number(stats.star_distribution?.maximum || 0).toLocaleString()}</dd></div>
        </dl>
      </div>
      <div className="panel">
        <div className="section-kicker">VALIDATION SIGNALS</div>
        <div className="provenance">
          {[
            ["01", "Collection"],
            ["02", "Normalization"],
            ["03", "Validation"],
            ["04", "Snapshot"],
            ["05", "Publication"],
          ].map(([number, label]) => <span key={label}><i>{number}</i>{label}</span>)}
        </div>
      </div>
    </section>

    <section className="section">
      <div className="section-kicker">PUBLISHED METRICS</div>
      <div className="data-strip-grid">
        {checks.map(([label, value, rate]) => <div key={label}><strong>{label}</strong><span>{value}</span><small>{rate} of snapshot records</small></div>)}
      </div>
    </section>

    <section className="section callout">
      <div>
        <div className="section-kicker">INTERPRETATION</div>
        <h2>Missing metadata is reported, not silently repaired.</h2>
        <p>Repository descriptions, language values, stars, and derived classifications can change or be incomplete upstream. RepoSource preserves the published snapshot and its missingness rather than inventing values. For consequential current facts, verify the upstream GitHub repository.</p>
      </div>
      <div className="actions">
        <Link className="button" href="/data">Inspect data</Link>
        <a className="button secondary" href="https://github.com/SamoTech/RepoSource-Registry/blob/main/docs/data-quality.md" rel="noreferrer">Quality methodology ↗</a>
      </div>
    </section>

    <section className="section data-strip">
      <div className="section-kicker">TRUST BOUNDARY</div>
      <div className="data-strip-grid">
        <div><strong>GitHub is upstream</strong><span>RepoSource is a structured secondary snapshot, not live GitHub state.</span></div>
        <div><strong>Metrics are snapshot-scoped</strong><span>Quality values describe the generated timestamp shown above.</span></div>
        <div><strong>Validation is explicit</strong><span>Use the manifest, schema, tests, and published artifacts to reproduce the data contract.</span></div>
      </div>
    </section>

    <p className="disclaimer">Snapshot: {stats.generated_at}. See the canonical manifest and quality documentation for reproducibility details.</p>
  </div>;
}
