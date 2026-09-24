// Álbum Coletivo — webhook do Mercado Pago. Pagamento aprovado desbloqueia o álbum
// (external_reference = slug) usando a service_role. Mesma receita do Muraí/Revelê.
Deno.serve(async (req) => {
  try {
    const token = Deno.env.get("MP_ACCESS_TOKEN");
    const SB_URL = Deno.env.get("SUPABASE_URL")!;
    const SVC = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
    const url = new URL(req.url);
    let pid: string | null = url.searchParams.get("data.id") || url.searchParams.get("id");
    let type: string | null = url.searchParams.get("type") || url.searchParams.get("topic");
    if (!pid || (type && type !== "payment")) {
      const b = await req.json().catch(() => null as any);
      if (b) { type = b.type || b.topic || type; pid = (b.data && b.data.id) || b.id || pid; }
    }
    if (!pid || (type && type !== "payment")) return new Response("ignored", { status: 200 });
    if (!token) return new Response("sem_token", { status: 200 });
    const pr = await fetch("https://api.mercadopago.com/v1/payments/" + encodeURIComponent(pid), {
      headers: { Authorization: "Bearer " + token },
    });
    const pay = await pr.json();
    if (pay && pay.status === "approved" && pay.external_reference) {
      await fetch(`${SB_URL}/rest/v1/album_albuns?slug=eq.${encodeURIComponent(pay.external_reference)}`, {
        method: "PATCH",
        headers: {
          apikey: SVC, Authorization: "Bearer " + SVC,
          "Content-Type": "application/json", Prefer: "return=minimal",
        },
        body: JSON.stringify({ unlocked: true }),
      });
    }
    return new Response("ok", { status: 200 });
  } catch (e) {
    return new Response("err:" + String(e), { status: 200 });
  }
});
