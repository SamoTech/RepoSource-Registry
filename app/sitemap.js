const siteUrl = "https://repo-source-registry.vercel.app";

export const dynamic = "force-static";

export default function sitemap() {
  return [
    { url: siteUrl, changeFrequency: "weekly", priority: 1 },
    { url: `${siteUrl}/search`, changeFrequency: "weekly", priority: 0.9 },
    { url: `${siteUrl}/data`, changeFrequency: "monthly", priority: 0.8 },
  ];
}
