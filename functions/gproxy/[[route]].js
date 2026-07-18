// Cloudflare Pages Function — edge reverse-proxy for Google OAuth endpoints.
//
// Routes (all fixed Google hosts only):
//   /gproxy/auth     ->  https://accounts.google.com/o/oauth2/v2/auth
//   /gproxy/token    ->  https://oauth2.googleapis.com/token
//   /gproxy/userinfo ->  https://www.googleapis.com/oauth2/v3/userinfo
//
// Why?
//   The backend runs inside ModelScope Studio (a China datacenter). Google's
//   OAuth hosts are NOT reachable from China. This Function runs on
//   Cloudflare's global edge (which CAN reach Google) and the backend points
//   its google token_url / userinfo_url at this proxy.
//
// CRITICAL FIX (2026-07-18): Google's token endpoint returns HTTP 403 for
// requests whose User-Agent is `Python-urllib/...` (the default UA used by
// Python's urllib on the backend). It accepts curl/browser UAs (returns 400
// for a bad code). We therefore MUST strip the caller's UA and send a normal
// browser UA, and buffer the POST body so the upstream sees a clean request.
//
// Security: generic pass-through to three fixed Google hosts. No secrets of its
// own; client_secret is sent server-to-server in the POST body to /gproxy/token
// and never reaches the browser.

const UPSTREAM = {
  auth: "https://accounts.google.com/o/oauth2/v2/auth",
  token: "https://oauth2.googleapis.com/token",
  userinfo: "https://www.googleapis.com/oauth2/v3/userinfo",
};

const PROXY_UA =
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36";

export async function onRequest(context) {
  const { request, params } = context;
  const url = new URL(request.url);

  const seg = Array.isArray(params.route)
    ? params.route.join("/")
    : params.route || "";
  const key = seg.split("/")[0];
  const target = UPSTREAM[key];
  if (!target) {
    return new Response(
      JSON.stringify({ error: "unknown_gproxy_route", hint: "use /gproxy/{auth|token|userinfo}" }),
      { status: 404, headers: { "Content-Type": "application/json" } }
    );
  }

  const upstream = `${target}${url.search}`;
  const headers = new Headers(request.headers);
  // Drop hop-by-hop / identity headers that would confuse the upstream.
  headers.delete("host");
  headers.delete("cf-connecting-ip");
  // Drop the caller's UA (Python-urllib etc.) — Google 403s those.
  headers.delete("user-agent");
  headers.set("User-Agent", PROXY_UA);

  const init = { method: request.method, headers };
  if (request.method !== "GET" && request.method !== "HEAD") {
    // Buffer the body so the upstream receives a clean, complete request
    // (streaming the original Request body can drop Content-Length / encoding).
    const text = await request.text();
    init.body = text;
    if (!headers.has("content-type")) {
      headers.set("Content-Type", "application/x-www-form-urlencoded");
    }
  }

  const resp = await fetch(upstream, init);

  const outHeaders = new Headers(resp.headers);
  if (key === "auth") {
    outHeaders.set("Cache-Control", "no-store");
  }
  return new Response(resp.body, {
    status: resp.status,
    statusText: resp.statusText,
    headers: outHeaders,
  });
}
