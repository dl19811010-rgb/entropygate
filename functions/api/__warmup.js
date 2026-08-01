// Warm-up endpoint: called by the cron job to keep the backend alive.
// Returns immediately without upstream call — the mere presence of this
// file triggers the CF Pages function runtime to stay warm.
export async function onRequest(context) {
  return new Response("ok", { status: 200 });
}