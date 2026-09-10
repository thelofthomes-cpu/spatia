import { isConfigured, loadSupabase } from './app/lib/supabaseClient.js';

let supabase = null;

const els = {
  loading: document.getElementById('loadingState'),
  notFound: document.getElementById('notFoundState'),
  content: document.getElementById('tourContent'),
  statusPill: document.getElementById('statusPill'),
  propName: document.getElementById('propName'),
  propDesc: document.getElementById('propDesc'),
  factRow: document.getElementById('factRow'),
  roomGrid: document.getElementById('roomGrid'),
  messages: document.getElementById('messages'),
  q: document.getElementById('q'),
  btnAsk: document.getElementById('btnAsk'),
  btnWhatsapp: document.getElementById('btnWhatsapp'),
  btnBrochure: document.getElementById('btnBrochure'),
  btnShare: document.getElementById('btnShare'),
  btnBookViewing: document.getElementById('btnBookViewing'),
  leadForm: document.getElementById('leadForm'),
  leadNote: document.getElementById('leadNote'),
};

function escapeHTML(s) {
  return String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

function getSessionId() {
  let id = localStorage.getItem('spatia_session_id');
  if (!id) {
    id = crypto.randomUUID();
    localStorage.setItem('spatia_session_id', id);
  }
  return id;
}

function logEvent(projectId, event_type) {
  supabase.from('analytics_events').insert({ project_id: projectId, session_id: getSessionId(), event_type }).then(() => {});
}

const projectId = new URLSearchParams(location.search).get('project');

async function init() {
  if (!isConfigured) {
    els.loading.hidden = true;
    els.notFound.hidden = false;
    els.notFound.querySelector('h1').textContent = 'This site is not configured yet';
    els.notFound.querySelector('p').textContent = 'The workspace owner needs to finish setting up SPATIA.';
    return;
  }
  if (!projectId) {
    els.loading.hidden = true;
    els.notFound.hidden = false;
    return;
  }

  try {
    supabase = await loadSupabase();
  } catch (e) {
    console.error(e);
    els.loading.hidden = true;
    els.notFound.hidden = false;
    els.notFound.querySelector('h1').textContent = "Couldn't load this tour";
    els.notFound.querySelector('p').textContent = 'Check your connection and reload the page.';
    return;
  }

  const { data: project, error } = await supabase
    .from('projects')
    .select('*')
    .eq('id', projectId)
    .eq('status', 'LIVE')
    .single();

  if (error || !project) {
    els.loading.hidden = true;
    els.notFound.hidden = false;
    return;
  }

  const { data: rooms } = await supabase.from('rooms').select('name').eq('project_id', projectId).order('sort_order');
  const { data: workspace } = await supabase.from('workspaces').select('whatsapp_number, brochure_url').eq('id', project.workspace_id).single();

  render(project, rooms ?? [], workspace);

  const viewedKey = `spatia_viewed_${projectId}`;
  if (!sessionStorage.getItem(viewedKey)) {
    logEvent(projectId, 'view');
    sessionStorage.setItem(viewedKey, '1');
  }
}

function render(project, rooms, workspace) {
  els.loading.hidden = true;
  els.content.hidden = false;
  els.statusPill.hidden = false;

  els.propName.textContent = project.name;
  els.propDesc.textContent = project.description || '';

  const facts = [];
  if (project.bedrooms) facts.push(`${project.bedrooms} bed`);
  if (project.bathrooms) facts.push(`${project.bathrooms} bath`);
  if (project.area_sqm) facts.push(`${project.area_sqm} m²`);
  if (project.has_pool) facts.push('Pool');
  if (project.parking_spaces) facts.push(`${project.parking_spaces} parking`);
  els.factRow.innerHTML = facts.map((f) => `<span class="fact">${escapeHTML(f)}</span>`).join('') || '<span class="fact">Details coming soon</span>';

  els.roomGrid.innerHTML = rooms.length
    ? rooms.map((r) => `<div class="room-chip" data-room="${escapeHTML(r.name)}">${escapeHTML(r.name.toUpperCase())}</div>`).join('')
    : '<p style="color:#888">Room layout coming soon.</p>';
  els.roomGrid.querySelectorAll('[data-room]').forEach((chip) =>
    chip.addEventListener('click', () => ask(`Tell me about the ${chip.dataset.room}`))
  );

  if (workspace?.whatsapp_number) {
    const digits = workspace.whatsapp_number.replace(/[^0-9]/g, '');
    els.btnWhatsapp.href = `https://wa.me/${digits}?text=${encodeURIComponent(`Hi, I'm interested in ${project.name}`)}`;
    els.btnWhatsapp.hidden = false;
    els.btnWhatsapp.addEventListener('click', () => logEvent(project.id, 'whatsapp_click'));
  }
  if (workspace?.brochure_url) {
    els.btnBrochure.href = workspace.brochure_url;
    els.btnBrochure.hidden = false;
    els.btnBrochure.addEventListener('click', () => logEvent(project.id, 'brochure_download'));
  }

  els.btnBookViewing.addEventListener('click', () => {
    document.getElementById('leadForm').scrollIntoView({ behavior: 'smooth', block: 'center' });
    document.getElementById('leadMessage').value ||= `I'd like to book a viewing for ${project.name}.`;
    document.getElementById('leadName').focus();
    logEvent(project.id, 'booking_request');
  });

  els.btnShare.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(location.href);
      const original = els.btnShare.textContent;
      els.btnShare.textContent = 'Link copied!';
      setTimeout(() => (els.btnShare.textContent = original), 1600);
    } catch {
      /* clipboard unavailable — nothing to fall back to on a static page */
    }
  });

  els.leadForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const submitBtn = els.leadForm.querySelector('button[type="submit"]');
    submitBtn.disabled = true;
    const { error } = await supabase.from('leads').insert({
      project_id: project.id,
      name: document.getElementById('leadName').value.trim(),
      contact: document.getElementById('leadContact').value.trim(),
      message: document.getElementById('leadMessage').value.trim(),
      source: 'tour',
    });
    if (error) {
      els.leadNote.textContent = "Something went wrong — please try again.";
    } else {
      els.leadForm.reset();
      els.leadNote.textContent = "Thanks — we'll be in touch shortly.";
    }
    submitBtn.disabled = false;
  });

  els.btnAsk.addEventListener('click', () => ask());
  els.q.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') ask();
  });
  document.querySelectorAll('.quick button').forEach((b) => b.addEventListener('click', () => ask(b.dataset.q)));

  function addMsg(t, c) {
    const d = document.createElement('div');
    d.className = c;
    d.textContent = t;
    els.messages.appendChild(d);
    els.messages.scrollTop = 999999;
  }

  async function ask(text) {
    const q = text || els.q.value.trim();
    if (!q) return;
    addMsg(q, 'user');
    els.q.value = '';
    const { data, error } = await supabase.functions.invoke('ask-ai', {
      body: { projectId: project.id, sessionId: getSessionId(), message: q },
    });
    addMsg(error || data?.error ? data?.error || "Sorry, I couldn't reach SPATIA AI just now." : data.reply, 'bot');
  }
}

init();
