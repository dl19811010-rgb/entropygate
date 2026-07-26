// Cloudflare Pages Function — dynamic sitemap.xml for SEO.
//
// Route: GET /sitemap.xml
//
// Lists every approved/published article so search engines can discover all
// content (the SPA has no crawlable internal links to most articles).

const ORIGIN = "https://entropygate.cc.cd/api/v1";
const SITE = "https://aientropygate.com";

function escapeXml(s) {
  return String(s || "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&apos;");
}

function toW3C(iso) {
  if (!iso) return "";
  try {
    return new Date(iso).toISOString();
  } catch {
    return "";
  }
}

export async function onRequest() {
  const staticUrls = [
    { loc: `${SITE}/`, priority: "1.0", changefreq: "hourly" },
    { loc: `${SITE}/flash`, priority: "0.8", changefreq: "hourly" },
    { loc: `${SITE}/search`, priority: "0.5", changefreq: "daily" },
    { loc: `${SITE}/about`, priority: "0.3", changefreq: "monthly" },
  ];

  const urls = [];
  try {
    // Pull up to 1000 recent articles (light fields keep the payload small).
    const r = await fetch(
      `${ORIGIN}/articles?page=1&page_size=1000&fields=light&status=approved,published`,
      { headers: { Accept: "application/json", "User-Agent": "EntropyGate-Sitemap/1.0" } }
    );
    if (r.ok) {
      const j = await r.json();
      const payload = j.data || {};
      const items = Array.isArray(payload.items)
        ? payload.items
        : Array.isArray(payload.list)
          ? payload.list
          : [];
      for (const a of items) {
        if (!a || !a.id) continue;
        urls.push({
          loc: `${SITE}/article?id=${a.id}`,
          lastmod: toW3C(a.updated_at || a.published_at || a.created_at),
          priority: "0.7",
          changefreq: "weekly",
        });
      }
    }
  } catch {
    // fall through: serve whatever we have (static routes at minimum)
  }

  const body =
    `<?xml version="1.0" encoding="UTF-8"?>\n` +
    `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n` +
    [...staticUrls, ...urls]
      .map(
        (u) =>
          `  <url><loc>${escapeXml(u.loc)}</loc>` +
          (u.lastmod ? `<lastmod>${u.lastmod}</lastmod>` : "") +
          `<changefreq>${u.changefreq}</changefreq><priority>${u.priority}</priority></url>`
      )
      .join("\n") +
    `\n</urlset>\n`;

  return new Response(body, {
    headers: {
      "Content-Type": "application/xml; charset=utf-8",
      "Cache-Control": "public, s-maxage=600, stale-while-revalidate=1800",
    },
  });
}
