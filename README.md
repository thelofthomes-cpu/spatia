# SPATIA

Spatial intelligence for real estate — turn physical properties into interactive
digital twins with an AI assistant that understands every room.

This repo contains two front-ends:

- **`/` — Marketing website.** Public landing page: product overview, how it
  works, pricing, FAQ, and calls to action into the app.
- **`/app` — Product app.** The SPATIA workspace: dashboard, project
  (digital twin) management, the SPATIA AI demo, analytics, and settings.
  This is a realistic front-end prototype — data is in-memory and AI
  responses are canned, but the UI and flows represent the intended product.

## Run locally

No build step — serve the repo root with any static file server and open it
in a browser.

```
python3 -m http.server 8000
```

Then visit:
- `http://localhost:8000/` for the marketing site
- `http://localhost:8000/app/` for the workspace app

## Structure

```
index.html      marketing site
site.css        marketing site styles
site.js         marketing site nav behavior
app/index.html  workspace app
app/app.js      workspace app behavior (routing, projects, AI chat, modals)
app/styles.css  workspace app styles
```

## Included in this prototype

- Public marketing site (product, how it works, pricing, FAQ)
- Workspace dashboard
- Property/digital-twin project management
- New-project workflow
- Demo interactive twin viewer
- SPATIA AI property assistant (prototype responses)
- Analytics dashboard
- White-label/workspace settings
- Responsive UI across both site and app

## Production architecture to implement next

Next.js + TypeScript, Supabase/PostgreSQL, Cloudflare R2, Three.js, background
job queue, authentication, real 360 panorama ingestion, 3D reconstruction
provider/pipeline, LLM API, vector search, payments and production analytics.
