// Cloudflare Pages Function — dynamic llms-full.txt for GEO (Generative Engine
// Optimization).
//
// Route: GET /llms-full.txt
//
// Full article index in Markdown for LLM retrieval agents: every published
// article with title, URL, date and one-line summary. Companion to /llms.txt
// (site-level description + citation policy). Capped at the newest 1000
// articles; the complete historical list lives in /sitemap.xml.

const ORIGIN = "https://entropygate.cc.cd/api/v1";
const SITE = "https://aientropygate.com";
const MAX_PAGES = 5; // 5 * 200 = 1000 articles cap

function fmtDate(iso) {
  if (!iso) return "";
  try {
    return new Date(iso).toISOString().slice(0, 10);
  } catch {
    return "";
  }
}

function clean(s) {
  return String(s || "")
    .replace(/[\r\n]+/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

export async function onRequest(context) {
  // 边缘缓存：.txt 不在 CF 默认缓存扩展名内，须用 Cache API（见 sitemap.xml.js）
  const cached = await caches.default.match(context.request);
  if (cached) return cached;

  const articles = [];
  try {
    // Backend caps page_size (~200), so page through with 200/page.
    for (let page = 1; page <= MAX_PAGES; page++) {
      const r = await fetch(
        `${ORIGIN}/articles?page=${page}&page_size=200&fields=light&status=approved,published`,
        { headers: { Accept: "application/json", "User-Agent": "EntropyGate-LlmsFull/1.0" } }
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
        articles.push({
          id: a.id,
          title: clean(a.title),
          summary: clean(a.summary || a.description || ""),
          date: fmtDate(a.published_at || a.created_at || a.updated_at),
        });
      }
      if (items.length < 200) break;
    }
  } catch {
    // fall through: serve whatever we have
  }

  const lines = [
    "# EntropyGate — AI 情报快讯（全量文章索引）",
    "",
    "> 本文件列出本站最新发布的文章（最多 1000 篇），供 AI 搜索引擎与助手检索引用。",
    "> 站点说明与引用政策见 https://aientropygate.com/llms.txt",
    "> 完整历史清单见 https://aientropygate.com/sitemap.xml",
    "",
    `共收录 ${articles.length} 篇文章（截至生成时）。`,
    "",
    "## 文章列表",
    "",
  ];

  for (const a of articles) {
    const url = `${SITE}/article?id=${a.id}`;
    const date = a.date ? ` (${a.date})` : "";
    const desc = a.summary ? ` — ${a.summary.slice(0, 120)}` : "";
    lines.push(`- [${a.title || url}](${url})${date}${desc}`);
  }
  lines.push("");

  const resp = new Response(lines.join("\n"), {
    headers: {
      "Content-Type": "text/plain; charset=utf-8",
      "Cache-Control": "public, s-maxage=1800, stale-while-revalidate=3600",
    },
  });
  context.waitUntil(caches.default.put(context.request, resp.clone()));
  return resp;
}
