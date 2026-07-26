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

export async function onRequest(context) {
  // 边缘缓存：CF 默认不缓存 .xml，Cache-Control 头单独不生效，
  // 必须用 Cache API 程序化缓存（2026-07-26 实测冷请求 ~4.5-11s）。
  const cached = await caches.default.match(context.request);
  if (cached) return cached;

  const staticUrls = [
    { loc: `${SITE}/`, priority: "1.0", changefreq: "hourly" },
    { loc: `${SITE}/flash`, priority: "0.8", changefreq: "hourly" },
    { loc: `${SITE}/search`, priority: "0.5", changefreq: "daily" },
    { loc: `${SITE}/about`, priority: "0.3", changefreq: "monthly" },
  ];

  const urls = [];
  try {
    // Backend caps page_size (422 above ~200), so page through with 200/page.
    for (let page = 1; page <= 20; page++) {
      const r = await fetch(
        `${ORIGIN}/articles?page=${page}&page_size=200&fields=light&status=approved,published`,
        { headers: { Accept: "application/json", "User-Agent": "EntropyGate-Sitemap/1.0" } }
      );
      if (!r.ok) break;
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
      if (items.length < 200) break;
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

  const resp = new Response(body, {
    headers: {
      "Content-Type": "application/xml; charset=utf-8",
      "Cache-Control": "public, s-maxage=1800, stale-while-revalidate=3600",
    },
  });
  context.waitUntil(caches.default.put(context.request, resp.clone()));
  return resp;
}
