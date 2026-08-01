// Test middleware
export async function onRequest(context) {
  const { request, next } = context;
  const url = new URL(request.url);
  if (url.pathname.startsWith("/api/")) {
    return new Response(JSON.stringify({test: "ok", path: url.pathname}), {
      status: 200,
      headers: {"Content-Type": "application/json", "X-Test": "called"}
    });
  }
  return next();
}