// SPATIA AI — answers buyer/tenant questions about a published property
// using its real spatial data, backed by the Claude API.
//
// Deploy: supabase functions deploy ask-ai
// Secret: supabase secrets set ANTHROPIC_API_KEY=sk-ant-...
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};

function json(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...corsHeaders, "content-type": "application/json" },
  });
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: corsHeaders });

  let payload: { projectId?: string; sessionId?: string; message?: string };
  try {
    payload = await req.json();
  } catch {
    return json({ error: "Invalid JSON body" }, 400);
  }

  const { projectId, message } = payload;
  const sessionId = payload.sessionId || "anon";

  if (!projectId || !message || !message.trim()) {
    return json({ error: "projectId and message are required" }, 400);
  }

  const supabaseUrl = Deno.env.get("SUPABASE_URL");
  const serviceRoleKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");
  const anthropicKey = Deno.env.get("ANTHROPIC_API_KEY");

  if (!supabaseUrl || !serviceRoleKey) {
    return json({ error: "Server misconfigured (missing Supabase service credentials)" }, 500);
  }
  if (!anthropicKey) {
    return json({ error: "SPATIA AI is not configured yet (missing ANTHROPIC_API_KEY)" }, 500);
  }

  const supabase = createClient(supabaseUrl, serviceRoleKey);

  const { data: project, error: projectErr } = await supabase
    .from("projects")
    .select("id, name, description, status, bedrooms, bathrooms, area_sqm, has_pool, parking_spaces")
    .eq("id", projectId)
    .single();

  if (projectErr || !project) return json({ error: "Property not found" }, 404);
  if (project.status !== "LIVE") return json({ error: "This property is not published" }, 403);

  const { data: rooms } = await supabase
    .from("rooms")
    .select("name, room_type, notes")
    .eq("project_id", projectId)
    .order("sort_order");

  const roomList = (rooms ?? [])
    .map((r) => `${r.name}${r.room_type ? ` (${r.room_type})` : ""}${r.notes ? ` — ${r.notes}` : ""}`)
    .join("; ") || "not itemized";

  const system = `You are SPATIA AI, an assistant embedded in the digital twin tour of a real property. Answer only using the property data given below — never invent details. If the answer isn't in the data, say you don't have that information and suggest contacting the agent. Keep answers short (1-3 sentences), friendly, and factual.

Property: ${project.name}
Description: ${project.description ?? "n/a"}
Bedrooms: ${project.bedrooms ?? "unknown"}
Bathrooms: ${project.bathrooms ?? "unknown"}
Area: ${project.area_sqm ? project.area_sqm + " m²" : "unknown"}
Pool: ${project.has_pool ? "yes" : "no"}
Parking spaces: ${project.parking_spaces ?? "unknown"}
Rooms: ${roomList}`;

  let reply: string;
  try {
    const aiRes = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "content-type": "application/json",
        "x-api-key": anthropicKey,
        "anthropic-version": "2023-06-01",
      },
      body: JSON.stringify({
        model: "claude-sonnet-5",
        max_tokens: 300,
        system,
        messages: [{ role: "user", content: message.slice(0, 2000) }],
      }),
    });

    if (!aiRes.ok) {
      console.error("Anthropic error", aiRes.status, await aiRes.text());
      return json({ error: "AI request failed" }, 502);
    }

    const aiJson = await aiRes.json();
    reply = aiJson.content?.[0]?.text ?? "Sorry, I couldn't come up with an answer for that.";
  } catch (e) {
    console.error(e);
    return json({ error: "AI request failed" }, 502);
  }

  await supabase.from("chat_messages").insert([
    { project_id: projectId, session_id: sessionId, role: "user", content: message },
    { project_id: projectId, session_id: sessionId, role: "assistant", content: reply },
  ]);
  await supabase.from("analytics_events").insert({
    project_id: projectId,
    session_id: sessionId,
    event_type: "ai_question",
  });

  return json({ reply });
});
