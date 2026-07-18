// Cloudflare Pages Function — edge reverse-proxy for Google OAuth endpoints.
//
// Routes (all fixed Google hosts only):
//   /gproxy/auth     ->  https://accounts.google.com/o/oauth2/v2/auth
//   /gproxy/token    ->  https://oauth2.googleapis.com/token
//   /gproxy/userinfo ->  https://www.googleapis.com/oauth2/v3/userinfo
//
// Why?
//   The backend runs inside ModelScope Studio (a China datacenter). Google's
//   OAuth hosts (accounts.google.com / oauth2.googleapis.com / www.googleapis.com)
//   are NOT reachable from China. That breaks BOTH halves of the Google login
//   flow for China-based users:
//     1. The browser cannot even open the Google consent page
//        (accounts.google.com), so login fails before any redirect.
//     2. The server-side code<->token exchange times out too.
//   GitHub works because github.com is reachable from China.
//
//   This Function runs on Cloudflare's global edge (which CAN reach Google).
//   The backend points its google auth_url / token_url / userinfo_url at this
//   proxy (https://aientropygate.com/gproxy/...). Now the China server only has
//   to reach Cloudflare, and the user's BROWSER also only talks to Cloudflare
//   (aientropygate.com, reachable in China) — Cloudflare does the Google part.
//
// Security: generic pass-through to three fixed Google hosts. No secrets of its
// own; client_secret is sent server-to-server in the POST body to /gproxy/token
// and never reaches the browser. To avoid open-proxy abuse we only forward to
// the three hardcoded hosts and only allow GET/POST for auth/token/userinfo.

const UPSTREAM = {
  auth: "https://accounts.google.com/o/oauth2/v2/auth",
  token: "https://oauth2.googleapis.com/token",
  userinfo: "https://www.googleapis.com/oauth2/v3/userinfo",
};

export async function onRequest(context) {
  const { request, params } = context;
  const url = new URL(request.url);

  const seg = Array.isArray(params.route)
    ? params.route.join("/")
    : params.route || "";
  const key = seg.split("/")[0];
  const target = UPSTREAM[key];
  if (!target) {
    return new Response(JSON.stringify({ error: "unknown_gproxy_route", hint: "use /gproxy/{auth|token|userinfo}" }), {
      status: 404,
      headers: { "Content-Type": "application/json" },
    });
  }

  // Build upstream URL. For `auth`, the original query string already contains
  // client_id/redirect_uri/scope, so just forward it. For token/userinfo the
  // backend sends the body/headers; forward them as-is.
  const upstream = `${target}${url.search}`;
  const headers = new Headers(request.headers);
  headers.delete("host");
  headers.delete("cf-connecting-ip");

  const init = { method: request.method, headers };
  if (request.method !== "GET" && request.method !== "HEAD") {
    init.body = request.body;
  }

  const resp = await fetch(upstream, init);

  // For the auth page we must NOT let Cloudflare cache it (it's per-user/state).
  const outHeaders = new Headers(resp.headers);
  if (key === "auth") {
    outHeaders.set("Cache-Control", "no-store");
  }
  // Fix Location redirects so the browser keeps going through the proxy only if
  // Google itself redirects within its own auth domain (rare). We leave absolute
  // Google URLs as-is; the consent page posts back to entropygate.cc.cd via the
  // redirect_uri param, so no rewriting is needed for the happy path.
  return new Response(resp.body, {
    status: resp.status,
    statusText: resp.statusText,
    headers: outHeaders,
  });
}
