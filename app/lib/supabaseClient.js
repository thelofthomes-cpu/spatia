const cfg = window.SPATIA_CONFIG || {};

export const isConfigured =
  !!cfg.SUPABASE_URL &&
  !!cfg.SUPABASE_ANON_KEY &&
  !cfg.SUPABASE_ANON_KEY.startsWith('YOUR-');

// Loaded lazily (and only once configured) so a blocked/slow CDN request
// fails as a catchable rejection instead of aborting the whole page script.
export async function loadSupabase() {
  const { createClient } = await import('https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/+esm');
  return createClient(cfg.SUPABASE_URL, cfg.SUPABASE_ANON_KEY);
}
