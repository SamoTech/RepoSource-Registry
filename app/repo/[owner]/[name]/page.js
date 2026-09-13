import Link from "next/link";
import { getDataset, getStats, findRepository } from "../../../../lib/registry";

export const dynamic = "force-dynamic";

export async function generateMetadata({ params }) {
  const { owner, name } = await params;
  const dataset = await getDataset();
  const repo = findRepository(dataset.repositories || [], decodeURIComponent(owner), decodeURIComponent(name));
  return { title: repo ? repo.full_name : "Repository not found", description: repo?.description || "RepoSource Registry repository snapshot." };
}

export default async function RepositoryPage({ params }) {
  const { owner, name } = await params;
  const [dataset, stats] = await Promise.all([getDataset(), getStats()]);
  const repo = findRepository(dataset.repositories || [], decodeURIComponent(owner), decodeURIComponent(name));
  if (!repo) return <div className="shell page"><div className="empty"><h1>Repository not found</h1><p>The repository is not present in the current published snapshot.</p><Link className="button" href="/search">Back to discovery</Link></div></div>;

  const fields = [
    ["Primary language", repo.primary_language || "Not declared"],
    ["Stars", repo.stars?.toLocaleString()],
    ["Forks", repo.forks?.toLocaleString()],
    ["Open issues", repo.open_issues?.toLocaleString()],
    ["License", repo.license || "Not declared"],
    ["Activity", repo.activity_status],
    ["Popularity band", repo.popularity_band],
    ["Archived", repo.archived ? "Yes" : "No"],
  ];

  return <div className="shell page">
    <Link href="/search" className="back">← Back to discovery</Link>
    <div className="repo-detail">
      <div className="section-kicker">REGISTRY SNAPSHOT</div>
      <h1>{repo.full_name}</h1>
      <p className="lead small">{repo.description || "No description provided in the snapshot."}</p>
      <div className="actions"><a className="button" href={repo.html_url} rel="noreferrer">View on GitHub ↗</a></div>
      <dl className="facts">{fields.map(([label, value]) => <div key={label}><dt>{label}</dt><dd>{value}</dd></div>)}</dl>
      <div className="topic-list">{(repo.topics || []).map(topic => <span key={topic}>{topic}</span>)}</div>
      <section className="detail-note"><strong>Verification</strong><p>This page reflects the RepoSource Registry snapshot generated at {stats.generated_at}. GitHub remains the primary source for current repository facts.</p></section>
      <section className="detail-note"><strong>Registry provenance</strong><p>Source: {repo.source}. Dataset version: {repo.dataset_version}. Schema version: {repo.schema_version}. Indexed at: {repo.indexed_at}.</p></section>
    </div>
  </div>;
}
