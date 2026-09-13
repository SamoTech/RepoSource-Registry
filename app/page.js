import Link from "next/link";
import { getStats } from "../lib/registry";

export const revalidate = 3600;

export default async function Home() {
  const stats = await getStats();
  const languages = Object.entries(stats.languages || {}).sort((a, b) => b[1] - a[1]).slice(0, 8);
  const categories = Object.entries(stats.categories || {}).sort((a, b) => b[1] - a[1]);
  const bands = [
    ["2k+", stats.star_bands?.["2k+"] || 0],
    ["5k+", stats.star_bands?.["5k+"] || 0],
    ["10k+", stats.star_bands?.["10k+"] || 0],
    ["50k+", stats.star_bands?.["50k+"] || 0],
  ];

  return (
    <div>
      <section className="hero shell">
        <div className="hero-grid">
          <div>
            <div className="eyebrow"><span className="signal-dot" /> OPEN DATA · REPOSITORY INDEX</div>
            <h1>Open-source discovery, indexed as data.</h1>
            <p className="lead">RepoSource Registry is an open, machine-readable snapshot of notable GitHub repositories for developers, researchers, and data tooling.</p>
            <div className="hero-actions">
              <Link href="/search" className="button">Discover repositories <span aria-hidden="true">→</span></Link>
              <Link href="/data" className="button secondary">Access the dataset</Link>
            </div>
            <p className="note">Snapshot data is secondary. Verify consequential current facts against the upstream GitHub repository.</p>
          </div>

          <aside className="instrument" aria-label="Registry calibration panel">
            <div className="instrument-top"><span>REGISTRY / CALIBRATION</span><b>LIVE SNAPSHOT</b></div>
            <div className="instrument-value"><strong>{stats.repository_count.toLocaleString()}</strong><span>indexed repositories</span></div>
            <div className="calibration" aria-hidden="true">
              <div className="calibration-track"><i /><i /><i /><i /></div>
              <div className="calibration-ticks"><span>2k°</span><span>5k°</span><span>10k°</span><span>50k°+</span></div>
            </div>
            <div className="instrument-foot"><span>STAR-BAND SCALE</span><span>SCHEMA {"1.1.0"}</span></div>
          </aside>
        </div>
      </section>

      <section className="shell stats" aria-label="Dataset statistics">
        <div><span className="metric-label">INDEXED</span><strong>{stats.repository_count.toLocaleString()}</strong><small>repositories</small></div>
        <div><span className="metric-label">LANGUAGES</span><strong>{Object.keys(stats.languages || {}).length}</strong><small>declared values</small></div>
        <div><span className="metric-label">CATEGORIES</span><strong>{Object.keys(stats.categories || {}).length}</strong><small>derived groups</small></div>
        <div><span className="metric-label">THRESHOLD</span><strong>{stats.minimum_stars.toLocaleString()}+</strong><small>minimum stars</small></div>
      </section>

      <section className="shell section two-col">
        <div>
          <div className="section-kicker">EXPLORE / LANGUAGES</div>
          <h2>Start with the ecosystems you know.</h2>
          <p>Jump directly into the largest language segments in the current published snapshot.</p>
          <div className="chips">{languages.map(([name, count]) => <Link key={name} href={`/search?language=${encodeURIComponent(name)}`} className="chip"><span>{name}</span><b>{count.toLocaleString()}</b></Link>)}</div>
        </div>
        <div className="panel">
          <div className="panel-heading"><div><span className="section-kicker">DISTRIBUTION</span><h3>Star bands</h3></div><span className="degree-mark">°</span></div>
          {bands.map(([name, count], index) => <div className="bar-row" key={name}><span><i className={`bar-swatch band-${index}`} />{name}</span><b>{count.toLocaleString()}</b></div>)}
        </div>
      </section>

      <section className="shell section data-strip">
        <div className="section-kicker">WHY IT EXISTS</div>
        <div className="data-strip-grid">
          <div><strong>Discover</strong><span>Find repositories by name, owner, language, category, or stars.</span></div>
          <div><strong>Download</strong><span>Use the canonical machine-readable snapshot directly from GitHub.</span></div>
          <div><strong>Verify</strong><span>Trace every repository back to its upstream GitHub source.</span></div>
        </div>
      </section>

      <section className="shell section callout">
        <div><div className="section-kicker">OPEN DATA / PROVENANCE</div><h2>GitHub is the source. RepoSource is the structured snapshot.</h2><p>The repository contains the canonical dataset, schema, methodology, manifests, and validation workflow. Vercel provides the discovery and presentation layer.</p></div>
        <div className="actions"><a className="button secondary" href="https://github.com/SamoTech/RepoSource-Registry" rel="noreferrer">View GitHub ↗</a><Link className="button secondary" href="/data">Inspect data</Link></div>
      </section>

      <section className="shell section trust">
        <div>
          <div className="section-kicker">TRACEABILITY</div>
          <h2>From source to snapshot, with a visible chain.</h2>
          <div className="provenance" aria-label="Data provenance chain">
            {['GitHub source', 'Collection', 'Normalization', 'Validation', 'Snapshot', 'Public data'].map((step, index) => <span key={step}><i>{String(index + 1).padStart(2, "0")}</i>{step}</span>)}
          </div>
        </div>
        <div className="fresh"><span>Latest generated snapshot</span><strong>{stats.generated_at}</strong><small>Registry data is not live GitHub state.</small></div>
      </section>
    </div>
  );
}
