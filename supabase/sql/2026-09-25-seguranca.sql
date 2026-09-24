-- P0 de segurança (squad 2026-09-24): fim da listagem anônima de álbuns/fotos e dos originais públicos.
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('album-orig', 'album-orig', false, 26214400, array['image/*'])
on conflict (id) do update set public = false, file_size_limit = 26214400, allowed_mime_types = array['image/*'];
update storage.buckets set file_size_limit = 5242880, allowed_mime_types = array['image/jpeg'] where id = 'album-fotos';

drop policy if exists album_storage_sel on storage.objects;          -- sem listagem do bucket de previews
drop policy if exists album_orig_ins on storage.objects;
create policy album_orig_ins on storage.objects for insert to anon with check (bucket_id = 'album-orig');

drop policy if exists album_fotos_sel on public.album_fotos;          -- sem SELECT anônimo nas tabelas
drop policy if exists album_albuns_sel on public.album_albuns;

create or replace function public.album_get(p_slug text) returns json
language sql stable security definer set search_path = public as $$
  select json_build_object(
    'id', a.id, 'slug', a.slug, 'title', a.title, 'host_name', a.host_name,
    'unlocked', a.unlocked, 'created_at', a.created_at,
    'fotos', coalesce((select json_agg(json_build_object('id', f.id, 'preview_path', f.preview_path, 'created_at', f.created_at)
                                       order by f.created_at desc)
                       from album_fotos f where f.album_id = a.id), '[]'::json))
  from album_albuns a where a.slug = p_slug
$$;
revoke all on function public.album_get(text) from public;
grant execute on function public.album_get(text) to anon, authenticated;
