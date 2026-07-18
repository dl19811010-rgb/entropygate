// Cloudflare Pages Function — edge reverse-proxy for the public API.
//
// Route: /api/*  ->  https://entropygate.cc.cd/api/*
//
// Why a same-origin proxy?
//   The public frontend is served from aientropygate.com, while the API origin
//   is entropygate.cc.cd (a different host). A browser calling the API directly
//   is a cross-origin request. The upstream gateway in front of ModelScope
//   Studio only allows a FIXED set of CORS request headers (it strips
//   `Authorization` and does NOT list `X-Access-Token` / `X-Fields`), so any
//   custom header (e.g. the auth token `X-Access-Token`) triggers a CORS
//   preflight that the gateway rejects — breaking both authenticated requests
//   and any header-based feature.
//
//   Routing through this same-origin Function eliminates browser CORS entirely:
//   the browser talks to aientropygate.com/api/* (same origin), and this
//   Function forwards to the backend server-to-server, freely passing through
//   auth/custom headers.
//
// GETs are cached at the CDN edge for 60s via a Cache Rule on the zone
// (domestic users get <100ms). Authenticated GETs are NOT cached to avoid
// leaking private data. Non-GET (POST/PUT/DELETE) is a transparent pass-through.

const ORIGIN = "https://entropygate.cc.cd/api";

export async function onRequest(context) {
  const { request, params } = context;
  const url = new URL(request.url);

  // Rebuild upstream URL: /api/<route> -> ORIGIN/<route>
  // NOTE: [[route]] (optional catch-all) yields an ARRAY of path segments.
  const route = Array.isArray(params.route)
    ? params.route.join("/")
    : params.route || "";
  const upstream = `${ORIGIN}/${route}${url.search}`;

  // Forward the original request headers so auth (X-Access-Token) and any
  // custom headers survive the hop. Server-to-server, so no browser CORS.
  // Drop `host` (must reflect the upstream, not the Pages host).
  const headers = new Headers(request.headers);
  headers.delete("host");

  if (request.method === "GET") {
    const resp = await fetch(upstream, { method: "GET", headers });
    if (resp.ok) {
      const h = new Headers(resp.headers);
      // Only hint edge caching for anonymous GETs.
      if (!headers.has("x-access-token")) {
        h.set("Cache-Control", "public, max-age=60");
      }
      return new Response(resp.body, { status: resp.status, headers: h });
    }
    return resp;
  }

  // Non-GET: transparent pass-through (auth writes, crawler, admin, etc.)
  return fetch(upstream, {
    method: request.method,
    headers,
    body: request.body,
  });
}
