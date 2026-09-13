export default function robots() {
  const base = process.env.SITE_URL ? process.env.SITE_URL.replace(/\/$/, "") : process.env.VERCEL_URL ? `https://${process.env.VERCEL_URL}` : "";
  return {
    rules: { userAgent: "*", allow: "/" },
    ...(base ? { sitemap: `${base}/sitemap.xml` } : {}),
  };
}
