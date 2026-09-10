import { isConfigured, loadSupabase } from './lib/supabaseClient.js';

let supabase = null;

const els = {
  configBanner: document.getElementById('configBanner'),
  authScreen: document.getElementById('authScreen'),
  appShell: document.getElementById('appShell'),
  authForm: document.getElementById('authForm'),
  authEmail: document.getElementById('authEmail'),
  authPassword: document.getElementById('authPassword'),
  authError: document.getElementById('authError'),
  authSubmit: document.getElementById('authSubmit'),
  authToggle: document.getElementById('authToggle'),
  workspaceName: document.getElementById('workspaceName'),
  projectList: document.getElementById('projectList'),
  allProjects: document.getElementById('allProjects'),
  dashboardStats: document.getElementById('dashboardStats'),
  aiLog: document.getElementById('aiLog'),
  aiProjectSelect: document.getElementById('aiProjectSelect'),
  roomChips: document.getElementById('roomChips'),
  messages: document.getElementById('messages'),
  q: document.getElementById('q'),
  leadsTable: document.getElementById('leadsTable').querySelector('tbody'),
  analyticsStats: document.getElementById('analyticsStats'),
  bars: document.getElementById('bars'),
  settingsForm: document.getElementById('settingsForm'),
  settingsName: document.getElementById('settingsName'),
  settingsDomain: document.getElementById('settingsDomain'),
  settingsWhatsapp: document.getElementById('settingsWhatsapp'),
  settingsBrochure: document.getElementById('settingsBrochure'),
  settingsAccent: document.getElementById('settingsAccent'),
  settingsSaved: document.getElementById('settingsSaved'),
  btnOpenDemo: document.getElementById('btnOpenDemo'),
  modal: document.getElementById('modal'),
  modalContent: document.getElementById('modalContent'),
};

let workspace = null;
let projects = [];
let authMode = 'signin';

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

function timeAgo(iso) {
  const s = Math.max(1, Math.round((Date.now() - new Date(iso).getTime()) / 1000));
  if (s < 60) return `${s}s ago`;
  const m = Math.round(s / 60);
  if (m < 60) return `${m}m ago`;
  const h = Math.round(m / 60);
  if (h < 24) return `${h}h ago`;
  return `${Math.round(h / 24)}d ago`;
}

function openModal(html) {
  els.modalContent.innerHTML = html;
  els.modal.style.display = 'grid';
}
function closeModal() {
  els.modal.style.display = 'none';
}

function show(id) {
  document.querySelectorAll('.view').forEach((v) => v.classList.remove('active-view'));
  document.getElementById(id).classList.add('active-view');
  document.querySelectorAll('nav a').forEach((a) => a.classList.toggle('active', a.getAttribute('href') === '#' + id));
  location.hash = id;
  if (id === 'analytics') loadAnalytics();
  if (id === 'leads') loadLeads();
}

// ---------------------------------------------------------------------
// Auth
// ---------------------------------------------------------------------

async function initAuth() {
  const { data: { session } } = await supabase.auth.getSession();
  if (session) {
    await enterApp();
  } else {
    els.authScreen.hidden = false;
  }

  supabase.auth.onAuthStateChange((_event, session) => {
    if (session && els.appShell.hidden) enterApp();
    if (!session) {
      els.appShell.hidden = true;
      els.authScreen.hidden = false;
    }
  });
}

els.authToggle.addEventListener('click', (e) => {
  e.preventDefault();
  authMode = authMode === 'signin' ? 'signup' : 'signin';
  els.authSubmit.textContent = authMode === 'signin' ? 'Sign in' : 'Create account';
  els.authToggle.textContent = authMode === 'signin' ? 'Create one' : 'Sign in instead';
  els.authToggle.previousSibling.textContent = authMode === 'signin' ? 'No account yet? ' : 'Already have one? ';
});

