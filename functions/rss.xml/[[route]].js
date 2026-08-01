// Cloudflare Pages Function — RSS 2.0 feed for EntropyGate articles.
//
// Route: GET /rss.xml
//
// Fetches the latest approved/published articles from the backend API
// and renders them as a standards-compliant RSS 2.0 XML feed.

const ORIGIN = "http://117.72.240.101.nip.io/api/v1";
const SITE_URL = "https://aientropygate.com";
const FEED_TITLE = "EntropyGate — AI 情报快讯";
const FEED_DESC = "AI 领域最新动态：大语言模型、智能体、硬件、政策与研究。由 EntropyGate AI 自动采集、策展与改写。";

function escapeXml(str) {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&apos;");
}

function toRFC822(iso) {
  if (!iso) return "";
  try {
    return new Date(iso).toUTCString().replace(/GMT$/, "+0000");
  } catch {
    return "";
  }
}

export async function onRequest(context) {
  // 边缘缓存：.xml 不在 CF 默认缓存扩展名内，须用 Cache API（见 sitemap.xml.js）
  const cached = await caches.default.match(context.request);
  if (cached) return cached;
  try {
    const resp = await fetch(
      `${ORIGIN}/articles?page=1&page_size=30&fields=light&status=approved,published`,
      { headers: { Accept: "application/json" } }
    );
    if (!resp.ok) {
      return new Response("<error>Unable to fetch articles</error>", {
        status: 502,
        headers: { "Content-Type": "application/xml" },
      });
    }

    const json = await resp.json();
    // 后端信封: { code, data: { items?: list?: [...], total } }
    const payload = json.data || {};
    const items = Array.isArray(payload.items)
      ? payload.items
      : Array.isArray(payload.list)
        ? payload.list
        : [];

    const now = new Date().toUTCString().replace(/GMT$/, "+0000");

    let xml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>${escapeXml(FEED_TITLE)}</title>
  <link>${SITE_URL}</link>
  <description>${escapeXml(FEED_DESC)}</description>
  <language>zh-cn</language>
  <lastBuildDate>${now}</lastBuildDate>
  <atom:link href="${SITE_URL}/rss.xml" rel="self" type="application/rss+xml" />
`;

    for (const a of items) {
      const title = escapeXml(a.rewritten_title || a.title || "");
      const link = `${SITE_URL}/article?id=${a.id}`;
      const desc = escapeXml(a.summary || a.rewritten_content || a.preview || "");
      const pubDate = toRFC822(a.published_at || a.created_at);
      const source = escapeXml(a.source_name || "");
      const img =
        a.image_url || a.thumbnail_url
          ? `<enclosure url="${escapeXml(a.image_url || a.thumbnail_url)}" type="image/jpeg" />`
          : "";

      xml += `
  <item>
    <title>${title}</title>
    <link>${link}</link>
    <guid isPermaLink="false">${SITE_URL}/article?id=${a.id}</guid>
    <pubDate>${pubDate}</pubDate>
    <description><![CDATA[ ${desc} ]]></description>${img}
    <source url="${SITE_URL}">${source}</source>
  </item>`;
    }

    xml += `\n</channel>\n</rss>`;

    const rssResp = new Response(xml, {
      status: 200,
      headers: {
        "Content-Type": "application/rss+xml; charset=utf-8",
        "Cache-Control": "public, s-maxage=900, stale-while-revalidate=1800",
      },
    });
    context.waitUntil(caches.default.put(context.request, rssResp.clone()));
    return rssResp;
  } catch (err) {
    return new Response(`<error>${escapeXml(String(err.message))}</error>`, {
      status: 500,
      headers: { "Content-Type": "application/xml" },
    });
  }
}
