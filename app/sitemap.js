export default function sitemap() {
  const base = process.env.SITE_URL ? process.env.SITE_URL.replace(/\/$/, "") : process.env.VERCEL_URL ? `https://${process.env.VERCEL_URL}` : null;
  if (!base) return [];
  return ["/", "/search", "/data"].map((path) => ({ url: `${base}${path}`, changeFrequency: path === "/" ? "weekly" : "monthly", priority: path === "/" ? 1 : 0.7 }));
}