els.authForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  els.authError.hidden = true;
  els.authSubmit.disabled = true;
  const email = els.authEmail.value.trim();
  const password = els.authPassword.value;
  try {
    if (authMode === 'signin') {
      const { error } = await supabase.auth.signInWithPassword({ email, password });
      if (error) throw error;
    } else {
      const { data, error } = await supabase.auth.signUp({ email, password });
      if (error) throw error;
      if (!data.session) {
        els.authError.style.background = '#eef7ee';
        els.authError.style.color = '#2e7d32';
        els.authError.textContent = 'Account created — check your email to confirm it, then sign in.';
        els.authError.hidden = false;
      }
    }
  } catch (err) {
    els.authError.style.background = '';
    els.authError.style.color = '';
    els.authError.textContent = err.message || 'Something went wrong.';
    els.authError.hidden = false;
  } finally {
    els.authSubmit.disabled = false;
  }
});

document.getElementById('btnSignOut').addEventListener('click', () => supabase.auth.signOut());

// ---------------------------------------------------------------------
// Data loading
// ---------------------------------------------------------------------

async function enterApp() {
  els.authScreen.hidden = true;
  els.appShell.hidden = false;

  const { data: { user } } = await supabase.auth.getUser();
  const { data: memberships, error } = await supabase
    .from('workspace_members')
    .select('role, workspaces(*)')
    .eq('user_id', user.id)
    .limit(1);

  if (error || !memberships?.length) {
    els.workspaceName.textContent = 'No workspace found';
    return;
  }

  workspace = memberships[0].workspaces;
  els.workspaceName.textContent = workspace.name;
  fillSettingsForm();

  await loadProjects();
  renderDashboard();
  renderProjectGrid();
  await populateAiSelect();
  show(location.hash.slice(1) || 'dashboard');
}

async function loadProjects() {
  const { data, error } = await supabase
    .from('projects')
    .select('*')
    .eq('workspace_id', workspace.id)
    .order('created_at', { ascending: false });
  projects = error ? [] : data;
}

function projectMeta(p) {
  const parts = [];
  if (p.bedrooms) parts.push(`${p.bedrooms} bed`);
  if (p.bathrooms) parts.push(`${p.bathrooms} bath`);
  if (p.area_sqm) parts.push(`${p.area_sqm} m²`);
  if (p.has_pool) parts.push('pool');
  return parts.join(' • ') || p.description || p.capture_type;
}

function tourUrl(projectId) {
  return `../tour.html?project=${projectId}`;
}

function projectRowHTML(p) {
  const name = escapeHTML(p.name);
  const meta = escapeHTML(projectMeta(p));
  return `<div class="project"><div class="thumb">TWIN</div><div><b>${name}</b><p>${meta}</p></div><span class="status">${p.status}</span></div>`;
}

function projectCardHTML(p) {
  const name = escapeHTML(p.name);
  const meta = escapeHTML(projectMeta(p));
  const publishLabel = p.status === 'LIVE' ? 'Unpublish' : 'Publish';
  return `<div class="project-card">
    <div class="bigthumb">DIGITAL TWIN</div>
    <div class="body">
      <b>${name}</b><p>${meta}</p><span class="status">${p.status}</span>
      <div class="card-actions">
        <button class="textbtn" data-action="toggle-publish" data-id="${p.id}">${publishLabel}</button>
        ${p.status === 'LIVE' ? `<a class="textbtn" href="${tourUrl(p.id)}" target="_blank" rel="noopener">View tour →</a>` : ''}
      </div>
    </div>
  </div>`;
}

