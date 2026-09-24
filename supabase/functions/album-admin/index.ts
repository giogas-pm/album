// Álbum Coletivo — ações de DONO do álbum (remover foto), autenticadas por admin_key.
// O dono guarda a admin_key localmente e na URL (#a=slug&k=...). Remove a linha E os
// objetos no Storage (master + preview). Mesma receita do Muraí/Revelê (mural-admin).
const SB_URL = Deno.env.get("SUPABASE_URL")!;
const SVC = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const BUCKET = "album-fotos"; // previews (público)
const BUCKET_ORIG = "album-orig"; // originais (privado)
const H = { apikey: SVC, Authorization: "Bearer " + SVC, "Content-Type": "application/json" };
const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};
function json(obj: unknown, status = 200) {
  return new Response(JSON.stringify(obj), { status, headers: { ...CORS, "Content-Type": "application/json" } });
}
Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  try {
    const { slug, key, action, foto_id } = await req.json().catch(() => ({} as any));
    if (!slug || !key) return json({ ok: false, motivo: "faltam_dados" }, 400);
    const rows = await fetch(
      `${SB_URL}/rest/v1/album_albuns?slug=eq.${encodeURIComponent(slug)}&select=id,admin_key,unlocked`,
      { headers: H },
    ).then((r) => r.json());
    if (!rows.length) return json({ ok: false, motivo: "album_inexistente" }, 404);
    if (!rows[0].admin_key || rows[0].admin_key !== key) return json({ ok: false, motivo: "nao_autorizado" }, 403);
    const albumId = rows[0].id;
    if (action === "delete_foto") {
      if (!foto_id) return json({ ok: false, motivo: "sem_foto" }, 400);
      // busca os caminhos antes de apagar a linha
      const fr = await fetch(
        `${SB_URL}/rest/v1/album_fotos?id=eq.${encodeURIComponent(foto_id)}&album_id=eq.${albumId}&select=storage_path,preview_path`,
        { headers: H },
      ).then((r) => r.json());
      if (fr.length) {
        for (const [bucket, path] of [[BUCKET_ORIG, fr[0].storage_path], [BUCKET, fr[0].preview_path]]) {
          if (!path) continue;
          await fetch(`${SB_URL}/storage/v1/object/${bucket}`, {
            method: "DELETE", headers: H, body: JSON.stringify({ prefixes: [path] }),
          }).catch(() => {});
        }
      }
      await fetch(
        `${SB_URL}/rest/v1/album_fotos?id=eq.${encodeURIComponent(foto_id)}&album_id=eq.${albumId}`,
        { method: "DELETE", headers: { ...H, Prefer: "return=minimal" } },
      );
      return json({ ok: true });
    }
    if (action === "originals") {
      // download em alta: só dono + álbum pago; links assinados de 1h no bucket privado
      if (!rows[0].unlocked) return json({ ok: false, motivo: "nao_pago" }, 402);
      const fs = await fetch(
        `${SB_URL}/rest/v1/album_fotos?album_id=eq.${albumId}&select=storage_path&order=created_at.asc`,
        { headers: H },
      ).then((r) => r.json());
      const paths = fs.map((f: any) => f.storage_path).filter(Boolean);
      if (!paths.length) return json({ ok: true, urls: [] });
      const signed = await fetch(`${SB_URL}/storage/v1/object/sign/${BUCKET_ORIG}`, {
        method: "POST", headers: H, body: JSON.stringify({ expiresIn: 3600, paths }),
      }).then((r) => r.json());
      const urls = (Array.isArray(signed) ? signed : []).filter((x: any) => x.signedURL)
        .map((x: any) => `${SB_URL}/storage/v1${x.signedURL}`);
      return json({ ok: true, urls });
    }
    return json({ ok: false, motivo: "acao_desconhecida" }, 400);
  } catch (e) {
    return json({ ok: false, motivo: "excecao", detalhe: String(e) }, 200);
  }
});
