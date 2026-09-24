// Álbum Coletivo — cria a preferência de pagamento (R$39) no Mercado Pago e devolve o link do checkout.
// Mesma receita do Muraí/Revelê, adaptada pra tabela album_albuns. O organizador paga uma vez
// pra baixar tudo em alta / álbum permanente / sem marca.
const REF = "diemqzngskmcuytkzjhr";
const WEBHOOK_URL = `https://${REF}.supabase.co/functions/v1/mp-webhook-album`;
const SITE = "https://giogas-pm.github.io/album/";
const PRECO = 39;
const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};
function json(obj: unknown) {
  return new Response(JSON.stringify(obj), { headers: { ...CORS, "Content-Type": "application/json" } });
}
Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  try {
    const token = Deno.env.get("MP_ACCESS_TOKEN");
    if (!token) return json({ ok: false, motivo: "sem_token" });
    const { slug, titulo } = await req.json().catch(() => ({} as any));
    if (!slug) return json({ ok: false, motivo: "sem_slug" });
    const nome = ("Álbum Coletivo — " + (titulo || "fotos da festa")).slice(0, 240);
    const pref = {
      items: [{ title: nome, quantity: 1, unit_price: PRECO, currency_id: "BRL" }],
      external_reference: String(slug),
      metadata: { slug: String(slug) },
      statement_descriptor: "ALBUM",
      notification_url: WEBHOOK_URL,
      back_urls: {
        success: `${SITE}?pago=ok#a=${slug}`,
        pending: `${SITE}?pago=pendente#a=${slug}`,
        failure: `${SITE}?pago=falhou#a=${slug}`,
      },
      auto_return: "approved",
    };
    const r = await fetch("https://api.mercadopago.com/checkout/preferences", {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: "Bearer " + token },
      body: JSON.stringify(pref),
    });
    const j = await r.json();
    if (j && j.init_point) return json({ ok: true, init_point: j.init_point });
    return json({ ok: false, motivo: "mp_erro", detalhe: (j && (j.message || j.error)) || null });
  } catch (e) {
    return json({ ok: false, motivo: "excecao", detalhe: String(e) });
  }
});
