// Cloudflare Pages Function — edge reverse-proxy for the public API.
//
// The public reader only issues GETs (stories / featured / breaking / article
// detail). The ModelScope Studio origin has a ~2.2s fixed gateway latency, so
// we proxy those GETs here and let a Cloudflare **Cache Rule** (configured on
// the zone) cache the responses at the CDN edge for 60s. Domestic users then
// get <100ms responses without ever hitting the Studio gateway.
//
// (Note: the Pages Functions `caches.default` API is per-invocation and does
// NOT persist across requests, so edge caching must be done via a Cache Rule,
// not the Cache API here.)
//
// Route: /api/*  ->  https://entropygate.cc.cd/api/*
// Non-GET (POST/PUT/DELETE) is passed through untouched (admin uses its own
// origin and must not be cached).

const ORIGIN = "https://entropygate.cc.cd/api";

export async function onRequest(context) {
  const { request, params } = context;
  const url = new URL(request.url);

  // Rebuild upstream URL: /api/<route> -> ORIGIN/<route>
  // NOTE: [[route]] (optional catch-all) yields an ARRAY of path segments.
  const route = Array.isArray(params.route)
    ? params.route.join("/")
    : (params.route || "");
  const upstream = `${ORIGIN}/${route}${url.search}`;

  // Only annotate/cache safe GETs; everything else is a transparent pass-through.
  if (request.method === "GET") {
    const resp = await fetch(upstream, {
      method: "GET",
      headers: { Accept: "application/json" },
    });
    if (resp.ok) {
      const h = new Headers(resp.headers);
      // Signal the CDN to cache this response at the edge for 60s.
      // (The actual caching is enforced by a Cache Rule on the zone; this
      // header is a belt-and-suspenders hint.)
      h.set("Cache-Control", "public, max-age=60");
      return new Response(resp.body, { status: resp.status, headers: h });
    }
    return resp;
  }

  // Non-GET: transparent pass-through (admin writes etc.)
  return fetch(upstream, {
    method: request.method,
    headers: request.headers,
    body: request.body,
  });
}
