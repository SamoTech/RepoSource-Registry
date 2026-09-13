import Link from "next/link";
import { getDataset, getStats, searchRepositories } from "../../lib/registry";

export const dynamic = "force-dynamic";

export const metadata = {
  title: "Discover GitHub repositories",
  description: "Search and filter the RepoSource Registry snapshot by repository, owner, language, category, or star range.",
  alternates: { canonical: "https://repo-source-registry.vercel.app/search" },
};

function starBandLabel(band) {
  return band || "2k+";
}

export default async function SearchPage({ searchParams }) {
  const params = await searchParams;
  const q = params?.q || "";
  const language = params?.language || "";
  const category = params?.category || "";
  const minStars = params?.minStars || "";
  const sort = params?.sort || "stars";
  const [dataset, stats] = await Promise.all([getDataset(), getStats()]);
  const results = searchRepositories(dataset.repositories || [], { q, language, category, minStars, sort });
  const languages = Object.keys(stats.languages || {}).sort((a, b) => a.localeCompare(b));
  const categories = Object.keys(stats.categories || {}).sort((a, b) => a.localeCompare(b));
  const hasFilters = Boolean(q || language || category || minStars || sort !== "stars");
  const clearHref = "/search";

  return <div className="shell page">
    <div className="section-kicker">DISCOVERY / REGISTRY</div>
    <div className="page-heading"><div><h1>Explore repositories</h1><p className="lead small">Search the published snapshot by repository, owner, language, category, or star range.</p></div><div className="page-counter"><strong>{stats.repository_count.toLocaleString()}</strong><span>indexed records</span></div></div>

    <form className="filters" action="/search">
      <label className="filter-search"><span className="sr-only">Search text</span><input name="q" defaultValue={q} placeholder="Name, owner, description, topic…" aria-label="Search repositories" /></label>
      <select name="language" defaultValue={language} aria-label="Filter by language"><option value="">All languages</option>{languages.map(x => <option key={x}>{x}</option>)}</select>
      <select name="category" defaultValue={category} aria-label="Filter by category"><option value="">All categories</option>{categories.map(x => <option key={x}>{x}</option>)}</select>
      <select name="minStars" defaultValue={minStars} aria-label="Minimum stars"><option value="">Any stars</option><option value="5000">5k+</option><option value="10000">10k+</option><option value="50000">50k+</option></select>
      <select name="sort" defaultValue={sort} aria-label="Sort results"><option value="stars">Stars: high to low</option><option value="stars-asc">Stars: low to high</option><option value="name">Repository name</option></select>
      <button type="submit">Apply</button>
    </form>

    <div className="results-toolbar"><p className="result-count">{results.length ? `Showing ${results.length} matching result${results.length === 1 ? "" : "s"}` : "No matching repositories"}</p>{hasFilters && <Link href={clearHref} className="clear-link">Clear filters ×</Link>}</div>
    <div className="results">{results.map(repo => {
      const owner = repo.owner || String(repo.full_name || "").split("/")[0];
      const name = repo.name || String(repo.full_name || "").split("/").pop();
      const stars = Number(repo.stars);
      return <article className="repo-card" key={repo.repository_id || repo.full_name}>
        <div className="repo-head"><div><span className="record-label">REPOSITORY</span><Link href={`/repo/${encodeURIComponent(owner)}/${encodeURIComponent(name)}`}><h2>{repo.full_name || `${owner}/${name}`}</h2></Link></div><span className="heat-tag"><i />{starBandLabel(repo.popularity_band)} · stars</span></div>
        <p>{repo.description || "No description provided in the snapshot."}</p>
        <div className="meta"><span>★ {Number.isFinite(stars) ? stars.toLocaleString() : "—"}</span><span>{repo.primary_language || "No declared language"}</span>{(Array.isArray(repo.topics) ? repo.topics : []).slice(0, 4).map(t => <span key={t}>{t}</span>)}</div>
        {repo.html_url && <a className="upstream" href={repo.html_url} rel="noreferrer">View upstream on GitHub ↗</a>}
      </article>;
    })}</div>
    {!results.length && <div className="empty-state"><span className="empty-code">NO_MATCH / 204</span><h2>No repositories match these constraints.</h2><p>Try a broader name, remove a filter, or lower the minimum star threshold.</p><Link className="button secondary" href="/search">Reset discovery</Link></div>}
    <p className="disclaimer">Snapshot: {stats.generated_at}. GitHub is the upstream source for current repository facts.</p>
  </div>;
}
