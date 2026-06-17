// 3D "blueprint forge": 10 translucent panels (one per plan section) orbit and
// assemble into a rotating tower over a drafting grid. On generation, they snap
// into place — a visual metaphor for an idea becoming a structured plan.
(function () {
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const mount = document.getElementById("forge3d");
  if (!mount || typeof THREE === "undefined") return;

  const W = () => mount.clientWidth;
  const H = () => mount.clientHeight;

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(42, W() / H(), 0.1, 100);
  camera.position.set(4.4, 3.0, 6.2);
  camera.lookAt(0, 0.6, 0);

  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setSize(W(), H());
  mount.appendChild(renderer.domElement);

  // lights
  scene.add(new THREE.AmbientLight(0x88aaff, 0.5));
  const key = new THREE.DirectionalLight(0xffffff, 1.4);
  key.position.set(5, 8, 6);
  scene.add(key);
  const gold = new THREE.PointLight(0xe8b04b, 1.6, 30);
  gold.position.set(-4, 2, 3);
  scene.add(gold);

  // drafting grid floor
  const grid = new THREE.GridHelper(14, 28, 0x5fa8d3, 0x27375e);
  grid.position.y = -1.6;
  grid.material.opacity = 0.35;
  grid.material.transparent = true;
  scene.add(grid);

  // 10 panels = 10 plan sections
  const group = new THREE.Group();
  scene.add(group);
  const N = 10;
  const panels = [];
  const goldMat = new THREE.MeshStandardMaterial({
    color: 0xe8b04b, metalness: 0.6, roughness: 0.25,
    transparent: true, opacity: 0.92,
  });
  const blueMat = new THREE.MeshStandardMaterial({
    color: 0x16223f, metalness: 0.3, roughness: 0.4,
    transparent: true, opacity: 0.78,
  });

  for (let i = 0; i < N; i++) {
    const geo = new THREE.BoxGeometry(2.2, 0.16, 2.2);
    const mat = (i % 3 === 0 ? goldMat : blueMat).clone();
    const m = new THREE.Mesh(geo, mat);
    const targetY = i * 0.34 - 1.4;

    // wireframe edges
    const edges = new THREE.LineSegments(
      new THREE.EdgesGeometry(geo),
      new THREE.LineBasicMaterial({ color: 0x5fa8d3, transparent: true, opacity: 0.5 })
    );
    m.add(edges);

    m.userData = {
      targetY,
      spin: 0.15 + Math.random() * 0.25,
      orbit: Math.random() * Math.PI * 2,
      radius: 3.2 + Math.random() * 1.6,
    };
    // start scattered
    m.position.set(
      Math.cos(m.userData.orbit) * m.userData.radius,
      targetY + (Math.random() - 0.5) * 4,
      Math.sin(m.userData.orbit) * m.userData.radius
    );
    m.rotation.y = Math.random() * Math.PI;
    group.add(m);
    panels.push(m);
  }

  let assembled = 0; // 0..1
  let assembling = false;
  let t = 0;

  window.forgeAssemble = function () {
    assembling = true;
  };

  function tick() {
    t += 0.016;
    if (assembling && assembled < 1) assembled = Math.min(1, assembled + 0.012);

    panels.forEach((m, i) => {
      const u = m.userData;
      const ease = assembled * assembled * (3 - 2 * assembled);
      // orbit position when loose
      const ox = Math.cos(u.orbit + t * u.spin) * u.radius;
      const oz = Math.sin(u.orbit + t * u.spin) * u.radius;
      const oy = u.targetY + Math.sin(t * 0.8 + i) * 1.6;
      // lerp toward assembled tower
      m.position.x = ox * (1 - ease);
      m.position.z = oz * (1 - ease);
      m.position.y = oy * (1 - ease) + u.targetY * ease;
      m.rotation.y += 0.004 + (1 - ease) * 0.02;
    });

    group.rotation.y += reduce ? 0 : 0.0035;
    renderer.render(scene, camera);
    if (!reduce) requestAnimationFrame(tick);
    else renderer.render(scene, camera);
  }
  tick();

  window.addEventListener("resize", () => {
    camera.aspect = W() / H();
    camera.updateProjectionMatrix();
    renderer.setSize(W(), H());
  });
})();
