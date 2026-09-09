const projects=[['Villa A — Cantonments','4 bed • 5 bath • 420 m²','LIVE'],['Apartment 08 — Airport','3 bed • 3 bath • 210 m²','PROCESSING'],['House 14 — Labone','5 bed • 6 bath • 510 m²','LIVE'],['Office HQ — Ridge','1,240 m² • 3 floors','LIVE'],['Beach Villa — Labadi','6 bed • pool • 680 m²','DRAFT']];

function escapeHTML(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}

function projectHTML(p,card=false){const[name,desc,status]=p.map(escapeHTML);return card?`<div class="project-card"><div class="bigthumb">DIGITAL TWIN</div><div class="body"><b>${name}</b><p>${desc}</p><span class="status">${status}</span></div></div>`:`<div class="project"><div class="thumb">TWIN</div><div><b>${name}</b><p>${desc}</p></div><span class="status">${status}</span></div>`}

function render(){document.getElementById('projectList').innerHTML=projects.slice(0,4).map(p=>projectHTML(p)).join('');document.getElementById('allProjects').innerHTML=projects.map(p=>projectHTML(p,true)).join('')}

function renderBars(){document.getElementById('bars').innerHTML=Array.from({length:30},()=>`<i style="height:${20+Math.round(Math.random()*80)}%"></i>`).join('')}

function show(id){document.querySelectorAll('.view').forEach(x=>x.classList.remove('active-view'));document.getElementById(id).classList.add('active-view');document.querySelectorAll('nav a').forEach(a=>a.classList.toggle('active',a.getAttribute('href')==='#'+id));location.hash=id;if(id==='analytics')renderBars()}

function newProject(){openModal(`<p class="eyebrow">NEW PROJECT</p><h2>Create a digital twin</h2><p style="color:#777">The production MVP will accept 360° panoramas, photos, video and LiDAR capture. This prototype demonstrates the workflow.</p><div class="settings"><label>Property name<input id="newName" placeholder="e.g. Villa 27 — Cantonments"></label><label>Capture type<select id="capture" style="padding:12px;border:1px solid #e9e7e2;border-radius:8px"><option>360° panoramas</option><option>iPhone / LiDAR</option><option>Photo / photogrammetry</option><option>Existing digital twin</option></select></label><button class="primary" onclick="createProject()">Create project</button></div>`)}

function createProject(){let n=document.getElementById('newName').value.trim()||'Untitled Property';projects.unshift([n,'New capture • AI processing','DRAFT']);render();closeModal();show('projects')}

function openTour(){openModal(`<p class="eyebrow">LIVE DIGITAL TWIN</p><h2>Villa A — Cantonments</h2><div class="tour"><div class="scene">LIVING ROOM</div><div class="tourbar"><span>← Living</span><b>Living Room</b><span>Kitchen →</span></div></div><div style="display:flex;gap:8px;margin-top:14px"><button class="primary" onclick="closeModal();show('ai')">Ask SPATIA AI</button><button class="ghost">Share tour</button><button class="ghost">Book viewing</button></div>`)}

function ask(text){const input=document.getElementById('q');const q=text||input.value.trim();if(!q)return;addMsg(q,'user');input.value='';setTimeout(()=>{let a='I can answer using the property’s spatial model and listing data.';if(/bedroom/i.test(q))a='The property has 4 bedrooms, including a master suite. The master bedroom is the largest sleeping area.';else if(/pool/i.test(q))a='Yes. A swimming pool is mapped to the rear outdoor area, adjacent to the garden.';else if(/largest|biggest/i.test(q))a='The living room is the largest primary interior space, while the master suite is the largest bedroom.';else if(/parking/i.test(q))a='The listing data indicates 4 parking spaces.';addMsg(a,'bot')},450)}

function addMsg(t,c){const d=document.createElement('div');d.className=c;d.textContent=t;document.getElementById('messages').appendChild(d);document.getElementById('messages').scrollTop=99999}

function inspectRoom(name){show('ai');setTimeout(()=>ask(`Tell me about the ${name}`),50)}

function openModal(html){document.getElementById('modalContent').innerHTML=html;document.getElementById('modal').style.display='grid'}
function closeModal(){document.getElementById('modal').style.display='none'}

document.getElementById('modal').addEventListener('click',e=>{if(e.target.id==='modal')closeModal()});
window.addEventListener('hashchange',()=>{const id=location.hash.slice(1)||'dashboard';if(document.getElementById(id))show(id)});

render();
show(location.hash.slice(1)||'dashboard');
