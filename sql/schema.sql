-- Run in Supabase SQL Editor. text-embedding-3-small creates 1536-dimensional vectors.
create extension if not exists vector;
create table if not exists public.documents (
    id bigint generated always as identity primary key,
    source text not null,
    chunk_index integer not null,
    content text not null,
    embedding vector(1536) not null,
    created_at timestamptz not null default now(),
    unique(source, chunk_index)
);
-- Restrict direct client access; the demo API uses a server-side service role key.
alter table public.documents enable row level security;

create or replace function public.match_documents(
    query_embedding vector(1536), match_count integer default 5
)
returns table (source text, content text, similarity float)
language sql stable
as $$
    select d.source, d.content,
           1 - (d.embedding <=> query_embedding) as similarity
    from public.documents d
    order by d.embedding <=> query_embedding
    limit least(greatest(match_count, 1), 20);
$$;
-- For a real deployment, tighten EXECUTE grants, add user auth, and restrict
-- service keys to your private backend. Avoid exposing RPC to public clients.
revoke all on function public.match_documents(vector(1536), integer) from public, anon, authenticated;
