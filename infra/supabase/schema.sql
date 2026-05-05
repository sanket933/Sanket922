create extension if not exists vector;
create extension if not exists pgcrypto;

create table workspaces (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  human_approval_required boolean not null default true,
  created_at timestamptz not null default now()
);

create type approval_status as enum ('pending','ceo_approved','ops_approved','human_required','rejected','dispatched');
create type action_type as enum ('social_post','reel_publish','email_send','dm_send','lead_research','analytics_sync');

create table approval_items (
  id uuid primary key default gen_random_uuid(),
  workspace_id uuid not null references workspaces(id) on delete cascade,
  action_type action_type not null,
  platform text,
  target text,
  payload jsonb not null,
  rationale text not null,
  risk_score numeric(4,3) not null default 0,
  status approval_status not null default 'pending',
  ceo_reason text,
  ops_reason text,
  approved_by uuid,
  scheduled_for timestamptz,
  dispatched_at timestamptz,
  created_at timestamptz not null default now()
);

create table leads (
  id uuid primary key default gen_random_uuid(),
  workspace_id uuid not null references workspaces(id) on delete cascade,
  company_name text not null,
  website text,
  social_url text,
  pain_points jsonb not null default '[]',
  score numeric(4,3) not null default 0,
  status text not null default 'new',
  last_contacted_at timestamptz,
  created_at timestamptz not null default now(),
  unique(workspace_id, website)
);

create table conversations (
  id uuid primary key default gen_random_uuid(),
  workspace_id uuid not null references workspaces(id) on delete cascade,
  lead_id uuid references leads(id) on delete cascade,
  channel text not null,
  direction text not null check (direction in ('inbound','outbound')),
  subject text,
  body text not null,
  provider_message_id text,
  created_at timestamptz not null default now()
);

create table content_assets (
  id uuid primary key default gen_random_uuid(),
  workspace_id uuid not null references workspaces(id) on delete cascade,
  platform text not null,
  format text not null,
  hook text not null,
  body text,
  cta text,
  media_url text,
  status text not null default 'draft',
  created_at timestamptz not null default now()
);

create table analytics_events (
  id uuid primary key default gen_random_uuid(),
  workspace_id uuid not null references workspaces(id) on delete cascade,
  source text not null,
  entity_id uuid,
  metrics jsonb not null,
  occurred_at timestamptz not null default now()
);

create table memories (
  id uuid primary key default gen_random_uuid(),
  workspace_id uuid not null references workspaces(id) on delete cascade,
  kind text not null,
  content text not null,
  metadata jsonb not null default '{}',
  embedding vector(1536),
  created_at timestamptz not null default now()
);

create table audit_logs (
  id uuid primary key default gen_random_uuid(),
  workspace_id uuid references workspaces(id) on delete cascade,
  actor text not null,
  action text not null,
  entity_type text,
  entity_id uuid,
  metadata jsonb not null default '{}',
  created_at timestamptz not null default now()
);

create index memories_embedding_idx on memories using ivfflat (embedding vector_cosine_ops) with (lists = 100);
create index approval_items_status_idx on approval_items(status, scheduled_for);
create index analytics_events_source_idx on analytics_events(workspace_id, source, occurred_at desc);
