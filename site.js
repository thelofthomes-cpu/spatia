function toggleNav(){document.getElementById('siteNav').classList.toggle('open')}
document.querySelectorAll('#siteNav a').forEach(a=>a.addEventListener('click',()=>document.getElementById('siteNav').classList.remove('open')));