function renderDashboard() {
  els.projectList.innerHTML = projects.length
    ? projects.slice(0, 4).map(projectRowHTML).join('')
    : '<p style="color:#888;padding:14px 0">No projects yet — create your first digital twin.</p>';

  const live = projects.filter((p) => p.status === 'LIVE');
  const demo = live[0];
  els.btnOpenDemo.href = demo ? tourUrl(demo.id) : '#';

  const statCards = els.dashboardStats.children;
  statCards[0].querySelector('strong').textContent = live.length;
  statCards[0].querySelector('span').textContent = `${projects.length} total`;

  loadWorkspaceMetrics().then((m) => {
    statCards[1].querySelector('strong').textContent = m.tour_views;
    statCards[2].querySelector('strong').textContent = m.leads;
    statCards[3].querySelector('strong').textContent = m.ai_questions;
  });

  loadAiActivity();
}

function renderProjectGrid() {
  els.allProjects.innerHTML = projects.length
    ? projects.map(projectCardHTML).join('')
    : '<p style="color:#888">No projects yet — create your first digital twin.</p>';
}

els.allProjects.addEventListener('click', async (e) => {
  const btn = e.target.closest('[data-action="toggle-publish"]');
  if (!btn) return;
  const project = projects.find((p) => p.id === btn.dataset.id);
  const nextStatus = project.status === 'LIVE' ? 'DRAFT' : 'LIVE';
  btn.disabled = true;
  const { error } = await supabase.from('projects').update({ status: nextStatus }).eq('id', project.id);
  if (!error) project.status = nextStatus;
  renderProjectGrid();
  renderDashboard();
  populateAiSelect();
});

async function loadAiActivity() {
  const { data } = await supabase
    .from('chat_messages')
    .select('content, created_at, projects(name)')
    .eq('role', 'user')
    .order('created_at', { ascending: false })
    .limit(5);

  if (!data?.length) return;
  els.aiLog.innerHTML = data
    .map(
      (m) =>
        `<div><b>${escapeHTML(m.projects?.name || 'Property')}</b><span>“${escapeHTML(m.content).slice(0, 70)}” · ${timeAgo(m.created_at)}</span></div>`
    )
    .join('');
}

async function loadWorkspaceMetrics() {
  const { data, error } = await supabase.rpc('workspace_metric_counts', { p_workspace_id: workspace.id, p_days: 30 });
  return error || !data?.length
    ? { unique_visitors: 0, tour_views: 0, whatsapp_clicks: 0, brochure_downloads: 0, ai_questions: 0, leads: 0 }
    : data[0];
}

// ---------------------------------------------------------------------
// New project
// ---------------------------------------------------------------------

function newProjectModal() {
  openModal(`<p class="eyebrow">NEW PROJECT</p><h2>Create a digital twin</h2>
    <div class="settings">
      <label>Property name<input id="npName" placeholder="e.g. Villa 27 — Cantonments" required></label>
      <label>Capture type<select id="npCapture"><option>360° panoramas</option><option>iPhone / LiDAR</option><option>Photo / photogrammetry</option><option>Existing digital twin</option></select></label>
      <label>Bedrooms<input id="npBedrooms" type="number" min="0"></label>
      <label>Bathrooms<input id="npBathrooms" type="number" min="0"></label>
      <label>Area (m²)<input id="npArea" type="number" min="0"></label>
      <label>Capture files (photos/panoramas)<input id="npFiles" type="file" multiple accept="image/*"></label>
      <div id="npError" class="auth-error" hidden></div>
      <button class="primary" id="npSubmit">Create project</button>
    </div>`);
  document.getElementById('npSubmit').addEventListener('click', createProject);
}

