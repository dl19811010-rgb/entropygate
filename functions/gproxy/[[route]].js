// Cloudflare Pages Function — edge reverse-proxy for Google OAuth endpoints.
//
// Route:  /gproxy/token     ->  https://oauth2.googleapis.com/token
//         /gproxy/userinfo  ->  https://www.googleapis.com/oauth2/v3/userinfo
//
// Why?
//   The backend runs inside ModelScope Studio (a China datacenter). Google's
//   OAuth token/userinfo hosts (oauth2.googleapis.com / www.googleapis.com) are
//   NOT reachable from China, so the server-side authorization-code exchange
//   times out and Google login fails with `token_exchange_failed` — even though
//   the browser side (accounts.google.com) works and GitHub login (github.com,
//   reachable from China) works fine.
//
//   This Function runs on Cloudflare's global edge, which CAN reach Google. The
//   backend points its google token_url / userinfo_url at this proxy
//   (https://aientropygate.com/gproxy/...), so the China server only has to
//   reach Cloudflare (reachable) and Cloudflare talks to Google.
//
// Security: this proxy is generic pass-through to two fixed Google hosts only.
// It carries no secrets of its own; the client_secret is sent by the backend in
// the POST body (server-to-server, never exposed to the browser).

const UPSTREAM = {
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
    return new Response(JSON.stringify({ error: "unknown_gproxy_route" }), {
      status: 404,
      headers: { "Content-Type": "application/json" },
    });
  }

  const upstream = `${target}${url.search}`;
  const headers = new Headers(request.headers);
  headers.delete("host");

  const init = { method: request.method, headers };
  if (request.method !== "GET" && request.method !== "HEAD") {
    init.body = request.body;
  }
  return fetch(upstream, init);
}
