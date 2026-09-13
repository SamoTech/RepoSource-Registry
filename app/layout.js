import Link from "next/link";
import "./globals.css";

export const metadata = {
  title: { default: "RepoSource Registry — GitHub Repository Discovery", template: "%s · RepoSource Registry" },
  description: "Explore an open, machine-readable GitHub repository discovery dataset with documented provenance, schema, and snapshots.",
  openGraph: {
    title: "RepoSource Registry — GitHub Repository Discovery",
    description: "Open, machine-readable GitHub repository discovery data.",
    type: "website",
  },
  twitter: { card: "summary", title: "RepoSource Registry", description: "Open GitHub repository discovery data." },
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <header className="site-header">
          <div className="shell nav">
            <Link href="/" className="brand">RepoSource <span>Registry</span></Link>
            <nav aria-label="Primary navigation">
              <Link href="/search">Discover</Link>
              <Link href="/data">Data</Link>
              <a href="https://github.com/SamoTech/RepoSource-Registry">GitHub</a>
            </nav>
          </div>
        </header>
        <main>{children}</main>
        <footer className="footer">
          <div className="shell footer-grid">
            <div><strong>RepoSource Registry</strong><p>Open repository discovery data. GitHub remains the primary source for current repository facts.</p></div>
            <div className="footer-links"><Link href="/data">Dataset</Link><a href="https://github.com/SamoTech/RepoSource-Registry/blob/main/docs/methodology.md">Methodology</a><a href="https://github.com/SamoTech/RepoSource-Registry/blob/main/docs/sponsoring.md">Sponsoring</a></div>
          </div>
        </footer>
      </body>
    </html>
  );
}
