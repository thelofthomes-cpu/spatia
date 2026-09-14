// Real-time 3D walkthrough for the marketing hero — a live-rendered
// house interior (living room → kitchen → bedroom) with a camera that
// glides forward and back through the doorways in a seamless loop.
// Not a video: this is an actual WebGL scene, rendered in the browser.

const canvas = document.getElementById('heroCanvas');
if (canvas && window.WebGLRenderingContext) {
  init().catch((e) => console.error('3D hero failed to load', e));
}

async function init() {
  const THREE = await import('https://unpkg.com/three@0.160.0/build/three.module.js');

  const container = canvas.parentElement;
  const BG = 0xe8e4db;
  const WALL = 0xf1eee5;
  const FLOOR = 0x8a6f52;
  const INK = 0x2a2723;
  const ACCENT = 0xc9bba0;

  const scene = new THREE.Scene();
  scene.background = new THREE.Color(BG);
  scene.fog = new THREE.Fog(BG, 9, 24);

  const camera = new THREE.PerspectiveCamera(58, 1, 0.1, 50);

  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

  function resize() {
    const w = container.clientWidth;
    const h = container.clientHeight || 420;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  }
  resize();
  window.addEventListener('resize', resize);

  // ---- lighting ----
  scene.add(new THREE.HemisphereLight(0xffffff, BG, 1.0));
  const sun = new THREE.DirectionalLight(0xfff3e0, 0.7);
  sun.position.set(6, 10, 4);
  scene.add(sun);

  // ---- geometry helpers ----
  const floorMat = new THREE.MeshStandardMaterial({ color: FLOOR, roughness: 0.85 });
  const wallMat = new THREE.MeshStandardMaterial({ color: WALL, roughness: 0.95 });
  const inkMat = new THREE.MeshStandardMaterial({ color: INK, roughness: 0.7 });
  const accentMat = new THREE.MeshStandardMaterial({ color: ACCENT, roughness: 0.8 });

  function box(w, h, d, mat, x, y, z) {
    const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat);
    m.position.set(x, y, z);
    scene.add(m);
    return m;
  }

  const DEPTH = 8; // room depth along z, centered on 0 (-4..4)
  const WALL_H = 3.2;
  const DOOR_HALF = 1.2;

  // continuous floor spanning all three rooms
  box(26, 0.2, DEPTH, floorMat, 0, -0.1, 0);

  // back / front perimeter walls
  box(26, WALL_H, 0.2, wallMat, 0, WALL_H / 2, -DEPTH / 2);
  box(26, WALL_H, 0.2, wallMat, 0, WALL_H / 2, DEPTH / 2);

  // dividing walls with doorway gaps, at x = -4 and x = 4
  [-4, 4].forEach((x) => {
    const segLen = DEPTH / 2 - DOOR_HALF;
    box(0.2, WALL_H, segLen, wallMat, x, WALL_H / 2, -(DEPTH / 4 + DOOR_HALF / 2));
    box(0.2, WALL_H, segLen, wallMat, x, WALL_H / 2, DEPTH / 4 + DOOR_HALF / 2);
  });

  // --- Room 1: living room (x around -8) ---
  box(2.6, 0.7, 1.1, accentMat, -9.5, 0.35, 1.4); // sofa
  box(0.9, 0.4, 0.9, inkMat, -9.5, 0.2, -0.6); // coffee table

  // --- Room 2: kitchen (x around 0) ---
  box(3.4, 0.9, 0.7, inkMat, 0, 0.45, -3.2); // counter along back wall
  box(0.5, 0.9, 0.5, accentMat, 1.8, 0.45, -1.6); // stool

  // --- Room 3: bedroom (x around 8) ---
  box(2.2, 0.5, 2.8, accentMat, 8.5, 0.25, 0.6); // bed
  box(0.6, 0.5, 0.6, inkMat, 7.1, 0.25, 1.6); // nightstand

  // ---- camera path: smooth forward/back glide through all three rooms ----
  const clock = new THREE.Clock();
  const CYCLE = 26; // seconds for a full forward+back loop
  let raf;

  function animate() {
    raf = requestAnimationFrame(animate);
    const t = clock.getElapsedTime();
    const omega = (Math.PI * 2) / CYCLE;
    const x = 9.5 * Math.cos(t * omega);
    const dir = Math.sign(-Math.sin(t * omega)) || 1;
    const sway = Math.sin(t * 0.9) * 0.35;
    const bob = Math.sin(t * 1.8) * 0.04;

    camera.position.set(x, 1.55 + bob, sway);
    camera.lookAt(x + dir * 3, 1.4, sway * 0.6);

    renderer.render(scene, camera);
  }

  document.addEventListener('visibilitychange', () => {
    if (document.hidden) cancelAnimationFrame(raf);
    else animate();
  });

  animate();
}
