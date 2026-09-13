import Link from "next/link";
import { getDataset, getStats, searchRepositories } from "../../lib/registry";

export const dynamic = "force-dynamic";

export const metadata = { title: "Discover repositories", description: "Search and filter the RepoSource Registry snapshot." };

export default async function SearchPage({ searchParams }) {
  const params = await searchParams;
  const q = params?.q || "";
  const language = params?.language || "";
  const category = params?.category || "";
  const minStars = params?.minStars || "";
  const [dataset, stats] = await Promise.all([getDataset(), getStats()]);
  const results = searchRepositories(dataset.repositories || [], { q, language, category, minStars });
  const languages = Object.keys(stats.languages || {}).sort((a, b) => a.localeCompare(b));
  const categories = Object.keys(stats.categories || {}).sort((a, b) => a.localeCompare(b));

  return <div className="shell page">
    <div className="section-kicker">DISCOVERY</div>
    <h1>Explore repositories</h1>
    <p className="lead small">Search the published snapshot. Results are capped at 100 and sorted by stars.</p>
    <form className="filters" action="/search">
      <input name="q" defaultValue={q} placeholder="Name, owner, description, topic…" aria-label="Search text" />
      <select name="language" defaultValue={language} aria-label="Filter by language"><option value="">All languages</option>{languages.map(x => <option key={x}>{x}</option>)}</select>
      <select name="category" defaultValue={category} aria-label="Filter by category"><option value="">All categories</option>{categories.map(x => <option key={x}>{x}</option>)}</select>
      <select name="minStars" defaultValue={minStars} aria-label="Minimum stars"><option value="">Any stars</option><option value="5000">5k+</option><option value="10000">10k+</option><option value="50000">50k+</option></select>
      <button type="submit">Search</button>
    </form>
    <p className="result-count">{results.length ? `Showing ${results.length} matching result${results.length === 1 ? "" : "s"}` : "No matching repositories"}</p>
    <div className="results">{results.map(repo => <article className="repo-card" key={repo.repository_id}>
      <div className="repo-head"><Link href={`/repo/${encodeURIComponent(repo.owner || repo.full_name.split("/")[0])}/${encodeURIComponent(repo.name || repo.full_name.split("/").pop())}`}><h2>{repo.full_name}</h2></Link><span className="stars">★ {repo.stars.toLocaleString()}</span></div>
      <p>{repo.description || "No description provided in the snapshot."}</p>
      <div className="meta"><span>{repo.primary_language || "No declared language"}</span><span>{repo.popularity_band}</span>{(repo.topics || []).slice(0, 4).map(t => <span key={t}>{t}</span>)}</div>
      <a className="upstream" href={repo.html_url} rel="noreferrer">View on GitHub ↗</a>
    </article>)}</div>
    <p className="disclaimer">Snapshot: {stats.generated_at}. GitHub is the upstream source for current repository facts.</p>
  </div>;
}
