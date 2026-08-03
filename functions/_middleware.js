// Root-level _middleware.js — handles /api/* requests by proxying to Tunnel
// Non-API requests pass through to static assets via next()
const ORIGIN = "https://api-tunnel.aientropygate.com";
const fallbackCache = new Map();
const FALLBACK_TTL = 5 * 60 * 1000;

export async function onRequest(context) {
  const { request, next } = context;
  const url = new URL(request.url);
  const pathname = url.pathname;

  // Only handle /api/* routes
  if (!pathname.startsWith("/api/")) {
    return next();
  }

  // Warm-up ping
  if (pathname === "/api/__warmup") {
    try {
      await fetch(ORIGIN + "/api/v1/health", {
        method: "GET",
        headers: { "Accept": "application/json" },
        signal: AbortSignal.timeout(25000),
      });
    } catch (e) {}
    return new Response("ok", { status: 200 });
  }

  // Build upstream URL using the full pathname
  // e.g. /api/v1/health -> https://api-tunnel.aientropygate.com/api/v1/health
  const upstream = ORIGIN + pathname + url.search;

  const headers = new Headers(request.headers);
  headers.delete("host");

  const isAnonymousGet = request.method === "GET" && !headers.has("x-access-token");

  try {
    const resp = await fetch(upstream, {
      method: request.method,
      headers,
      body: request.method === "GET" ? undefined : request.body,
      redirect: "manual",
      signal: AbortSignal.timeout(isAnonymousGet ? 25000 : 30000),
    });

    if (isAnonymousGet && resp.ok) {
      const body = await resp.clone().text();
      fallbackCache.set(pathname, {
        status: resp.status,
        headers: [...resp.headers.entries()],
        body,
        timestamp: Date.now(),
      });
    }

    if (resp.ok) {
      const h = new Headers(resp.headers);
      if (isAnonymousGet) {
        h.set("Cache-Control", "public, max-age=120, stale-while-revalidate=300");
      }
      return new Response(resp.body, { status: resp.status, headers: h });
    }
    return resp;
  } catch (err) {
    if (isAnonymousGet && fallbackCache.has(pathname)) {
      const cached = fallbackCache.get(pathname);
      if (Date.now() - cached.timestamp < FALLBACK_TTL) {
        const h = new Headers(cached.headers);
        h.set("Cache-Control", "public, max-age=30");
        h.set("X-Cache", "stale");
        return new Response(cached.body, { status: cached.status, headers: h });
      }
    }
    throw err;
  }
}