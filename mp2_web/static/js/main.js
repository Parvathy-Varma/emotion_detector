// static/js/main.js
const API_BASE = '/api';
const DEFAULT_USER_ID = 1;

function $(id){ return document.getElementById(id); }

let currentDetection = null;

async function logDetectionLocal(mood, confidence=0.9){
  // POST detection to server
  const resp = await fetch(`${API_BASE}/log_detection`, {
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({user_id: DEFAULT_USER_ID, emotion:mood, confidence})
  });
  const j = await resp.json();
  return j.detection_id;
}

async function fetchUserStats(){
  const resp = await fetch(`${API_BASE}/user_stats?user_id=${DEFAULT_USER_ID}&limit=14`);
  return await resp.json();
}

function showStatsModal(stats, detectionMeta){
  $('statsModal').classList.remove('hidden');
  const ctx = $('statsChart').getContext('2d');
  const counts = stats.counts || {};
  const labels = Object.keys(counts);
  const data = labels.map(l => counts[l] || 0);
  if(window._chart) window._chart.destroy();
  window._chart = new Chart(ctx, {
    type:'bar',
    data:{labels, datasets:[{label:'count', data}]}
  });
  const recent = stats.last_detections || [];
  const recentList = $('recentList'); recentList.innerHTML = '';
  recent.forEach(r => {
    const d = document.createElement('div');
    d.textContent = `${r.detected_at} — ${r.emotion}`;
    recentList.appendChild(d);
  });

  $('continueBtn').onclick = () => {
    $('statsModal').classList.add('hidden');
    $('choiceArea').classList.remove('hidden');
  };
}

async function handleDetected(mood, confidence=0.85){
  $('status').textContent = `Detected: ${mood} (${(confidence*100).toFixed(0)}%)`;
  const detId = await logDetectionLocal(mood, confidence);
  currentDetection = {detection_id: detId, mood};
  $('moodLabel').textContent = mood;
  const stats = await fetchUserStats();
  showStatsModal(stats, currentDetection);
}

// For convenience: server-side detect endpoint (optional)
$('useServerDetect').addEventListener('click', async () => {
  $('status').textContent = 'Calling server detect...';
  try{
    const r = await fetch('/detect'); // optional endpoint if implemented server-side
    const j = await r.json();
    if(j.emotion){
      await handleDetected(j.emotion, j.confidence || 0.85);
    } else {
      $('status').textContent = 'No face detected from server';
    }
  }catch(e){
    $('status').textContent = 'Server detect error (server must implement /detect)';
  }
});

// Hook to your local python detection script:
// If you run a local python script that detects and then sends POST to /api/log_detection,
// the page will show the stats automatically once you call handleDetected from that script
// But we also provide a "Start Local Detection Script" hint
$('startClientDetect').addEventListener('click', () => {
  alert("Start your local detection script (it should POST /api/log_detection) OR run detection and then call handleDetected from browser console for testing.");
});

// After Continue: show recos
$('gamesBtn').addEventListener('click', ()=> fetchAndShow('games'));
$('videosBtn').addEventListener('click', ()=> fetchAndShow('videos'));

async function fetchAndShow(kind){
  if(!currentDetection) { alert('No detection yet'); return; }
  const mood = currentDetection.mood;
  const resp = await fetch(`${API_BASE}/get_recommendations?user_id=${DEFAULT_USER_ID}&emotion=${mood}`);
  const j = await resp.json();
  renderRecommendations(j.videos, j.games);
  $('recommendations').classList.remove('hidden');
  if(kind === 'videos') window.scrollTo(0, $('videoCards').offsetTop);
  else window.scrollTo(0, $('gameCards').offsetTop);
}

function renderRecommendations(videos, games){
  const vcont = $('videoCards'); vcont.innerHTML = '<h3>Videos</h3>';
  videos.forEach(v=>{
    const card = document.createElement('div'); card.className='card';
    card.innerHTML = `<img src="https://img.youtube.com/vi/${v.id}/hqdefault.jpg" /><h4>${v.title}</h4>
      <button class="play" data-id="${v.id}">Play</button>
      <button class="select" data-id="${v.id}" data-title="${v.title}">Select</button>`;
    vcont.appendChild(card);
  });
  vcont.querySelectorAll('.play').forEach(b => b.onclick = e => playVideo(e.target.dataset.id));
  vcont.querySelectorAll('.select').forEach(b => b.onclick = e => pickItem('video', e.target.dataset.id, e.target.dataset.title));

  const gcont = $('gameCards'); gcont.innerHTML = '<h3>Games</h3>';
  games.forEach(g=>{
    const card = document.createElement('div'); card.className='card';
    card.innerHTML = `<h4>${g.title}</h4>
      <button class="playGame" data-file="${g.file}">Play</button>
      <button class="selectGame" data-id="${g.id}" data-file="${g.file}" data-title="${g.title}">Select</button>`;
    gcont.appendChild(card);
  });
  gcont.querySelectorAll('.playGame').forEach(b => b.onclick = e => window.open(`/games/${e.target.dataset.file}`, '_blank'));
  gcont.querySelectorAll('.selectGame').forEach(b => b.onclick = e => pickItem('game', e.target.dataset.id, e.target.dataset.title, e.target.dataset.file));
}

function playVideo(id){
  $('playerArea').innerHTML = `<iframe width="640" height="360" src="https://www.youtube.com/embed/${id}?autoplay=1" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>`;
  $('playerModal').classList.remove('hidden');
}
$('closePlayer').addEventListener('click', ()=> { $('playerModal').classList.add('hidden'); $('playerArea').innerHTML=''; });

async function pickItem(kind, item_id, title, file=null){
  if(!currentDetection) return alert('No detection id');
  await fetch(`${API_BASE}/log_pick`, {
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({
      user_id: DEFAULT_USER_ID,
      detection_id: currentDetection.detection_id,
      kind: kind,
      item_id: item_id,
      title: title,
      mood: currentDetection.mood
    })
  });
  if(kind === 'video') playVideo(item_id);
  else window.open(`/games/${file}`, '_blank');
}
