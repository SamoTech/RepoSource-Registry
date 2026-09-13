import Link from "next/link";
import { getDataset, getStats, findRepository, isSafeGithubUrl } from "../../../../lib/registry";

export const dynamic = "force-dynamic";

export async function generateMetadata({ params }) {
  const { owner, name } = await params;
  const dataset = await getDataset();
  const repo = findRepository(dataset.repositories || [], owner, name);
  const canonical = `https://repo-source-registry.vercel.app/repo/${encodeURIComponent(owner)}/${encodeURIComponent(name)}`;
  return repo
    ? { title: repo.full_name, description: repo.description || `RepoSource Registry snapshot for ${repo.full_name}.`, alternates: { canonical } }
    : { title: "Repository not found", description: "The repository is not present in the current RepoSource Registry snapshot.", alternates: { canonical }, robots: { index: false, follow: false } };
}

export default async function RepositoryPage({ params }) {
  const { owner, name } = await params;
  const [dataset, stats] = await Promise.all([getDataset(), getStats()]);
  const repo = findRepository(dataset.repositories || [], owner, name);
  if (!repo) return <div className="shell page"><div className="empty"><span className="empty-code">404 / NOT IN SNAPSHOT</span><h1>Repository not found</h1><p>The repository is not present in the current published snapshot.</p><Link className="button" href="/search">Back to discovery</Link></div></div>;

  const stars = Number(repo.stars);
  const facts = [
    ["Primary language", repo.primary_language || "Not declared"],
    ["Stars", Number.isFinite(stars) ? stars.toLocaleString() : "Not recorded"],
    ["Forks", Number.isFinite(Number(repo.forks)) ? Number(repo.forks).toLocaleString() : "Not recorded"],
    ["Open issues", Number.isFinite(Number(repo.open_issues)) ? Number(repo.open_issues).toLocaleString() : "Not recorded"],
    ["License", repo.license || "Not declared"],
    ["Activity", repo.activity_status || "Not recorded"],
    ["Star band", repo.popularity_band || "Not recorded"],
    ["Archived", repo.archived ? "Yes" : "No"],
  ];
  const upstreamUrl = isSafeGithubUrl(repo.html_url) ? repo.html_url : null;

  return <div className="shell page">
    <Link href="/search" className="back">← Back to discovery</Link>
    <div className="repo-detail">
      <div className="detail-topline"><span className="section-kicker">REGISTRY SNAPSHOT</span><span className="record-label">SOURCE: GITHUB</span></div>
      <h1>{repo.full_name}</h1>
      <p className="lead small">{repo.description || "No description provided in the snapshot."}</p>
      <div className="actions">{upstreamUrl && <a className="button" href={upstreamUrl} rel="noreferrer">View upstream on GitHub ↗</a>}<span className="heat-tag"><i />{repo.popularity_band || "2k+"} star band</span></div>

      <dl className="facts">{facts.map(([label, value]) => <div key={label}><dt>{label}</dt><dd>{value}</dd></div>)}</dl>
      <div className="topic-list">{(Array.isArray(repo.topics) ? repo.topics : []).map(topic => <span key={topic}>{topic}</span>)}</div>

      <section className="detail-note provenance-note"><span className="section-kicker">VERIFICATION</span><strong>Snapshot first. Upstream always wins for current facts.</strong><p>This record reflects the RepoSource Registry snapshot generated at {stats.generated_at}. Mutable repository fields can change on GitHub after collection.</p></section>
      <section className="detail-note"><span className="section-kicker">REGISTRY PROVENANCE</span><div className="provenance-inline"><span>Source <b>{repo.source || "GitHub"}</b></span><span>Dataset <b>{repo.dataset_version || "—"}</b></span><span>Schema <b>{repo.schema_version || "—"}</b></span><span>Indexed <b>{repo.indexed_at || "—"}</b></span></div></section>
    </div>
  </div>;
}
