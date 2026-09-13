import Link from "next/link";
import { getStats } from "../lib/registry";

export const revalidate = 3600;

export default async function Home() {
  const stats = await getStats();
  const languages = Object.entries(stats.languages || {}).sort((a, b) => b[1] - a[1]).slice(0, 8);
  const categories = Object.entries(stats.categories || {}).sort((a, b) => b[1] - a[1]);

  return (
    <div>
      <section className="hero shell">
        <div className="eyebrow">OPEN DATA · REPRODUCIBLE SNAPSHOT</div>
        <h1>Discover the repositories shaping open source.</h1>
        <p className="lead">RepoSource Registry is an open, machine-readable GitHub repository discovery dataset for developers, researchers, and open-source tooling.</p>
        <form action="/search" className="searchbar">
          <label htmlFor="q" className="sr-only">Search repositories</label>
          <input id="q" name="q" placeholder="Search repositories, owners, descriptions, or topics" />
          <button type="submit">Discover repositories</button>
        </form>
        <p className="note">Registry values are a snapshot. Verify important current facts on GitHub.</p>
        <div className="thermal-panel" aria-label="Repository popularity temperature scale">
          <div className="thermal-head"><strong>Popularity temperature</strong><span>cold → hot · visual scale</span></div>
          <div className="thermal-scale" aria-hidden="true" />
          <div className="thermal-labels"><span className="cold">2K° · baseline</span><span className="hot">50K°+ · hot</span></div>
        </div>
      </section>

      <section className="shell stats" aria-label="Dataset statistics">
        <div><strong>{stats.repository_count.toLocaleString()}</strong><span>repositories</span></div>
        <div><strong>{Object.keys(stats.languages || {}).length}</strong><span>language values</span></div>
        <div><strong>{Object.keys(stats.categories || {}).length}</strong><span>derived categories</span></div>
        <div><strong>{stats.minimum_stars.toLocaleString()}+</strong><span>minimum stars</span></div>
      </section>

      <section className="shell section two-col">
        <div>
          <div className="section-kicker">EXPLORE</div>
          <h2>Browse the ecosystem by language.</h2>
          <p>Use the published snapshot to inspect popular language segments without changing the underlying dataset.</p>
          <div className="chips">{languages.map(([name, count]) => <Link key={name} href={`/search?language=${encodeURIComponent(name)}`} className="chip">{name}<b>{count.toLocaleString()}</b></Link>)}</div>
        </div>
        <div className="panel">
          <div className="section-kicker">CATEGORIES</div>
          {categories.map(([name, count]) => <Link key={name} href={`/search?category=${encodeURIComponent(name)}`} className="bar-row"><span>{name}</span><b>{count.toLocaleString()}</b></Link>)}
        </div>
      </section>

      <section className="shell section callout">
        <div><div className="section-kicker">OPEN DATA</div><h2>The GitHub repository is the source project. This site is the discovery layer.</h2><p>The canonical dataset, schema, methodology, manifests, and contribution workflow remain in the GitHub repository.</p></div>
        <div className="actions"><a className="button secondary" href="https://github.com/SamoTech/RepoSource-Registry">View GitHub</a><Link className="button secondary" href="/data">Inspect data</Link></div>
      </section>

      <section className="shell section trust">
        <div><h2>Source → collection → validation → snapshot → verification</h2><p>GitHub remains the primary source for repository facts. RepoSource Registry publishes a structured secondary snapshot with explicit scope, schema, provenance, and integrity metadata.</p></div>
        <div className="fresh"><span>Latest snapshot</span><strong>{stats.generated_at}</strong></div>
      </section>
    </div>
  );
}
