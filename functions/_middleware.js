// Test middleware - add X-Test header
export async function onRequest(context) {
  const { request, next } = context;
  const url = new URL(request.url);
  const pathname = url.pathname;
  
  // For API paths, add test header
  if (pathname.startsWith("/api/")) {
    const resp = new Response("test-ok", { status: 200 });
    resp.headers.set("X-Test-Middleware", "called");
    resp.headers.set("X-Path", pathname);
    resp.headers.set("Access-Control-Allow-Origin", "*");
    return resp;
  }
  
  // For non-API paths, pass through
  return next();
}