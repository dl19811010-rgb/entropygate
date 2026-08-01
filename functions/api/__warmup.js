// Warm-up: keep the backend alive
export async function onRequest(context) {
  const url = new URL(context.request.url);
  if (url.pathname === "/api/__warmup") {
    try {
      await fetch("https://api-tunnel.aientropygate.com/api/v1/health", {
        method: "GET",
        headers: { "Accept": "application/json" },
        signal: AbortSignal.timeout(25000),
      });
    } catch (e) {}
    return new Response("ok", { status: 200 });
  }
  return new Response("Not found", { status: 404 });
}