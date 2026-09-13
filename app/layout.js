import Link from "next/link";
import "./globals.css";
import { WebsiteStructuredData } from "./seo-schema";

const siteUrl = "https://repo-source-registry.vercel.app";
const githubBase = "https://github.com/SamoTech/RepoSource-Registry/blob/main/";
const githubRepo = "https://github.com/SamoTech/RepoSource-Registry";
const sponsorUrl = "https://github.com/sponsors/SamoTech";

export const metadata = {
  metadataBase: new URL(siteUrl),
  title: { default: "RepoSource Registry — Open GitHub Repository Discovery Data", template: "%s · RepoSource Registry" },
  description: "Open, machine-readable GitHub repository discovery data with documented provenance, schema, and reproducible snapshots.",
  alternates: { canonical: siteUrl },
  verification: {
    google: "_EapoLGFWorKHOtsAEG4rjq0wg__sAgb5ARz1hrEBCw",
  },
  openGraph: {
    title: "RepoSource Registry — Open GitHub Repository Discovery Data",
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
        <WebsiteStructuredData />
        <header className="site-header">
          <div className="shell nav">
            <Link href="/" className="brand" aria-label="RepoSource Registry home"><span className="brand-mark">R</span><span>RepoSource</span> Registry</Link>
            <nav aria-label="Primary navigation">
              <Link href="/search">Discover</Link>
              <Link href="/data">Data</Link>
              <Link href="/research">Research</Link>
              <Link href="/quality">Quality</Link>
              <a href={`${githubBase}docs/services.md`} rel="noreferrer">Services ↗</a>
              <a href={sponsorUrl} rel="noreferrer">Sponsor ↗</a>
              <a href={githubRepo} rel="noreferrer">GitHub ↗</a>
            </nav>
          </div>
        </header>
        <main>{children}</main>
        <footer className="footer">
          <div className="shell footer-grid">
            <div><strong>RepoSource Registry</strong><p>Open repository discovery data. GitHub remains the primary source for current repository facts.</p><span className="footer-status"><i /> PUBLIC DATASET · MIT LICENSE</span></div>
            <div className="footer-links">
              <Link href="/search">Discover</Link><Link href="/data">Dataset</Link>
              <Link href="/research">Research</Link><Link href="/quality">Quality</Link>
              <a href={`${githubBase}docs/quickstart.md`} rel="noreferrer">Quickstart</a>
              <a href={`${githubBase}docs/methodology.md`} rel="noreferrer">Methodology</a>
              <a href={`${githubBase}docs/data-dictionary.md`} rel="noreferrer">Schema / dictionary</a>
              <a href={`${githubBase}docs/showcase.md`} rel="noreferrer">Showcase</a>
              <a href={`${githubBase}docs/sponsoring.md`} rel="noreferrer">Sponsoring</a>
              <a href={sponsorUrl} rel="noreferrer">GitHub Sponsors ↗</a>
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
