// Cloudflare Pages Function — edge reverse-proxy + cache for the public API.
//
// The public reader only issues GETs (stories / featured / breaking / article
// detail). The ModelScope Studio origin has a ~2.2s fixed gateway latency, so
// we cache those GET responses at the Cloudflare edge for 60s. Domestic users
// then get <100ms responses without ever hitting the Studio gateway.
//
// Route: /api/*  ->  https://entropygate.cc.cd/api/*
// Non-GET (POST/PUT/DELETE) is passed through untouched (admin uses its own
// origin and must not be cached).

const ORIGIN = "https://entropygate.cc.cd/api";

export async function onRequest(context) {
  const { request, params } = context;
  const url = new URL(request.url);

  // Rebuild upstream URL: /api/<route> -> ORIGIN/<route>
  // NOTE: [[route]] (optional catch-all) yields an ARRAY of path segments,
  // so join with "/" to reconstruct the path.
  const route = Array.isArray(params.route)
    ? params.route.join("/")
    : (params.route || "");
  const upstream = `${ORIGIN}/${route}${url.search}`;

  // Only cache safe, idempotent GET requests
  if (request.method === "GET") {
    const cache = caches.default;
    const cacheKey = new Request(upstream, { method: "GET" });

    let resp = await cache.match(cacheKey);
    if (resp) {
      const h = new Headers(resp.headers);
      h.set("X-Cache", "HIT");
      h.set("X-Upstream", upstream);
      return new Response(resp.body, { status: resp.status, headers: h });
    }

    resp = await fetch(upstream, {
      method: "GET",
      headers: { Accept: "application/json" },
    });

    if (resp.ok) {
      const h = new Headers(resp.headers);
      h.set("X-Upstream", upstream);
      // Cache public list/detail responses at the edge for 60s
      h.set("Cache-Control", "public, max-age=60");
      h.set("X-Cache", "MISS");
      const out = new Response(resp.body, { status: resp.status, headers: h });
      // Await the write so the next request can read it back
      try {
        await cache.put(cacheKey, out.clone());
        h.set("X-Put", "ok");
      } catch (e) {
        h.set("X-Put", "fail:" + e.message);
      }
      return out;
    }
    // Non-ok: echo upstream for debugging
    const eh = new Headers(resp.headers);
    eh.set("X-Upstream", upstream);
    eh.set("X-Cache", "ERROR");
    return new Response(resp.body, { status: resp.status, headers: eh });
  }

  // Non-GET: transparent pass-through (admin writes etc.)
  return fetch(upstream, {
    method: request.method,
    headers: request.headers,
    body: request.body,
  });
}