async function createProject() {
  const name = document.getElementById('npName').value.trim() || 'Untitled Property';
  const capture_type = document.getElementById('npCapture').value;
  const bedrooms = Number(document.getElementById('npBedrooms').value) || null;
  const bathrooms = Number(document.getElementById('npBathrooms').value) || null;
  const area_sqm = Number(document.getElementById('npArea').value) || null;
  const files = document.getElementById('npFiles').files;
  const submitBtn = document.getElementById('npSubmit');
  const errBox = document.getElementById('npError');
  submitBtn.disabled = true;

  const { data: project, error } = await supabase
    .from('projects')
    .insert({ workspace_id: workspace.id, name, capture_type, bedrooms, bathrooms, area_sqm })
    .select()
    .single();

  if (error) {
    errBox.textContent = error.message;
    errBox.hidden = false;
    submitBtn.disabled = false;
    return;
  }

  for (const file of files) {
    const path = `${project.id}/${Date.now()}-${file.name}`;
    const { error: upErr } = await supabase.storage.from('captures').upload(path, file);
    if (!upErr) {
      await supabase.from('project_media').insert({ project_id: project.id, storage_path: path, media_type: 'photo' });
    }
  }

  await loadProjects();
  renderDashboard();
  renderProjectGrid();
  populateAiSelect();
  closeModal();
  show('projects');
}

document.getElementById('btnNewProjectSide').addEventListener('click', newProjectModal);
document.getElementById('btnNewProjectTop').addEventListener('click', newProjectModal);
document.getElementById('btnNewProjectProjects').addEventListener('click', newProjectModal);

// ---------------------------------------------------------------------
// SPATIA AI
// ---------------------------------------------------------------------

async function populateAiSelect() {
  const live = projects.filter((p) => p.status === 'LIVE');
  els.aiProjectSelect.innerHTML = live.length
    ? live.map((p) => `<option value="${p.id}">${escapeHTML(p.name)}</option>`).join('')
    : '<option value="">No published twins yet</option>';
  await renderRoomChips();
}

els.aiProjectSelect.addEventListener('change', renderRoomChips);

async function renderRoomChips() {
  const projectId = els.aiProjectSelect.value;
  if (!projectId) {
    els.roomChips.innerHTML = '<div class="hint">Publish a twin to inspect its rooms</div>';
    return;
  }
  const { data: rooms } = await supabase.from('rooms').select('name').eq('project_id', projectId).order('sort_order');
  els.roomChips.innerHTML =
    (rooms ?? []).map((r) => `<div class="room" data-room="${escapeHTML(r.name)}">${escapeHTML(r.name.toUpperCase())}</div>`).join('') +
    '<div class="hint">Click any room to ask about it</div>';
}

els.roomChips.addEventListener('click', (e) => {
  const chip = e.target.closest('[data-room]');
  if (chip) ask(`Tell me about the ${chip.dataset.room}`);
});

function addMsg(t, c) {
  const d = document.createElement('div');
  d.className = c;
  d.textContent = t;
  els.messages.appendChild(d);
  els.messages.scrollTop = 999999;
}

async function ask(text) {
  const projectId = els.aiProjectSelect.value;
  const q = text || els.q.value.trim();
  if (!q) return;
  if (!projectId) {
    addMsg('Publish a digital twin first, then I can answer questions about it.', 'bot');
    return;
  }
  addMsg(q, 'user');
  els.q.value = '';

  const { data, error } = await supabase.functions.invoke('ask-ai', {
    body: { projectId, sessionId: getSessionId(), message: q },
  });

  if (error || data?.error) {
    addMsg(data?.error || "Sorry, I couldn't reach SPATIA AI just now.", 'bot');
    return;
  }
  addMsg(data.reply, 'bot');
}

document.getElementById('btnAsk').addEventListener('click', () => ask());
els.q.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') ask();
});
document.querySelectorAll('.quick button').forEach((b) => b.addEventListener('click', () => ask(b.dataset.q)));

// ---------------------------------------------------------------------
// Leads
// ---------------------------------------------------------------------

