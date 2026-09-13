function jsonLd(value) {
  return JSON.stringify(value).replace(/</g, "\\u003c");
}

export function WebsiteStructuredData() {
  const data = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    name: "RepoSource Registry",
    description: "Open, machine-readable GitHub repository discovery data.",
    url: "https://repo-source-registry.vercel.app/",
    isAccessibleForFree: true,
    potentialAction: {
      "@type": "SearchAction",
      target: "https://repo-source-registry.vercel.app/search?q={search_term_string}",
      "query-input": "required name=search_term_string",
    },
  };

  return <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: jsonLd(data) }} />;
}

export function DatasetStructuredData({ stats }) {
  const data = {
    "@context": "https://schema.org",
    "@type": "Dataset",
    name: "RepoSource Registry",
    description: "Open, machine-readable GitHub repository discovery data published as a documented, reproducible snapshot.",
    url: "https://repo-source-registry.vercel.app/data",
    version: "1.0.0",
    dateModified: stats.generated_at,
    keywords: [
      "GitHub repository dataset",
      "GitHub repository discovery",
      "repository metadata",
      "open source ecosystem dataset",
      "machine-readable repository data",
    ],
    sameAs: "https://github.com/SamoTech/RepoSource-Registry",
    distribution: {
      "@type": "DataDownload",
      encodingFormat: "application/json",
      contentUrl: "https://raw.githubusercontent.com/SamoTech/RepoSource-Registry/main/data/repositories.json",
    },
    includedInDataCatalog: {
      "@type": "DataCatalog",
      name: "RepoSource Registry",
    },
    isAccessibleForFree: true,
  };

  return <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: jsonLd(data) }} />;
}
