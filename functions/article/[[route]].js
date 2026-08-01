// Cloudflare Pages Function — article page SSR injection for SEO/GEO.
//
// Route: GET /article?id=<n>  (also /article/* legacy)
//
// Problem: the article page is a pure client-rendered SPA — the initial HTML
// only contains a loading skeleton, and the body is rendered inside an iframe
// (kimi_html is a full self-contained HTML doc). Search engines and LLM
// crawlers that do not execute JS see an empty page.
//
// Fix: at the edge, fetch the article from the backend and inject into the
// static HTML, before it reaches the client:
//   1. <title> + meta description + Open Graph / Twitter cards + canonical
//   2. JSON-LD (NewsArticle) for rich results & AI-engine comprehension
//   3. The full article body as readable HTML (styles scoped to the container)
//
// Human visitors are unaffected: the container sits after the React root, the
// SPA removes it on mount (see article page useEffect) and renders the normal
// iframe view. Bots without JS keep the full text. Same content, two render
// paths — not cloaking.

const ORIGIN = "https://api-tunnel.aientropygate.com/api/v1";
const SITE = "https://aientropygate.com";

function escapeHtml(s) {
  return String(s || "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function stripTags(s) {
  return String(s || "").replace(/<[^>]*>/g, " ").replace(/\s+/g, " ").trim();
}

// Extract <style> blocks + body inner HTML from a full kimi_html document,
// and scope bare `body`/`html` selectors to the container so the article
// styles do not leak into the host page.
function extractKimi(html) {
  if (!html) return { css: "", body: "" };
  let css = "";
  const styleRe = /<style[^>]*>([\s\S]*?)<\/style>/gi;
  let m;
  while ((m = styleRe.exec(html)) !== null) css += m[1] + "\n";
  css = css
    .replace(/(^|[},]\s*)html\b/g, "$1#ssr-kimi-root")
    .replace(/(^|[},]\s*)body\b/g, "$1#ssr-kimi-root");
  let body = "";
  const bodyRe = /<body[^>]*>([\s\S]*?)<\/body>/i;
  const bm = bodyRe.exec(html);
  body = bm ? bm[1] : html;
  // scripts are not expected in kimi output; drop them defensively
  body = body.replace(/<script[\s\S]*?<\/script>/gi, "");
  return { css, body };
}

class HeadHandler {
  constructor(meta) {
    this.meta = meta;
  }
  element(el) {
    const m = this.meta;
    const tags = [];
    tags.push(`<meta name="description" content="${escapeHtml(m.description)}">`);
    tags.push(`<link rel="canonical" href="${escapeHtml(m.canonical)}">`);
    tags.push(`<meta property="og:type" content="article">`);
    tags.push(`<meta property="og:title" content="${escapeHtml(m.title)}">`);
    tags.push(`<meta property="og:description" content="${escapeHtml(m.description)}">`);
    tags.push(`<meta property="og:url" content="${escapeHtml(m.canonical)}">`);
    if (m.image) tags.push(`<meta property="og:image" content="${escapeHtml(m.image)}">`);
    tags.push(`<meta name="twitter:card" content="summary_large_image">`);
    tags.push(`<meta name="twitter:title" content="${escapeHtml(m.title)}">`);
    tags.push(`<meta name="twitter:description" content="${escapeHtml(m.description)}">`);
    if (m.image) tags.push(`<meta name="twitter:image" content="${escapeHtml(m.image)}">`);
    tags.push(`<script type="application/ld+json">${m.jsonld}</script>`);
    el.append(tags.join(""), { html: true });
  }
}

class TitleHandler {
  constructor(title) {
    this.title = title;
    this.done = false;
  }
  element(el) {
    if (!this.done) {
      el.setInnerContent(this.title, { html: false });
      this.done = true;
    }
  }
}

class BodyHandler {
  constructor(ssrHtml) {
    this.ssrHtml = ssrHtml;
  }
  element(el) {
    el.append(this.ssrHtml, { html: true });
  }
}

export async function onRequest(context) {
  const { request } = context;
  if (request.method !== "GET" && request.method !== "HEAD") {
    return context.next();
  }
  const url = new URL(request.url);
  const id = url.searchParams.get("id");
  if (!id || !/^\d+$/.test(id)) {
    return context.next();
  }

  // Fetch the static article.html that the SPA would normally serve.
  const assetResp = await context.next();
  if (!assetResp.ok) return assetResp;

  let article;
  try {
    const r = await fetch(`${ORIGIN}/articles/${encodeURIComponent(id)}`, {
      headers: { Accept: "application/json", "User-Agent": "EntropyGate-SSR/1.0" },
    });
    if (!r.ok) return assetResp;
    const j = await r.json();
    article = (j && j.data) || null;
  } catch {
    return assetResp;
  }
  if (!article || !article.id) return assetResp;

  const title =
    (article.rewritten_title || article.title || "快讯").trim() + " — EntropyGate";
  const description =
    stripTags(article.ai_summary || article.summary || "").slice(0, 180) ||
    "AI 领域最新动态，由 EntropyGate 编辑智能筛选与改写。";
  const canonical = `${SITE}/article?id=${article.id}`;
  const image = article.image_url || article.cover_url || "";
  const published = article.published_at || article.created_at || "";
  const kimi = typeof article.kimi_html === "string" && article.kimi_html.length > 1000
    ? article.kimi_html
    : "";

  const jsonld = JSON.stringify({
    "@context": "https://schema.org",
    "@type": "NewsArticle",
    headline: article.rewritten_title || article.title || "",
    description,
    image: image ? [image] : undefined,
    datePublished: published,
    dateModified: article.updated_at || published,
    author: { "@type": "Organization", name: "EntropyGate", url: SITE },
    publisher: {
      "@type": "Organization",
      name: "EntropyGate",
      logo: { "@type": "ImageObject", url: `${SITE}/logo.png` },
    },
    mainEntityOfPage: canonical,
    inLanguage: "zh-CN",
  }).replace(/<\//g, "<\\/");

  let ssrHtml = "";
  if (kimi) {
    const { css, body } = extractKimi(kimi);
    ssrHtml =
      `<div id="ssr-kimi-root" style="max-width:780px;margin:24px auto;padding:0 16px;">` +
      (css ? `<style>${css}</style>` : "") +
      body +
      `</div>`;
  } else {
    // Non-kimi article: still expose title + summary as readable text.
    ssrHtml =
      `<div id="ssr-kimi-root" style="max-width:780px;margin:24px auto;padding:0 16px;">` +
      `<h1>${escapeHtml(article.rewritten_title || article.title || "")}</h1>` +
      `<p>${escapeHtml(description)}</p></div>`;
  }

  const rewritten = new HTMLRewriter()
    .on("title", new TitleHandler(title))
    .on("head", new HeadHandler({
      title, description, canonical, image, jsonld,
    }))
    .on("body", new BodyHandler(ssrHtml))
    .transform(assetResp);

  const headers = new Headers(rewritten.headers);
  headers.set("Cache-Control", "public, s-maxage=300, stale-while-revalidate=600");
  return new Response(rewritten.body, {
    status: rewritten.status,
    statusText: rewritten.statusText,
    headers,
  });
}