async function loadLeads() {
  const { data, error } = await supabase
    .from('leads')
    .select('name, contact, message, created_at, projects(name)')
    .order('created_at', { ascending: false })
    .limit(100);

  if (error || !data?.length) {
    els.leadsTable.innerHTML = '<tr><td colspan="5">No leads yet — they will appear here once buyers enquire from a published tour.</td></tr>';
    return;
  }
  els.leadsTable.innerHTML = data
    .map(
      (l) =>
        `<tr><td>${escapeHTML(l.projects?.name)}</td><td>${escapeHTML(l.name || '—')}</td><td>${escapeHTML(l.contact || '—')}</td><td>${escapeHTML(l.message || '—')}</td><td>${timeAgo(l.created_at)}</td></tr>`
    )
    .join('');
}

// ---------------------------------------------------------------------
// Analytics
// ---------------------------------------------------------------------

async function loadAnalytics() {
  const m = await loadWorkspaceMetrics();
  const cards = els.analyticsStats.children;
  cards[0].querySelector('strong').textContent = m.unique_visitors;
  cards[1].querySelector('strong').textContent = m.whatsapp_clicks;
  cards[2].querySelector('strong').textContent = m.brochure_downloads;
  cards[3].querySelector('strong').textContent = m.leads;

  const { data: days, error } = await supabase.rpc('daily_views', { p_workspace_id: workspace.id, p_days: 30 });
  if (error || !days?.length) {
    els.bars.innerHTML = '';
    return;
  }
  const max = Math.max(1, ...days.map((d) => Number(d.views)));
  els.bars.innerHTML = days
    .map((d) => `<i style="height:${Math.max(4, Math.round((Number(d.views) / max) * 100))}%" title="${d.day}: ${d.views} views"></i>`)
    .join('');
}

// ---------------------------------------------------------------------
// Settings
// ---------------------------------------------------------------------

function fillSettingsForm() {
  els.settingsName.value = workspace.name || '';
  els.settingsDomain.value = workspace.domain || '';
  els.settingsWhatsapp.value = workspace.whatsapp_number || '';
  els.settingsBrochure.value = workspace.brochure_url || '';
  els.settingsAccent.value = workspace.brand_accent || '#111111';
}

els.settingsForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const update = {
    name: els.settingsName.value.trim(),
    domain: els.settingsDomain.value.trim() || null,
    whatsapp_number: els.settingsWhatsapp.value.trim() || null,
    brochure_url: els.settingsBrochure.value.trim() || null,
    brand_accent: els.settingsAccent.value.trim() || '#111111',
  };
  const { error } = await supabase.from('workspaces').update(update).eq('id', workspace.id);
  if (!error) {
    workspace = { ...workspace, ...update };
    els.workspaceName.textContent = workspace.name;
    els.settingsSaved.hidden = false;
    setTimeout(() => (els.settingsSaved.hidden = true), 2000);
  }
});

// ---------------------------------------------------------------------
// Nav + modal wiring
// ---------------------------------------------------------------------

document.querySelectorAll('nav a').forEach((a) =>
  a.addEventListener('click', (e) => {
    e.preventDefault();
    show(a.getAttribute('href').slice(1));
  })
);
document.querySelectorAll('[data-nav]').forEach((el) => el.addEventListener('click', () => show(el.dataset.nav)));
document.getElementById('modalClose').addEventListener('click', closeModal);
els.modal.addEventListener('click', (e) => {
  if (e.target === els.modal) closeModal();
});
window.addEventListener('hashchange', () => {
  const id = location.hash.slice(1) || 'dashboard';
  if (document.getElementById(id) && !els.appShell.hidden) show(id);
});

// ---------------------------------------------------------------------
// Boot
// ---------------------------------------------------------------------

async function boot() {
  if (!isConfigured) {
    els.configBanner.hidden = false;
    els.authScreen.hidden = false;
    els.authForm.querySelectorAll('input, button').forEach((el) => (el.disabled = true));
    return;
  }
  try {
    supabase = await loadSupabase();
  } catch (e) {
    console.error(e);
    els.configBanner.hidden = false;
    els.configBanner.textContent = "Couldn't load the backend library — check your connection and reload the page.";
    return;
  }
  initAuth();
}

boot();
