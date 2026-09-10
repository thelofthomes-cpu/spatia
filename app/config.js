// Public, client-safe configuration — the anon key is designed to be
// exposed in the browser; access control is enforced by Postgres row
// level security policies (see supabase/migrations), not by keeping
// this key secret.
//
// Fill these in from your Supabase project: Settings → API.
window.SPATIA_CONFIG = {
  SUPABASE_URL: 'https://jdundadbmqukvchosoqx.supabase.co',
  SUPABASE_ANON_KEY: 'YOUR-SUPABASE-ANON-PUBLIC-KEY',
};
