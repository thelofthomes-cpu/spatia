-- SPATIA core schema: workspaces, projects (digital twins), rooms, media,
-- leads, analytics events, and AI chat history.
-- Run this once in the Supabase SQL editor (or via `supabase db push`).

create extension if not exists pgcrypto;

-- ---------------------------------------------------------------------
-- Tables
-- ---------------------------------------------------------------------

create table if not exists workspaces (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  domain text,
  brand_accent text not null default '#111111',
  whatsapp_number text,
  brochure_url text,
  owner_id uuid not null references auth.users(id) on delete cascade,
  created_at timestamptz not null default now()
);

create table if not exists workspace_members (
  workspace_id uuid not null references workspaces(id) on delete cascade,
  user_id uuid not null references auth.users(id) on delete cascade,
  role text not null default 'owner' check (role in ('owner', 'editor', 'viewer')),
  created_at timestamptz not null default now(),
  primary key (workspace_id, user_id)
);

create table if not exists projects (
  id uuid primary key default gen_random_uuid(),
  workspace_id uuid not null references workspaces(id) on delete cascade,
  name text not null,
  description text,
  capture_type text not null default '360° panoramas',
  status text not null default 'DRAFT' check (status in ('DRAFT', 'PROCESSING', 'LIVE')),
  bedrooms int,
  bathrooms int,
  area_sqm numeric,
  has_pool boolean not null default false,
  parking_spaces int,
  created_at timestamptz not null default now()
);

create table if not exists rooms (
  id uuid primary key default gen_random_uuid(),
  project_id uuid not null references projects(id) on delete cascade,
  name text not null,
  room_type text,
  notes text,
  sort_order int not null default 0
);

create table if not exists project_media (
  id uuid primary key default gen_random_uuid(),
  project_id uuid not null references projects(id) on delete cascade,
  storage_path text not null,
  media_type text not null default 'photo',
  uploaded_at timestamptz not null default now()
);

create table if not exists leads (
  id uuid primary key default gen_random_uuid(),
  project_id uuid not null references projects(id) on delete cascade,
  name text,
  contact text,
  message text,
  source text not null default 'tour',
  created_at timestamptz not null default now()
);

create table if not exists analytics_events (
  id uuid primary key default gen_random_uuid(),
  project_id uuid not null references projects(id) on delete cascade,
  session_id text not null,
  event_type text not null check (event_type in ('view', 'whatsapp_click', 'brochure_download', 'ai_question', 'booking_request')),
  created_at timestamptz not null default now()
);

create table if not exists chat_messages (
  id uuid primary key default gen_random_uuid(),
  project_id uuid not null references projects(id) on delete cascade,
  session_id text not null,
  role text not null check (role in ('user', 'assistant')),
  content text not null,
  created_at timestamptz not null default now()
);

-- ---------------------------------------------------------------------
-- New user provisioning: create a workspace + a working demo property
-- so a freshly signed-up account has something real to look at.
-- ---------------------------------------------------------------------

create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer set search_path = public
as $$
declare
  new_workspace_id uuid;
  new_project_id uuid;
