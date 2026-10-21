-- Tabelas Itapecuru Baladas
create extension if not exists "pgcrypto";

create table eventos (
  id uuid default gen_random_uuid() primary key,
  nome text not null,
  cidade text not null,
  descricao text,
  data_evento date,
  produtor_nome text,
  produtor_telegram_id bigint,
  status text default 'rascunho',
  created_at timestamp default now()
);

create table fotos (
  id uuid default gen_random_uuid() primary key,
  evento_id uuid references eventos(id) on delete cascade,
  url_original text,
  url_watermark text,
  legenda text,
  created_at timestamp default now()
);

create table flyers (
  id uuid default gen_random_uuid() primary key,
  titulo text not null,
  cidade text not null,
  data_evento date,
  local text,
  imagem_url text,
  link text,
  status text default 'ativo',
  created_at timestamp default now()
);

create table noticias_musica (
  id uuid default gen_random_uuid() primary key,
  titulo text not null,
  resumo text,
  categoria text, -- Sertanejo, Forró, Piseiro, etc
  imagem_url text,
  fonte text,
  link_externo text,
  created_at timestamp default now()
);

-- RLS
alter table eventos enable row level security;
alter table fotos enable row level security;
alter table flyers enable row level security;
alter table noticias_musica enable row level security;

create policy "public read aprovados" on eventos for select using (status = 'aprovado');
create policy "public read fotos" on fotos for select using (true);
create policy "public read flyers" on flyers for select using (status = 'ativo');
create policy "public read noticias" on noticias_musica for select using (true);
create policy "service all" on eventos for all using (true) with check (true);
create policy "service fotos all" on fotos for all using (true) with check (true);
create policy "service flyers all" on flyers for all using (true) with check (true);
create policy "service noticias all" on noticias_musica for all using (true) with check (true);
