// EntropyGate AI — runtime config (Cloudflare Pages deploy)
// Same-origin /api/v1 is reverse-proxied + edge-cached by
// functions/api/[[route]].js, so domestic users never hit the Studio gateway.
window.API_BASE = "/api/v1";
