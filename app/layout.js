import Link from "next/link";
import "./globals.css";

const siteUrl = "https://repo-source-registry.vercel.app";
const githubBase = "https://github.com/SamoTech/RepoSource-Registry/blob/main/";

export const metadata = {
  metadataBase: new URL(siteUrl),
  title: { default: "RepoSource Registry — GitHub Repository Discovery", template: "%s · RepoSource Registry" },
  description: "Open, machine-readable GitHub repository discovery data with documented provenance, schema, and snapshots.",
  alternates: { canonical: siteUrl },
  openGraph: {
    title: "RepoSource Registry — GitHub Repository Discovery",
    description: "Open, machine-readable GitHub repository discovery data.",
    type: "website",
    url: siteUrl,
    siteName: "RepoSource Registry",
  },
  twitter: { card: "summary", title: "RepoSource Registry", description: "Open GitHub repository discovery data." },
  robots: { index: true, follow: true },
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <header className="site-header">
          <div className="shell nav">
            <Link href="/" className="brand" aria-label="RepoSource Registry home"><span className="brand-mark">R</span><span>RepoSource</span> Registry</Link>
            <nav aria-label="Primary navigation">
              <Link href="/search">Discover</Link>
              <Link href="/data">Data</Link>
              <a href={`${githubBase}docs/research.md`} rel="noreferrer">Research ↗</a>
              <a href={`${githubBase}docs/services.md`} rel="noreferrer">Services ↗</a>
              <a href="https://github.com/SamoTech/RepoSource-Registry" rel="noreferrer">GitHub ↗</a>
            </nav>
          </div>
        </header>
        <main>{children}</main>
        <footer className="footer">
          <div className="shell footer-grid">
            <div><strong>RepoSource Registry</strong><p>Open repository discovery data. GitHub remains the primary source for current repository facts.</p><span className="footer-status"><i /> PUBLIC DATASET · MIT LICENSE</span></div>
            <div className="footer-links">
              <Link href="/search">Discover</Link><Link href="/data">Dataset</Link>
              <a href={`${githubBase}docs/quickstart.md`} rel="noreferrer">Quickstart</a>
              <a href={`${githubBase}docs/methodology.md`} rel="noreferrer">Methodology</a>
              <a href={`${githubBase}docs/data-dictionary.md`} rel="noreferrer">Schema / dictionary</a>
              <a href={`${githubBase}docs/research.md`} rel="noreferrer">Research</a>
              <a href={`${githubBase}docs/showcase.md`} rel="noreferrer">Showcase</a>
              <a href={`${githubBase}docs/sponsoring.md`} rel="noreferrer">Sponsoring</a>
              <a href={`${githubBase}docs/services.md`} rel="noreferrer">Services</a>
              <a href={`${githubBase}CONTRIBUTING.md`} rel="noreferrer">Contributing</a>
              <a href={`${githubBase}SECURITY.md`} rel="noreferrer">Security</a>
              <a href={`${githubBase}CITATION.cff`} rel="noreferrer">Citation</a>
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}
