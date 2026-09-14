# SPATIA

Spatial intelligence for real estate — turn physical properties into interactive
digital twins with an AI assistant that understands every room.

## Architecture

- **Frontend** — static HTML/CSS/JS (no build step), deployed to **GitHub Pages**.
  - `/` — public marketing site.
  - `/app` — the SPATIA workspace (sign-in, dashboard, projects, AI, leads, analytics, settings).
  - `/tour.html` — the public digital-twin viewer buyers/tenants see (no login), linked from a published project.
- **Backend** — [Supabase](https://supabase.com): Postgres database, auth, file storage,
  and one Edge Function, all defined as code in `/supabase`.
  - `supabase/migrations/` — the full schema, row-level security policies, and a
    trigger that provisions a workspace + a working demo property for every new signup.
  - `supabase/functions/ask-ai/` — SPATIA AI. Reads a property's real data from
    the database and answers questions using the Claude API.

The static frontend talks to Supabase directly from the browser using the
public anon key — that's the intended Supabase model. Access control is
enforced by Postgres row-level security (see the migration), not by keeping
that key secret. The Anthropic API key is a real secret and only ever lives
server-side, as a Supabase Edge Function secret.

## One-time setup

You already have a Supabase project (`jdundadbmqukvchosoqx`). To wire everything up:

### 1. Run the database migration

Open your project's [SQL Editor](https://supabase.com/dashboard/project/jdundadbmqukvchosoqx/sql/new)
and run the contents of `supabase/migrations/20260101000000_init.sql`.

This creates every table, the row-level security policies, the auto-provisioning
trigger (new signups get a workspace + a live demo property automatically), the
analytics RPC functions, and the `captures` storage bucket.

### 2. Deploy the AI edge function

Install the [Supabase CLI](https://supabase.com/docs/guides/cli), then from the
repo root:

```bash
supabase login
supabase link --project-ref jdundadbmqukvchosoqx
supabase functions deploy ask-ai
supabase secrets set ANTHROPIC_API_KEY=sk-ant-...
```

Get an Anthropic API key from [console.anthropic.com](https://console.anthropic.com).
Never commit this key — it's set purely as a Supabase secret, which is only
readable inside the Edge Function runtime.

### 3. Fill in the public config

Open **Settings → API** in your Supabase dashboard and copy the **Project URL**
and **anon public key** into `app/config.js`:

```js
window.SPATIA_CONFIG = {
  SUPABASE_URL: 'https://jdundadbmqukvchosoqx.supabase.co',
  SUPABASE_ANON_KEY: 'paste-your-anon-public-key-here',
};
```

Commit this file. The anon key is meant to be public — see Architecture above.

### 4. Enable GitHub Pages

In the repo, go to **Settings → Pages** and set **Source** to **GitHub Actions**
(one-time). The included workflow (`.github/workflows/pages.yml`) then builds
and deploys the site automatically on every push to this branch.

Once deployed, the site is live at:
`https://<your-github-username>.github.io/spatia/`

> Note: GitHub Pages for a **private** repository requires a GitHub plan that
> supports it (Pro/Team/Enterprise); on the free plan, make the repo public or
> keep using it locally.

## Run locally

No build step — serve the repo root with any static file server:

```bash
python3 -m http.server 8000
```

- `http://localhost:8000/` — marketing site
- `http://localhost:8000/app/` — workspace app
- `http://localhost:8000/tour.html?project=<id>` — public tour of a given property

Without `app/config.js` filled in, the app and tour page still load and show a
"backend not configured" notice instead of crashing.

## What's real vs. what's still a placeholder

**Real, working end to end:**
- Email/password auth, one workspace per account, row-level-security-scoped data
- Projects (digital twins) stored in Postgres — create, publish/unpublish
- Capture photo uploads to Supabase Storage
- SPATIA AI answering from each property's actual room/listing data via the Claude API
- Public tour page with room browsing, AI chat, WhatsApp/brochure click-outs, and lead capture
- Leads and analytics (views, WhatsApp clicks, brochure downloads, AI questions) — real counts and a real 30-day chart from logged events

**Still a placeholder** (needs a specialized pipeline/provider, out of scope for this pass):
- Actual 3D/LiDAR reconstruction from uploaded captures — projects go LIVE manually, not after real processing
- Payments/billing
- Custom-domain white-labelling (the field exists in Settings; DNS/proxying isn't wired up)

## Repo structure

```
index.html, site.css, site.js, hero3d.js     marketing site (hero3d.js: real-time 3D hero walkthrough)
app/index.html, app.js, styles.css, config.js, lib/   workspace app
tour.html, tour.css, tour.js      public digital-twin viewer
supabase/migrations/              database schema + RLS policies
supabase/functions/ask-ai/        SPATIA AI edge function
.github/workflows/pages.yml       GitHub Pages deploy
```
