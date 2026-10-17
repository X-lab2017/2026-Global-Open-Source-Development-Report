import * as THREE from "./assets/cmap/vendor/three.module.js";
import { OrbitControls } from "./assets/cmap/vendor/OrbitControls.js";

// The third coordinate aids navigation only. No metric is encoded by depth.
export function mount(
  host,
  { nodes, edges, positions, orbit, selected, colors, onSelect },
) {
  let disposed = false,
    frame = 0;
  const pos = new Map(positions),
    scene = new THREE.Scene();
  scene.background = new THREE.Color(colors.bg);
  const camera = new THREE.PerspectiveCamera(45, 1, 1, 5000);
  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.domElement.setAttribute(
    "aria-label",
    "模型复用关系三维网络。拖动旋转，滚轮缩放，点击模型；也可使用旁边搜索和模型列表。",
  );
  host.append(renderer.domElement);
  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = false;
  controls.minDistance = 300;
  controls.maxDistance = 2600;
  const objects = [],
    by = new Map(),
    resources = [];
  const hash = (s) =>
    [...s].reduce((n, c) => (n * 31 + c.charCodeAt(0)) | 0, 0);
  nodes.forEach((n) => {
    const p = pos.get(n.id);
    by.set(
      n.id,
      new THREE.Vector3(
        p.x - 600,
        410 - p.y,
        ((Math.abs(hash(n.id)) % 151) - 75) * 1.45,
      ),
    );
  });
  const coords = [],
    pointColors = [];
  nodes.forEach((n) => {
    const p = pos.get(n.id),
      v = by.get(n.id),
      c = new THREE.Color(
        n.id === selected
          ? colors.gold
          : colors.palette[(p.cluster || 0) % colors.palette.length],
      );
    coords.push(v.x, v.y, v.z);
    pointColors.push(c.r, c.g, c.b);
  });
  const geo = new THREE.BufferGeometry();
  geo.setAttribute("position", new THREE.Float32BufferAttribute(coords, 3));
  geo.setAttribute("color", new THREE.Float32BufferAttribute(pointColors, 3));
  const material = new THREE.PointsMaterial({
    size: nodes.length > 1000 ? 4.5 : 6.5,
    vertexColors: true,
    sizeAttenuation: true,
  });
  const points = new THREE.Points(geo, material);
  scene.add(points);
  resources.push(geo, material);
  const segments = [],
    highlight = [];
  edges.forEach((e) => {
    const a = by.get(e.source),
      b = by.get(e.target);
    (e.source === selected || e.target === selected
      ? highlight
      : segments
    ).push(a.x, a.y, a.z, b.x, b.y, b.z);
  });
  for (const [arr, color, opacity] of [
    [segments, colors.line, 0.45],
    [highlight, colors.brand, 0.95],
  ]) {
    const g = new THREE.BufferGeometry();
    g.setAttribute("position", new THREE.Float32BufferAttribute(arr, 3));
    const m = new THREE.LineBasicMaterial({
      color,
      transparent: true,
      opacity,
    });
    scene.add(new THREE.LineSegments(g, m));
    resources.push(g, m);
  }
  // Hubs retain the same direct-downstream size meaning as the 2D view.
  nodes
    .filter((n) => n.downstreamCount >= 10 || n.id === selected)
    .forEach((n) => {
      const g = new THREE.SphereGeometry(
          n.id === selected
            ? 10
            : Math.min(10, 3 + Math.sqrt(n.downstreamCount) * 0.5),
          10,
          8,
        ),
        m = new THREE.MeshBasicMaterial({
          color:
            n.id === selected
              ? colors.gold
              : colors.palette[
                  (pos.get(n.id).cluster || 0) % colors.palette.length
                ],
        });
      const sphere = new THREE.Mesh(g, m);
      sphere.position.copy(by.get(n.id));
      sphere.userData.id = n.id;
      scene.add(sphere);
      objects.push(sphere);
      resources.push(g, m);
    });
  const tip = document.createElement("div");
  tip.className = "gm-three-tooltip";
  tip.hidden = true;
  host.append(tip);
  const render = () => {
    if (disposed) return;
    frame = 0;
    renderer.render(scene, camera);
  };
  const schedule = () => {
    if (!disposed && !frame) frame = requestAnimationFrame(render);
  };
  controls.addEventListener("change", schedule);
  const resize = () => {
    const w = host.clientWidth || 800,
      h = host.clientHeight || 560;
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    renderer.setSize(w, h);
    schedule();
  };
  const reset = () => {
    camera.position.set(
      0,
      0,
      Math.max(
        1150,
        1100 / (host.clientWidth / Math.max(1, host.clientHeight)),
      ),
    );
    controls.target.set(0, 0, 0);
    controls.update();
    schedule();
  };
  const ro = new ResizeObserver(resize);
  ro.observe(host);
  resize();
  reset();
  if (orbit) {
    camera.position.fromArray(orbit.position);
    controls.target.fromArray(orbit.target);
    controls.update();
    schedule();
  }
  const ray = new THREE.Raycaster(),
    pointer = new THREE.Vector2();
  ray.params.Points.threshold = 8;
  function hit(e) {
    const r = renderer.domElement.getBoundingClientRect();
    pointer.set(
      ((e.clientX - r.left) / r.width) * 2 - 1,
      (-(e.clientY - r.top) / r.height) * 2 + 1,
    );
    ray.setFromCamera(pointer, camera);
    const sphere = ray.intersectObjects(objects)[0];
    if (sphere) return sphere.object.userData.id;
    const point = ray.intersectObject(points)[0];
    return point ? nodes[point.index].id : null;
  }
  let start = null;
  renderer.domElement.addEventListener("pointerdown", (e) => {
    start = [e.clientX, e.clientY];
    tip.hidden = true;
  });
  renderer.domElement.addEventListener("pointerup", (e) => {
    if (!start || Math.hypot(e.clientX - start[0], e.clientY - start[1]) > 5)
      return;
    const id = hit(e);
    if (id) onSelect(id);
  });
  renderer.domElement.addEventListener("pointermove", (e) => {
    if (e.buttons) return;
    const id = hit(e);
    renderer.domElement.style.cursor = id ? "pointer" : "grab";
    tip.hidden = !id;
    if (id) tip.textContent = id;
  });
  renderer.domElement.addEventListener(
    "pointerleave",
    () => (tip.hidden = true),
  );
  renderer.domElement.addEventListener("webglcontextlost", (e) => {
    e.preventDefault();
    host.closest(".gm-network-stage").classList.remove("gm-three-ready");
    host.closest(".gm-network-stage").classList.add("gm-three-failed");
    tip.hidden = false;
    tip.textContent = "3D 上下文已中断，已保留 2D 网络。";
  });
  return {
    snapshot() {
      return {
        position: camera.position.toArray(),
        target: controls.target.toArray(),
      };
    },
    zoom(factor) {
      camera.position
        .sub(controls.target)
        .multiplyScalar(factor)
        .add(controls.target);
      controls.update();
      schedule();
    },
    reset,
    dispose() {
      disposed = true;
      cancelAnimationFrame(frame);
      ro.disconnect();
      controls.dispose();
      resources.forEach((r) => r.dispose());
      renderer.dispose();
      host.replaceChildren();
    },
  };
}
