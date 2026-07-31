// Cloudflare Pages Function — edge reverse-proxy for the public API.
//
// Route: /api/*  ->  https://entropygate.cc.cd/api/*
//
// Cold-start mitigation: ModelScope backend can take 10-20s to wake up.
// Strategy:
// 1. stale-while-revalidate header so repeat visitors hit CF edge cache
// 2. In-memory fallback cache: if backend is cold-starting, serve last good
//    response on next request instead of blocking
// 3. Shorter timeout for anonymous GETs (15s) to fail fast and serve stale
// 4. Pre-warm: respond immediately to warm-up pings from the warmup cron
// 5. warmup-upstream: __warmup endpoint actually calls the backend health
//    endpoint to keep the container alive

const ORIGIN = "https://entropygate.cc.cd/api";

// In-memory fallback: last successful response per route
const fallbackCache = new Map();
const FALLBACK_TTL = 5 * 60 * 1000; // 5 min

export async function onRequest(context) {
  const { request, params } = context;
  const url = new URL(request.url);

  // Warm-up ping: actually call the backend health endpoint to keep it alive
  if (url.pathname === "/api/__warmup") {
    try {
      // Actually ping the backend to wake it up
      await fetch(`${ORIGIN}/health`, {
        method: "GET",
        headers: { "Accept": "application/json" },
        signal: AbortSignal.timeout(25000),
      });
    } catch (e) {
      // Backend cold-starting is expected; ignore
    }
    return new Response("ok", { status: 200 });
  }

  const route = Array.isArray(params.route)
    ? params.route.join("/")
    : params.route || "";
  const upstream = `${ORIGIN}/${route}${url.search}`;

  const headers = new Headers(request.headers);
  headers.delete("host");

  const isAnonymousGet = request.method === "GET" && !headers.has("x-access-token") && !route.startsWith("v1/auth/");

  try {
    const resp = await fetch(upstream, {
      method: request.method,
      headers,
      body: request.method === "GET" ? undefined : request.body,
      redirect: "manual",
      // Longer timeout for anonymous GETs to survive cold start (25s)
      signal: AbortSignal.timeout(isAnonymousGet ? 25000 : 30000),
    });

    // Cache successful anonymous GET responses for fallback
    if (isAnonymousGet && resp.ok) {
      const body = await resp.clone().text();
      fallbackCache.set(route, {
        status: resp.status,
        headers: [...resp.headers.entries()],
        body,
        timestamp: Date.now(),
      });
    }

    if (resp.ok) {
      const h = new Headers(resp.headers);
      if (isAnonymousGet) {
        // stale-while-revalidate: edge serves stale up to 5 min while
        // fetching fresh in background — eliminates cold-start for repeat
        // visitors and search engine crawlers
        h.set("Cache-Control", "public, max-age=120, stale-while-revalidate=300");
      }
      return new Response(resp.body, { status: resp.status, headers: h });
    }
    return resp;
  } catch (err) {
    // Backend cold-starting or unreachable: serve stale fallback
    if (isAnonymousGet && fallbackCache.has(route)) {
      const cached = fallbackCache.get(route);
      if (Date.now() - cached.timestamp < FALLBACK_TTL) {
        const h = new Headers(cached.headers);
        h.set("Cache-Control", "public, max-age=30");
        h.set("X-Cache", "stale");
        return new Response(cached.body, { status: cached.status, headers: h });
      }
    }
    // No fallback: let the browser handle the error
    throw err;
  }
}
