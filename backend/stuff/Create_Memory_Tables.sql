create extension if not exists vector
with schema extensions;

create table if not exists public.memories (
  id bigint generated always as identity
  primary key,

  user_id uuid not null,
  memory_type text not null default 'general',
  content text not null,

  person_name text,
  location text,
  event_at timestamptz,
  embedding extensions.vector(384),

  created_at timestamptz not null
    default now()

);

create table if not exists public.reminders (
  id bigint generated always as identity
    primary key,

  user_id UUID not null,
  memory_id bigint not null
    references public.memories(id)
    on delete cascade,

  remind_at timestamptz not null,
  completed boolean not null default false

);

create index if not exists memories_user_idx
on public.memories(user_id);

create index if not exists reminders_due_idx
on public.reminders(remind_at);

alter table public.memories
enable row level security;

alter table public.reminders
enable row level security;