begin
  insert into workspaces (name, owner_id)
  values (coalesce(new.raw_user_meta_data ->> 'workspace_name', split_part(new.email, '@', 1) || '''s workspace'), new.id)
  returning id into new_workspace_id;

  insert into workspace_members (workspace_id, user_id, role)
  values (new_workspace_id, new.id, 'owner');

  insert into projects (workspace_id, name, description, status, bedrooms, bathrooms, area_sqm, has_pool, parking_spaces)
  values (
    new_workspace_id,
    'Villa A — Cantonments',
    'Demo digital twin, created automatically so you can try SPATIA AI and the public tour right away.',
    'LIVE', 4, 5, 420, true, 4
  )
  returning id into new_project_id;

  insert into rooms (project_id, name, room_type, sort_order) values
    (new_project_id, 'Living Room', 'living', 1),
    (new_project_id, 'Kitchen', 'kitchen', 2),
    (new_project_id, 'Master Bedroom', 'bedroom', 3),
    (new_project_id, 'Bedroom 2', 'bedroom', 4),
    (new_project_id, 'Pool', 'outdoor', 5);

  return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();

-- ---------------------------------------------------------------------
-- Row level security
-- ---------------------------------------------------------------------

alter table workspaces enable row level security;
alter table workspace_members enable row level security;
alter table projects enable row level security;
alter table rooms enable row level security;
alter table project_media enable row level security;
alter table leads enable row level security;
alter table analytics_events enable row level security;
alter table chat_messages enable row level security;

create or replace function public.is_workspace_member(p_workspace_id uuid)
returns boolean
language sql stable security definer set search_path = public
as $$
  select exists (
    select 1 from workspace_members
    where workspace_id = p_workspace_id and user_id = auth.uid()
  );
$$;

create or replace function public.project_workspace(p_project_id uuid)
returns uuid
language sql stable security definer set search_path = public
as $$
  select workspace_id from projects where id = p_project_id;
$$;

-- workspaces
create policy "members can view workspace" on workspaces
  for select using (is_workspace_member(id));
create policy "public can view workspace of a live project" on workspaces
  for select using (exists (select 1 from projects p where p.workspace_id = workspaces.id and p.status = 'LIVE'));
create policy "owner can update workspace" on workspaces
  for update using (owner_id = auth.uid());
create policy "authenticated can create own workspace" on workspaces
  for insert with check (owner_id = auth.uid());

-- workspace_members
create policy "members can view membership" on workspace_members
  for select using (is_workspace_member(workspace_id));

-- projects
create policy "public can view live projects" on projects
  for select using (status = 'LIVE');
create policy "members can view workspace projects" on projects
  for select using (is_workspace_member(workspace_id));
create policy "members can insert projects" on projects
  for insert with check (is_workspace_member(workspace_id));
create policy "members can update projects" on projects
  for update using (is_workspace_member(workspace_id));
create policy "members can delete projects" on projects
  for delete using (is_workspace_member(workspace_id));

-- rooms
create policy "public can view rooms of live projects" on rooms
  for select using (exists (select 1 from projects p where p.id = rooms.project_id and p.status = 'LIVE'));
create policy "members can view rooms" on rooms
  for select using (is_workspace_member(project_workspace(project_id)));
create policy "members can manage rooms" on rooms
  for all using (is_workspace_member(project_workspace(project_id)))
  with check (is_workspace_member(project_workspace(project_id)));

-- project_media
create policy "public can view media of live projects" on project_media
  for select using (exists (select 1 from projects p where p.id = project_media.project_id and p.status = 'LIVE'));
create policy "members can view media" on project_media
  for select using (is_workspace_member(project_workspace(project_id)));
create policy "members can manage media" on project_media
  for all using (is_workspace_member(project_workspace(project_id)))
  with check (is_workspace_member(project_workspace(project_id)));

-- leads: public can submit against a live project; only members can read them
create policy "anyone can submit a lead for a live project" on leads
  for insert with check (exists (select 1 from projects p where p.id = leads.project_id and p.status = 'LIVE'));
create policy "members can view leads" on leads
  for select using (is_workspace_member(project_workspace(project_id)));

-- analytics_events: public can log against a live project; only members can read them
create policy "anyone can log an event for a live project" on analytics_events
  for insert with check (exists (select 1 from projects p where p.id = analytics_events.project_id and p.status = 'LIVE'));
create policy "members can view analytics" on analytics_events
  for select using (is_workspace_member(project_workspace(project_id)));

-- chat_messages: only the ask-ai edge function (service role) ever writes
-- here; workspace members may read the transcripts for their own properties.
create policy "members can view chat messages" on chat_messages
  for select using (is_workspace_member(project_workspace(project_id)));

-- ---------------------------------------------------------------------
-- Aggregation RPC for the analytics chart (PostgREST can't GROUP BY)
-- ---------------------------------------------------------------------

create or replace function public.daily_views(p_workspace_id uuid, p_days int default 30)
returns table(day date, views bigint)
language plpgsql security definer set search_path = public
as $$
begin
  if not is_workspace_member(p_workspace_id) then
    raise exception 'not authorized';
  end if;

  return query
  select d::date, coalesce(count(ae.id), 0)
  from generate_series(current_date - (p_days - 1), current_date, interval '1 day') d
  left join projects p on p.workspace_id = p_workspace_id
  left join analytics_events ae
    on ae.project_id = p.id and ae.event_type = 'view' and ae.created_at::date = d::date
  group by d
  order by d;
end;
$$;

grant execute on function public.daily_views(uuid, int) to authenticated;

create or replace function public.workspace_metric_counts(p_workspace_id uuid, p_days int default 30)
returns table(
  unique_visitors bigint,
  tour_views bigint,
  whatsapp_clicks bigint,
  brochure_downloads bigint,
  ai_questions bigint,
  leads bigint
)
language plpgsql security definer set search_path = public
as $$
begin
  if not is_workspace_member(p_workspace_id) then
    raise exception 'not authorized';
  end if;

  return query
  select
    count(distinct ae.session_id) filter (
      where ae.event_type = 'view' and ae.created_at >= now() - (p_days || ' days')::interval
    ),
    count(*) filter (where ae.event_type = 'view'),
    count(*) filter (where ae.event_type = 'whatsapp_click'),
    count(*) filter (where ae.event_type = 'brochure_download'),
    count(*) filter (where ae.event_type = 'ai_question'),
    (select count(*) from leads l join projects p2 on p2.id = l.project_id where p2.workspace_id = p_workspace_id)
  from analytics_events ae
  join projects p on p.id = ae.project_id
  where p.workspace_id = p_workspace_id;
end;
$$;

grant execute on function public.workspace_metric_counts(uuid, int) to authenticated;

-- ---------------------------------------------------------------------
-- Storage: capture photos, uploaded to `captures/<project_id>/<file>`
-- ---------------------------------------------------------------------

insert into storage.buckets (id, name, public)
values ('captures', 'captures', true)
on conflict (id) do nothing;

create policy "members can upload captures" on storage.objects
  for insert with check (
    bucket_id = 'captures'
    and is_workspace_member(project_workspace(((storage.foldername(name))[1])::uuid))
  );

create policy "members can delete their captures" on storage.objects
  for delete using (
    bucket_id = 'captures'
    and is_workspace_member(project_workspace(((storage.foldername(name))[1])::uuid))
  );

create policy "public can view captures" on storage.objects
  for select using (bucket_id = 'captures');
