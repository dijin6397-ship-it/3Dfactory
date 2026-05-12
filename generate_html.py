"""
基于 factory_model_v2.json 生成高精度3D工厂可视化HTML文件。
输出为可直接双击打开的单文件3D查看器。
"""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE, "factory_model_v2.json")
OUTPUT = os.path.join(BASE, "3d-viewer.html")

with open(DATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

BD = data["building"]
BCX = BD["centerX"]
BCY = BD["centerY"]
BW = BD["width"]
BH = BD["height"]

data_json = json.dumps(data, ensure_ascii=False)

html = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>上海北翟路车辆段检修库 - 3D 可视化</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;overflow:hidden;background:#0d1117}
#canvas-container{width:100vw;height:100vh}
#ui-overlay{position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none}
#controls{position:absolute;top:16px;left:16px;background:rgba(13,17,23,0.92);backdrop-filter:blur(12px);border-radius:12px;padding:18px;color:#fff;pointer-events:auto;width:260px;max-height:calc(100vh - 32px);overflow:hidden;box-shadow:0 8px 32px rgba(0,0,0,0.5);border:1px solid rgba(255,255,255,0.08);transition:padding .3s,width .3s}
#controls.collapsed{width:auto;max-height:none;overflow:visible}
#controls.collapsed .ctrl-body{display:none}
#controls:not(.collapsed) .ctrl-body{overflow-y:auto;max-height:calc(100vh - 120px)}
#controls .ctrl-header{display:flex;align-items:center;justify-content:space-between;gap:8px}
#controls .ctrl-header h1{font-size:15px;color:#58a6ff;font-weight:600;line-height:1.3;margin:0;flex:1}
#controls .ctrl-toggle{background:rgba(88,166,255,0.15);border:1px solid rgba(88,166,255,0.3);color:#58a6ff;width:28px;height:28px;border-radius:6px;cursor:pointer;font-size:16px;display:flex;align-items:center;justify-content:center;transition:all .2s;flex-shrink:0}
#controls .ctrl-toggle:hover{background:rgba(88,166,255,0.3)}
#controls h2{font-size:11px;margin:10px 0 6px;color:#8b949e;font-weight:500;text-transform:uppercase;letter-spacing:0.5px}
.cg{margin-bottom:10px}
.cg .btn{background:linear-gradient(135deg,#238636,#2ea043);color:#fff;border:none;padding:5px 10px;border-radius:6px;cursor:pointer;font-size:11px;margin:0 3px 3px 0;transition:all .15s}
.cg .btn:hover{transform:translateY(-1px);box-shadow:0 4px 12px rgba(46,160,67,0.3)}
.cg label{display:flex;align-items:center;gap:7px;margin-bottom:4px;font-size:11px;color:#c9d1d9;cursor:pointer}
.cg input[type="checkbox"]{accent-color:#58a6ff;width:13px;height:13px}
.stats{margin-top:10px;padding-top:10px;border-top:1px solid rgba(255,255,255,0.08)}
.stats p{font-size:11px;color:#8b949e;margin-bottom:3px}
.stats span{color:#58a6ff;font-weight:600}
.legend{margin-top:10px;padding-top:10px;border-top:1px solid rgba(255,255,255,0.08);display:flex;flex-wrap:wrap;gap:6px}
.legend-item{display:flex;align-items:center;gap:4px;font-size:9px;color:#8b949e}
.color-box{width:10px;height:10px;border-radius:2px}
#tooltip{position:absolute;background:rgba(13,17,23,0.95);backdrop-filter:blur(8px);color:#fff;padding:10px 14px;border-radius:8px;font-size:12px;pointer-events:none;border:1px solid rgba(88,166,255,0.3);box-shadow:0 4px 16px rgba(0,0,0,0.4);max-width:280px;z-index:100}
#tooltip.hidden{display:none}
#tooltip h4{color:#58a6ff;margin-bottom:6px;font-size:13px}
#tooltip p{color:#c9d1d9;margin:2px 0;font-size:11px}
#tooltip .tag{display:inline-block;background:rgba(88,166,255,0.15);color:#58a6ff;padding:1px 6px;border-radius:4px;font-size:10px;margin-right:4px}
#minimap{position:absolute;bottom:16px;right:16px;width:200px;height:120px;background:rgba(13,17,23,0.9);border:1px solid rgba(255,255,255,0.08);border-radius:8px;pointer-events:auto;overflow:hidden}
#minimap canvas{width:100%;height:100%}
#search-box{position:absolute;top:16px;right:16px;pointer-events:auto}
#search-box input{background:rgba(13,17,23,0.9);color:#c9d1d9;border:1px solid #30363d;border-radius:8px;padding:8px 14px;font-size:13px;width:220px;outline:none;transition:border-color .2s}
#search-box input:focus{border-color:#58a6ff}
#search-results{position:absolute;top:40px;right:0;background:rgba(13,17,23,0.95);border:1px solid #30363d;border-radius:8px;max-height:300px;overflow-y:auto;width:220px;display:none}
#search-results .sr-item{padding:8px 12px;cursor:pointer;font-size:12px;color:#c9d1d9;border-bottom:1px solid #21262d}
#search-results .sr-item:hover{background:rgba(88,166,255,0.1)}
</style>
<script type="importmap">
{"imports":{"three":"https://unpkg.com/three@0.160.0/build/three.module.js","three/addons/":"https://unpkg.com/three@0.160.0/examples/jsm/"}}
</script>
</head>
<body>
<div id="canvas-container"></div>
<div id="ui-overlay">
  <div id="controls">
    <div class="ctrl-header">
      <h1>上海申通北车（北翟路）<br>检修库工艺布局图</h1>
      <button class="ctrl-toggle" id="btn-collapse" title="收缩/展开">−</button>
    </div>
    <div class="ctrl-body">
    <h2>视角控制</h2>
    <div class="cg">
      <button id="btn-reset" class="btn">默认视角</button>
      <button id="btn-top" class="btn">俯视</button>
      <button id="btn-side" class="btn">侧视</button>
      <button id="btn-front" class="btn">正视</button>
    </div>
    <h2>显示图层</h2>
    <div class="cg">
      <label><input type="checkbox" id="tog-tracks" checked> 停车线 (9条)</label>
      <label><input type="checkbox" id="tog-trains" checked> 列车 (27辆)</label>
      <label><input type="checkbox" id="tog-bogie" checked> 转向架检修</label>
      <label><input type="checkbox" id="tog-crane-g" checked> 龙门吊</label>
      <label><input type="checkbox" id="tog-crane-b" checked> 桥式起重机</label>
      <label><input type="checkbox" id="tog-vehicle" checked> 车体检修区</label>
      <label><input type="checkbox" id="tog-workshop" checked> 部件检修间</label>
      <label><input type="checkbox" id="tog-equip" checked> 设备</label>
      <label><input type="checkbox" id="tog-platforms" checked> 检修平台</label>
      <label><input type="checkbox" id="tog-lifts" checked> 架车点</label>
      <label><input type="checkbox" id="tog-wheelsets" checked> 轮对存放架</label>
      <label><input type="checkbox" id="tog-safety" checked> 安全标线</label>
      <label><input type="checkbox" id="tog-columns" checked> 立柱</label>
      <label><input type="checkbox" id="tog-labels" checked> 文字标签</label>
      <label><input type="checkbox" id="tog-walls" checked> 墙体</label>
      <label><input type="checkbox" id="tog-floor" checked> 地面</label>
    </div>
    <h2>图例</h2>
    <div class="legend">
      <div class="legend-item"><span class="color-box" style="background:#2196f3"></span>停车线</div>
      <div class="legend-item"><span class="color-box" style="background:#78909c"></span>列车</div>
      <div class="legend-item"><span class="color-box" style="background:#1565c0"></span>转向架工位</div>
      <div class="legend-item"><span class="color-box" style="background:#ffc107"></span>龙门吊</div>
      <div class="legend-item"><span class="color-box" style="background:#ff8f00"></span>桥式起重机</div>
      <div class="legend-item"><span class="color-box" style="background:#1565c0"></span>车体检修</div>
      <div class="legend-item"><span class="color-box" style="background:#78909c"></span>部件检修间</div>
      <div class="legend-item"><span class="color-box" style="background:#42a5f5"></span>设备</div>
      <div class="legend-item"><span class="color-box" style="background:#ffc107"></span>平台/架车点</div>
      <div class="legend-item"><span class="color-box" style="background:#ffc107"></span>轮对</div>
      <div class="legend-item"><span class="color-box" style="background:#00c853"></span>安全线</div>
      <div class="legend-item"><span class="color-box" style="background:#607d8b"></span>立柱</div>
    </div>
    <div class="stats">
      <p>停车线: <span>9</span> 条</p>
      <p>列车: <span>27</span> 辆</p>
      <p>转向架工位: <span>6</span> 个</p>
      <p>龙门吊: <span>2</span> 台</p>
      <p>桥式起重机: <span>2</span> 台</p>
      <p>车体检修区: <span>3</span> 个</p>
      <p>部件检修间: <span>8</span> 间</p>
      <p>立柱: <span id="stat-cols">-</span> 根</p>
    </div>
    </div>
  </div>
  <div id="search-box">
    <input type="text" id="search-input" placeholder="搜索区域/设备...">
    <div id="search-results"></div>
  </div>
  <div id="tooltip" class="hidden"></div>
  <div id="minimap"><canvas id="minimap-canvas" width="400" height="240"></canvas></div>
</div>

<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const D = ''' + data_json + r''';
const BCX = ''' + str(BCX) + r''';
const BCY = ''' + str(BCY) + r''';
const BW = ''' + str(BW) + r''';
const BH = ''' + str(BH) + r''';

let scene, camera, renderer, controls;
const allMeshGroups = {};
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();

function init() {
  const container = document.getElementById('canvas-container');
  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x0d1117);
  scene.fog = new THREE.FogExp2(0x0d1117, 0.0012);

  camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 3000);
  camera.position.set(BCX, 280, BCY + 250);

  renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.3;
  container.appendChild(renderer.domElement);

  controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.08;
  controls.minDistance = 10;
  controls.maxDistance = 1200;
  controls.maxPolarAngle = Math.PI / 2.05;
  controls.target.set(BCX, 0, BCY);

  setupLights();
  buildScene();
  setupUI();
  setupSearch();
  setupRaycaster();
  animate();
  drawMinimap();

  document.getElementById('stat-cols').textContent = D.columns.length;
}

function setupLights() {
  scene.add(new THREE.AmbientLight(0xffffff, 0.45));

  const sun = new THREE.DirectionalLight(0xfff4e0, 1.1);
  sun.position.set(BCX + 200, 400, BCY + 150);
  sun.castShadow = true;
  sun.shadow.mapSize.set(4096, 4096);
  const s = 400;
  sun.shadow.camera.near = 1;
  sun.shadow.camera.far = 1000;
  sun.shadow.camera.left = BCX - s;
  sun.shadow.camera.right = BCX + s;
  sun.shadow.camera.top = BCY + s;
  sun.shadow.camera.bottom = BCY - s;
  sun.shadow.bias = -0.0003;
  scene.add(sun);

  const fill = new THREE.DirectionalLight(0x8ecae6, 0.3);
  fill.position.set(BCX - 150, 250, BCY - 100);
  scene.add(fill);

  const hemi = new THREE.HemisphereLight(0x87ceeb, 0x2c3e50, 0.25);
  scene.add(hemi);
}

function ensureGroup(name) {
  if (!allMeshGroups[name]) allMeshGroups[name] = [];
}

function addMesh(group, mesh) {
  ensureGroup(group);
  allMeshGroups[group].push(mesh);
  scene.add(mesh);
}

function buildScene() {
  createFloor();
  createWalls();
  createColumns();
  createSafetyLines();
  createTracks();
  createTrains();
  createBogieStations();
  createGantryCranes();
  createBridgeCranes();
  createVehicleMaintenance();
  createWorkshops();
  createEquipment();
  createPlatforms();
  createLifts();
  createWheelSets();
  createLabels();
}

function createFloor() {
  const ext = 60;
  const geo = new THREE.PlaneGeometry(BW + ext * 2, BH + ext * 2);
  const mat = new THREE.MeshStandardMaterial({ color: 0x1a2332, roughness: 0.9, metalness: 0.1 });
  const mesh = new THREE.Mesh(geo, mat);
  mesh.rotation.x = -Math.PI / 2;
  mesh.position.set(BCX, -0.2, BCY);
  mesh.receiveShadow = true;
  addMesh('floor', mesh);

  const grid = new THREE.GridHelper(Math.max(BW, BH) + ext * 2, 40, 0x1e3a5f, 0x132640);
  grid.position.set(BCX, -0.15, BCY);
  addMesh('floor', grid);

  const innerGeo = new THREE.PlaneGeometry(BW, BH);
  const innerMat = new THREE.MeshStandardMaterial({ color: 0x1e2d3d, roughness: 0.85, metalness: 0.05 });
  const inner = new THREE.Mesh(innerGeo, innerMat);
  inner.rotation.x = -Math.PI / 2;
  inner.position.set(BCX, 0.01, BCY);
  inner.receiveShadow = true;
  addMesh('floor', inner);
}

function createWalls() {
  const wh = D.building.wallHeight;
  const wallMat = new THREE.MeshStandardMaterial({ color: 0x3a4f6a, roughness: 0.85, metalness: 0.15, transparent: true, opacity: 0.5 });
  const bx = BCX - BW / 2;
  const bz = BCY - BH / 2;
  const wallDefs = [
    { w: BW, d: 0.5, x: BCX, z: bz },
    { w: BW, d: 0.5, x: BCX, z: bz + BH },
    { w: 0.5, d: BH, x: bx, z: BCY },
    { w: 0.5, d: BH, x: bx + BW, z: BCY },
  ];
  wallDefs.forEach(w => {
    const geo = new THREE.BoxGeometry(w.w, wh, w.d);
    const m = new THREE.Mesh(geo, wallMat);
    m.position.set(w.x, wh / 2, w.z);
    m.castShadow = true;
    m.receiveShadow = true;
    addMesh('walls', m);
  });

  const edgeMat = new THREE.LineBasicMaterial({ color: 0x58a6ff });
  const edgeGeo = new THREE.EdgesGeometry(new THREE.BoxGeometry(BW, wh, BH));
  const edges = new THREE.LineSegments(edgeGeo, edgeMat);
  edges.position.set(BCX, wh / 2, BCY);
  addMesh('walls', edges);
}

function createColumns() {
  const wh = D.building.wallHeight;
  const colGeo = new THREE.CylinderGeometry(0.4, 0.4, wh, 8);
  const colMat = new THREE.MeshStandardMaterial({ color: 0x607d8b, roughness: 0.7, metalness: 0.3 });
  D.columns.forEach(c => {
    const m = new THREE.Mesh(colGeo, colMat);
    m.position.set(c.x, wh / 2, c.y);
    m.castShadow = true;
    addMesh('columns', m);
  });
}

function createSafetyLines() {
  (D.greenLines || []).forEach(sl => {
    const geo = new THREE.BoxGeometry(sl.w, 0.08, sl.h);
    const mat = new THREE.MeshStandardMaterial({ color: sl.color, roughness: 0.5, metalness: 0.2, emissive: sl.color, emissiveIntensity: 0.15 });
    const m = new THREE.Mesh(geo, mat);
    m.position.set(sl.x + sl.w / 2, 0.06, sl.y + sl.h / 2);
    addMesh('safety', m);
  });

  (D.greenZoneBorders || []).forEach(gz => {
    if (gz.points && gz.points.length >= 4) {
      const pts = gz.points.map(p => new THREE.Vector3(p[0], 0, p[1]));
      pts.push(pts[0].clone());
      const lineGeo = new THREE.BufferGeometry().setFromPoints(pts);
      const lineMat = new THREE.LineBasicMaterial({ color: gz.color });
      const line = new THREE.Line(lineGeo, lineMat);
      addMesh('safety', line);

      const cx = (gz.points[0][0] + gz.points[2][0]) / 2;
      const cz = (gz.points[0][1] + gz.points[2][1]) / 2;
      const w = Math.abs(gz.points[1][0] - gz.points[0][0]);
      const h = Math.abs(gz.points[3][1] - gz.points[0][1]);
      if (w > 0 && h > 0) {
        const fillGeo = new THREE.PlaneGeometry(w, h);
        const fillMat = new THREE.MeshStandardMaterial({ color: gz.color, transparent: true, opacity: 0.05, roughness: 0.9, side: THREE.DoubleSide });
        const fill = new THREE.Mesh(fillGeo, fillMat);
        fill.rotation.x = -Math.PI / 2;
        fill.position.set(cx, 0.05, cz);
        addMesh('safety', fill);
      }
    }
  });
}

function createTracks() {
  (D.parkingTracks || []).forEach(t => {
    const len = t.length || t.w;
    const geo = new THREE.BoxGeometry(len, 0.15, 1.6);
    const color = 0x2196f3;
    const mat = new THREE.MeshStandardMaterial({ color, roughness: 0.5, metalness: 0.6, emissive: color, emissiveIntensity: 0.06 });
    const m = new THREE.Mesh(geo, mat);
    m.position.set(t.x + len / 2, 0.08, t.y);
    m.castShadow = true;
    m.receiveShadow = true;
    m.userData = { type: 'track', name: t.name, track_type: t.type };
    addMesh('tracks', m);

    const railMat = new THREE.MeshStandardMaterial({ color: 0xb0bec5, roughness: 0.3, metalness: 0.8 });
    [-0.6, 0.6].forEach(offset => {
      const rail = new THREE.Mesh(new THREE.BoxGeometry(len, 0.12, 0.12), railMat);
      rail.position.set(t.x + len / 2, 0.2, t.y + offset);
      addMesh('tracks', rail);
    });

    const slpGeo = new THREE.BoxGeometry(0.25, 0.06, 2.2);
    const slpMat = new THREE.MeshStandardMaterial({ color: 0x455a64, roughness: 0.9 });
    for (let i = 0; i <= len; i += 1.2) {
      const slp = new THREE.Mesh(slpGeo, slpMat);
      slp.position.set(t.x + i, 0.03, t.y);
      addMesh('tracks', slp);
    }
  });
}

function createTrains() {
  const trainColor = 0x455a64;
  const bodyMat = new THREE.MeshStandardMaterial({ color: trainColor, roughness: 0.4, metalness: 0.5 });
  const roofMat = new THREE.MeshStandardMaterial({ color: 0x37474f, roughness: 0.6, metalness: 0.3 });
  const windowMat = new THREE.MeshStandardMaterial({ color: 0x1a237e, roughness: 0.2, metalness: 0.8, transparent: true, opacity: 0.7 });
  const stripeMat = new THREE.MeshStandardMaterial({ color: 0xf44336, roughness: 0.5, metalness: 0.3 });

  (D.parkingTrains || []).forEach(tr => {
    const tw = tr.w || 50;
    const th = tr.h || 3.2;
    const bodyGeo = new THREE.BoxGeometry(tw, th, 2.8);
    const body = new THREE.Mesh(bodyGeo, bodyMat);
    body.position.set(tr.x + tw / 2, th / 2 + 0.5, tr.y);
    body.castShadow = true;
    body.receiveShadow = true;
    body.userData = { type: 'train', name: '列车' };
    addMesh('trains', body);

    const roofGeo = new THREE.BoxGeometry(tw - 0.3, 0.3, 2.5);
    const roof = new THREE.Mesh(roofGeo, roofMat);
    roof.position.set(tr.x + tw / 2, th + 0.65, tr.y);
    addMesh('trains', roof);

    const stripeGeo = new THREE.BoxGeometry(tw + 0.1, 0.25, 2.85);
    const stripe = new THREE.Mesh(stripeGeo, stripeMat);
    stripe.position.set(tr.x + tw / 2, th * 0.6, tr.y);
    addMesh('trains', stripe);

    for (let wx = -tw / 2 + 2; wx < tw / 2 - 1; wx += 2.5) {
      [1.42, -1.42].forEach(sz => {
        const winGeo = new THREE.PlaneGeometry(0.8, 0.6);
        const win = new THREE.Mesh(winGeo, windowMat);
        win.position.set(tr.x + wx, th * 0.7, tr.y + sz);
        if (sz < 0) win.rotation.y = Math.PI;
        addMesh('trains', win);
      });
    }
  });
}

function createBogieStations() {
  (D.bogieMaintenance || []).forEach(bw => {
    const group = new THREE.Group();
    const baseGeo = new THREE.BoxGeometry(bw.w, 0.5, bw.h);
    const baseMat = new THREE.MeshStandardMaterial({ color: bw.color, roughness: 0.6, metalness: 0.3, transparent: true, opacity: 0.85 });
    const base = new THREE.Mesh(baseGeo, baseMat);
    base.position.set(bw.x + bw.w / 2, 0.25, bw.y + bw.h / 2);
    base.castShadow = true;
    base.receiveShadow = true;
    group.add(base);

    const edgeGeo = new THREE.EdgesGeometry(baseGeo);
    const edgeMat = new THREE.LineBasicMaterial({ color: 0x42a5f5 });
    const edge = new THREE.LineSegments(edgeGeo, edgeMat);
    edge.position.copy(base.position);
    group.add(edge);

    const toolGeo = new THREE.BoxGeometry(bw.w * 0.15, 1.5, bw.h * 0.4);
    const toolMat = new THREE.MeshStandardMaterial({ color: 0x1e88e5, roughness: 0.5, metalness: 0.5 });
    [-bw.w * 0.3, bw.w * 0.3].forEach(tx => {
      const tool = new THREE.Mesh(toolGeo, toolMat);
      tool.position.set(bw.x + bw.w / 2 + tx, 1.0, bw.y + bw.h / 2);
      tool.castShadow = true;
      group.add(tool);
    });

    group.userData = { type: 'bogie_ws', name: bw.name };
    addMesh('bogie', group);
  });
}

function createGantryCranes() {
  (D.gantryCranes || []).forEach(gc => {
    const group = new THREE.Group();
    const mat = new THREE.MeshStandardMaterial({ color: gc.color, roughness: 0.4, metalness: 0.6, emissive: gc.color, emissiveIntensity: 0.12 });
    const legW = gc.w || 3;
    const span = gc.h || 80;
    const h = gc.height || 10;

    const legGeo = new THREE.BoxGeometry(legW, h, 2);
    const leg1 = new THREE.Mesh(legGeo, mat);
    leg1.position.set(gc.x + legW / 2, h / 2, gc.y - span / 2);
    leg1.castShadow = true;
    group.add(leg1);

    const leg2 = new THREE.Mesh(legGeo, mat);
    leg2.position.set(gc.x + legW / 2, h / 2, gc.y + span / 2);
    leg2.castShadow = true;
    group.add(leg2);

    const beamGeo = new THREE.BoxGeometry(legW + 1, 1.2, span + 2);
    const beam = new THREE.Mesh(beamGeo, mat);
    beam.position.set(gc.x + legW / 2, h, gc.y);
    beam.castShadow = true;
    group.add(beam);

    const hookGeo = new THREE.BoxGeometry(0.5, 2, 0.5);
    const hookMat = new THREE.MeshStandardMaterial({ color: 0xe0e0e0, roughness: 0.3, metalness: 0.8 });
    const hook = new THREE.Mesh(hookGeo, hookMat);
    hook.position.set(gc.x + legW / 2, h - 2.5, gc.y);
    group.add(hook);

    const wireGeo = new THREE.CylinderGeometry(0.05, 0.05, 3, 4);
    const wireMat = new THREE.MeshStandardMaterial({ color: 0x9e9e9e });
    const wire = new THREE.Mesh(wireGeo, wireMat);
    wire.position.set(gc.x + legW / 2, h - 1, gc.y);
    group.add(wire);

    group.userData = { type: 'gantry_crane', name: gc.name };
    addMesh('crane-g', group);
  });
}

function createBridgeCranes() {
  (D.bridgeCranes || []).forEach(bc => {
    const group = new THREE.Group();
    const mat = new THREE.MeshStandardMaterial({ color: bc.color, roughness: 0.4, metalness: 0.55, emissive: bc.color, emissiveIntensity: 0.12 });
    const span = bc.w || 140;
    const beamD = bc.h || 3;
    const h = bc.height || 13;

    const bridgeGeo = new THREE.BoxGeometry(span + 2, 1.5, beamD);
    const bridge = new THREE.Mesh(bridgeGeo, mat);
    bridge.position.set(bc.x, h, bc.y);
    bridge.castShadow = true;
    group.add(bridge);

    const endMat = new THREE.MeshStandardMaterial({ color: bc.color, roughness: 0.45, metalness: 0.5 });
    [-span / 2 - 0.5, span / 2 + 0.5].forEach(ex => {
      const endGeo = new THREE.BoxGeometry(1.5, 2, beamD + 1);
      const end = new THREE.Mesh(endGeo, endMat);
      end.position.set(bc.x + ex, h + 1, bc.y);
      end.castShadow = true;
      group.add(end);
    });

    const trolleyGeo = new THREE.BoxGeometry(3, 0.8, beamD - 1);
    const trolleyMat = new THREE.MeshStandardMaterial({ color: 0xffc107, roughness: 0.4, metalness: 0.5 });
    const trolley = new THREE.Mesh(trolleyGeo, trolleyMat);
    trolley.position.set(bc.x, h - 1.2, bc.y);
    group.add(trolley);

    const hookGeo = new THREE.BoxGeometry(0.4, 1.5, 0.4);
    const hookMat = new THREE.MeshStandardMaterial({ color: 0xe0e0e0, roughness: 0.3, metalness: 0.8 });
    const hook = new THREE.Mesh(hookGeo, hookMat);
    hook.position.set(bc.x, h - 3, bc.y);
    group.add(hook);

    group.userData = { type: 'bridge_crane', name: bc.name };
    addMesh('crane-b', group);
  });
}

function createVehicleMaintenance() {
  (D.vehicleMaintenance || []).forEach(vm => {
    const geo = new THREE.BoxGeometry(vm.w, 0.3, vm.h);
    const mat = new THREE.MeshStandardMaterial({ color: vm.color, roughness: 0.7, metalness: 0.2, transparent: true, opacity: 0.65 });
    const m = new THREE.Mesh(geo, mat);
    m.position.set(vm.x + vm.w / 2, 0.15, vm.y + vm.h / 2);
    m.receiveShadow = true;
    m.userData = { type: 'vehicle_maint', name: vm.name };
    addMesh('vehicle', m);

    const edgeGeo = new THREE.EdgesGeometry(geo);
    const edgeMat = new THREE.LineBasicMaterial({ color: vm.color });
    const edge = new THREE.LineSegments(edgeGeo, edgeMat);
    edge.position.copy(m.position);
    addMesh('vehicle', edge);
  });
}

function createWorkshops() {
  const wallH = 6;
  const wallThick = 0.3;
  const wallMat = new THREE.MeshStandardMaterial({ color: 0x90a4ae, roughness: 0.8, metalness: 0.1, transparent: true, opacity: 0.4 });
  const roofMat = new THREE.MeshStandardMaterial({ color: 0x78909c, roughness: 0.6, metalness: 0.2 });

  (D.workshops || []).forEach(w => {
    const group = new THREE.Group();

    const floorGeo = new THREE.BoxGeometry(w.w, 0.25, w.h);
    const floorMat = new THREE.MeshStandardMaterial({ color: w.color, roughness: 0.75, metalness: 0.15, transparent: true, opacity: 0.7 });
    const floor = new THREE.Mesh(floorGeo, floorMat);
    floor.position.set(w.x + w.w / 2, 0.12, w.y + w.h / 2);
    floor.receiveShadow = true;
    group.add(floor);

    const hw = w.w / 2;
    const hh = w.h / 2;
    const cx = w.x + w.w / 2;
    const cz = w.y + w.h / 2;
    [
      { dw: w.w, dx: 0, dz: -hh },
      { dw: w.w, dx: 0, dz: hh },
      { dw: w.h, dx: -hw, dz: 0, rot: true },
      { dw: w.h, dx: hw, dz: 0, rot: true },
    ].forEach(wall => {
      const wallGeo = wall.rot
        ? new THREE.BoxGeometry(wallThick, wallH, wall.dw)
        : new THREE.BoxGeometry(wall.dw, wallH, wallThick);
      const wm = new THREE.Mesh(wallGeo, wallMat);
      wm.position.set(cx + wall.dx, wallH / 2, cz + wall.dz);
      wm.castShadow = true;
      group.add(wm);
    });

    const roofGeo = new THREE.BoxGeometry(w.w + 0.6, 0.2, w.h + 0.6);
    const roof = new THREE.Mesh(roofGeo, roofMat);
    roof.position.set(cx, wallH, cz);
    roof.castShadow = true;
    group.add(roof);

    group.userData = { type: 'workshop', name: w.name };
    addMesh('workshop', group);
  });
}

function createEquipment() {
  const allEquip = [...(D.bogieEquipment || []), ...(D.vehicleEquipment || []), ...(D.workshopEquipment || [])];
  allEquip.forEach(e => {
    const geo = new THREE.BoxGeometry(e.w, 1.5, e.h);
    const mat = new THREE.MeshStandardMaterial({ color: e.color, roughness: 0.45, metalness: 0.5, emissive: e.color, emissiveIntensity: 0.1 });
    const m = new THREE.Mesh(geo, mat);
    m.position.set(e.x + e.w / 2, 0.75, e.y + e.h / 2);
    m.castShadow = true;
    m.receiveShadow = true;
    m.userData = { type: 'equipment', name: e.name };
    addMesh('equip', m);

    const edgeGeo = new THREE.EdgesGeometry(geo);
    const edgeMat = new THREE.LineBasicMaterial({ color: e.color });
    const edge = new THREE.LineSegments(edgeGeo, edgeMat);
    edge.position.copy(m.position);
    addMesh('equip', edge);
  });
}

function createPlatforms() {
  (D.platforms || []).forEach(p => {
    const geo = new THREE.BoxGeometry(p.w, 0.6, p.h);
    const mat = new THREE.MeshStandardMaterial({ color: p.color, roughness: 0.5, metalness: 0.4, emissive: p.color, emissiveIntensity: 0.1 });
    const m = new THREE.Mesh(geo, mat);
    m.position.set(p.x + p.w / 2, 0.3, p.y + p.h / 2);
    m.castShadow = true;
    m.receiveShadow = true;
    m.userData = { type: 'platform', name: p.name };
    addMesh('platforms', m);

    const edgeGeo = new THREE.EdgesGeometry(geo);
    const edgeMat = new THREE.LineBasicMaterial({ color: 0xffd54f });
    const edge = new THREE.LineSegments(edgeGeo, edgeMat);
    edge.position.copy(m.position);
    addMesh('platforms', edge);
  });
}

function createLifts() {
  (D.liftPoints || []).forEach(l => {
    const group = new THREE.Group();
    const r = l.radius || 2.5;

    const baseGeo = new THREE.CylinderGeometry(r, r, 0.4, 12);
    const baseMat = new THREE.MeshStandardMaterial({ color: l.color, roughness: 0.5, metalness: 0.5, emissive: l.color, emissiveIntensity: 0.15 });
    const base = new THREE.Mesh(baseGeo, baseMat);
    base.position.set(l.x, 0.2, l.y);
    base.castShadow = true;
    group.add(base);

    const postGeo = new THREE.CylinderGeometry(0.15, 0.15, 3, 6);
    const postMat = new THREE.MeshStandardMaterial({ color: 0xbdbdbd, roughness: 0.4, metalness: 0.7 });
    const pr = r * 0.7;
    for (let i = 0; i < 4; i++) {
      const angle = (i / 4) * Math.PI * 2;
      const post = new THREE.Mesh(postGeo, postMat);
      post.position.set(l.x + Math.cos(angle) * pr, 1.9, l.y + Math.sin(angle) * pr);
      group.add(post);
    }

    group.userData = { type: 'lift', name: l.name };
    addMesh('lifts', group);
  });
}

function createWheelSets() {
  (D.wheelSetStands || []).forEach(ws => {
    const group = new THREE.Group();

    const frameGeo = new THREE.BoxGeometry(2, 0.8, 1);
    const frameMat = new THREE.MeshStandardMaterial({ color: ws.color, roughness: 0.6, metalness: 0.4 });
    const frame = new THREE.Mesh(frameGeo, frameMat);
    frame.position.set(ws.x + ws.w / 2, 0.9, ws.y + ws.h / 2);
    frame.castShadow = true;
    group.add(frame);

    const wheelGeo = new THREE.CylinderGeometry(0.45, 0.45, 0.15, 12);
    const wheelMat = new THREE.MeshStandardMaterial({ color: 0x424242, roughness: 0.3, metalness: 0.8 });
    [-0.4, 0.4].forEach(wz => {
      const wheel = new THREE.Mesh(wheelGeo, wheelMat);
      wheel.rotation.x = Math.PI / 2;
      wheel.position.set(ws.x + ws.w / 2, 0.55, ws.y + ws.h / 2 + wz);
      group.add(wheel);
    });

    const axleGeo = new THREE.CylinderGeometry(0.08, 0.08, 1, 6);
    const axleMat = new THREE.MeshStandardMaterial({ color: 0x757575, roughness: 0.4, metalness: 0.7 });
    const axle = new THREE.Mesh(axleGeo, axleMat);
    axle.rotation.x = Math.PI / 2;
    axle.position.set(ws.x + ws.w / 2, 0.5, ws.y + ws.h / 2);
    group.add(axle);

    group.userData = { type: 'wheel_set', name: ws.name };
    addMesh('wheelsets', group);
  });
}

function makeSprite(text, x, y, z, scale, fontSize, color, bgColor) {
  const c = document.createElement('canvas');
  const ctx = c.getContext('2d');
  const dpr = 4;
  const w = Math.max(text.length * fontSize * 0.8, 80);
  const h = fontSize * 2.4;
  c.width = w * dpr;
  c.height = h * dpr;
  ctx.scale(dpr, dpr);

  if (bgColor) {
    ctx.fillStyle = bgColor;
    ctx.beginPath();
    ctx.roundRect(1, 1, w - 2, h - 2, 6);
    ctx.fill();
  }

  ctx.fillStyle = color || '#ffffff';
  ctx.font = 'bold ' + fontSize + 'px "Microsoft YaHei", "PingFang SC", "Noto Sans SC", "SimHei", sans-serif';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.imageSmoothingEnabled = true;
  ctx.imageSmoothingQuality = 'high';
  ctx.fillText(text, w / 2, h / 2);

  const texture = new THREE.CanvasTexture(c);
  texture.minFilter = THREE.LinearFilter;
  texture.magFilter = THREE.LinearFilter;
  texture.generateMipmaps = false;
  const mat = new THREE.SpriteMaterial({ map: texture, depthWrite: false, sizeAttenuation: true });
  const sprite = new THREE.Sprite(mat);
  sprite.position.set(x, y, z);
  sprite.scale.set(scale, scale * (h / w), 1);
  return sprite;
}

function createLabels() {
  const addedTrackLabels = {};

  (D.parkingTracks || []).forEach(t => {
    if (!addedTrackLabels[t.name]) {
      addedTrackLabels[t.name] = true;
      const s = makeSprite(t.name, t.x + 3, 5, t.y, 16, 26, '#e1f5fe', 'rgba(10,36,80,0.9)');
      s.userData = { type: 'label' };
      addMesh('labels', s);
    }
  });

  (D.bogieMaintenance || []).forEach(bw => {
    const s = makeSprite(bw.name, bw.x + bw.w / 2, 5.5, bw.y + bw.h / 2, Math.min(bw.w, 18), 18, '#e3f2fd', 'rgba(13,71,161,0.85)');
    s.userData = { type: 'label' };
    addMesh('labels', s);
  });

  (D.gantryCranes || []).forEach(gc => {
    const s = makeSprite(gc.name, gc.x + 1.5, gc.height + 6, gc.y, 18, 22, '#fffde7', 'rgba(230,120,20,0.85)');
    s.userData = { type: 'label' };
    addMesh('labels', s);
  });

  (D.bridgeCranes || []).forEach(bc => {
    const s = makeSprite(bc.name, bc.x, bc.height + 6, bc.y, 20, 22, '#fff3e0', 'rgba(210,70,0,0.85)');
    s.userData = { type: 'label' };
    addMesh('labels', s);
  });

  (D.vehicleMaintenance || []).forEach(vm => {
    const s = makeSprite(vm.name, vm.x + vm.w / 2, 5, vm.y + vm.h / 2, Math.min(vm.w * 0.7, 18), 18, '#e8f5e9', 'rgba(27,94,32,0.85)');
    s.userData = { type: 'label' };
    addMesh('labels', s);
  });

  (D.workshops || []).forEach(w => {
    const s = makeSprite(w.name, w.x + w.w / 2, 9, w.y + w.h / 2, Math.min(w.w * 0.7, 15), 15, '#eceff1', 'rgba(30,45,56,0.85)');
    s.userData = { type: 'label' };
    addMesh('labels', s);
  });

  const allEquip = [...(D.bogieEquipment || []), ...(D.vehicleEquipment || []), ...(D.workshopEquipment || [])];
  allEquip.forEach(e => {
    const s = makeSprite(e.name.substring(0, 8), e.x + e.w / 2, 3.5, e.y + e.h / 2, 10, 13, '#fbe9e7', 'rgba(170,40,10,0.8)');
    s.userData = { type: 'label' };
    addMesh('labels', s);
  });

  (D.labels || []).forEach(lb => {
    const h = lb.size === 'large' ? 30 : (lb.size === 'medium' ? 22 : 15);
    const fs = lb.size === 'large' ? 28 : (lb.size === 'medium' ? 20 : 14);
    const s = makeSprite(lb.text, lb.x, h, lb.y, fs, fs, lb.color || '#ffffff', 'rgba(10,14,20,0.85)');
    s.userData = { type: 'label' };
    addMesh('labels', s);
  });
}

function setupUI() {
  window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  });

  const setView = (px, py, pz, tx, ty, tz) => {
    camera.position.set(px, py, pz);
    controls.target.set(tx, ty, tz);
    controls.update();
  };

  document.getElementById('btn-reset').onclick = () => setView(BCX, 280, BCY + 250, BCX, 0, BCY);
  document.getElementById('btn-top').onclick = () => setView(BCX, 500, BCY + 1, BCX, 0, BCY);
  document.getElementById('btn-side').onclick = () => setView(BCX + 350, 80, BCY, BCX, 0, BCY);
  document.getElementById('btn-front').onclick = () => setView(BCX, 80, BCY + 350, BCX, 0, BCY);

  const collapseBtn = document.getElementById('btn-collapse');
  const controlsPanel = document.getElementById('controls');
  collapseBtn.onclick = () => {
    const collapsed = controlsPanel.classList.toggle('collapsed');
    collapseBtn.textContent = collapsed ? '+' : '\u2212';
    collapseBtn.title = collapsed ? '展开面板' : '收缩面板';
  };

  const toggleMap = {
    'tog-tracks': 'tracks',
    'tog-trains': 'trains',
    'tog-bogie': 'bogie',
    'tog-crane-g': 'crane-g',
    'tog-crane-b': 'crane-b',
    'tog-vehicle': 'vehicle',
    'tog-workshop': 'workshop',
    'tog-equip': 'equip',
    'tog-platforms': 'platforms',
    'tog-lifts': 'lifts',
    'tog-wheelsets': 'wheelsets',
    'tog-safety': 'safety',
    'tog-columns': 'columns',
    'tog-labels': 'labels',
    'tog-walls': 'walls',
  };

  Object.entries(toggleMap).forEach(([togId, layerName]) => {
    const el = document.getElementById(togId);
    if (el) {
      el.addEventListener('change', e => {
        (allMeshGroups[layerName] || []).forEach(m => m.visible = e.target.checked);
      });
    }
  });

  document.getElementById('tog-floor').addEventListener('change', e => {
    (allMeshGroups['floor'] || []).forEach(m => m.visible = e.target.checked);
  });
}

function setupSearch() {
  const input = document.getElementById('search-input');
  const results = document.getElementById('search-results');
  const allItems = [];

  (D.parkingTracks || []).forEach(t => {
    const len = t.length || t.w;
    allItems.push({ type: '轨道', name: t.name, x: t.x + len / 2, y: 5, z: t.y, w: len });
  });
  (D.bogieMaintenance || []).forEach(b => allItems.push({ type: '转向架工位', name: b.name, x: b.x + b.w / 2, y: 5, z: b.y + b.h / 2, w: b.w }));
  (D.gantryCranes || []).forEach(c => allItems.push({ type: '龙门吊', name: c.name, x: c.x + 1.5, y: 5, z: c.y, w: c.h || 30 }));
  (D.bridgeCranes || []).forEach(c => allItems.push({ type: '桥式起重机', name: c.name, x: c.x, y: 5, z: c.y, w: c.w || 30 }));
  (D.vehicleMaintenance || []).forEach(v => allItems.push({ type: '车体检修', name: v.name, x: v.x + v.w / 2, y: 5, z: v.y + v.h / 2, w: v.w }));
  (D.workshops || []).forEach(w => allItems.push({ type: '检修间', name: w.name, x: w.x + w.w / 2, y: 5, z: w.y + w.h / 2, w: w.w }));

  input.addEventListener('input', e => {
    const q = e.target.value.trim();
    if (!q) { results.style.display = 'none'; return; }
    const matches = allItems.filter(i => i.name.includes(q)).slice(0, 15);
    if (matches.length === 0) { results.style.display = 'none'; return; }
    results.innerHTML = '';
    matches.forEach(m => {
      const div = document.createElement('div');
      div.className = 'sr-item';
      div.innerHTML = '<span style="color:#58a6ff">[' + m.type + ']</span> ' + m.name;
      div.onclick = () => {
        const dist = Math.max(m.w * 1.5, 40);
        camera.position.set(m.x + dist, dist * 1.2, m.z + dist);
        controls.target.set(m.x, 0, m.z);
        controls.update();
        results.style.display = 'none';
        input.value = '';
      };
      results.appendChild(div);
    });
    results.style.display = 'block';
  });

  input.addEventListener('blur', () => {
    setTimeout(() => results.style.display = 'none', 200);
  });
}

function setupRaycaster() {
  const tooltip = document.getElementById('tooltip');
  const interactTargets = [];
  ['tracks', 'trains', 'bogie', 'crane-g', 'crane-b', 'vehicle', 'workshop', 'equip', 'platforms', 'lifts', 'wheelsets'].forEach(key => {
    (allMeshGroups[key] || []).forEach(m => interactTargets.push(m));
  });

  renderer.domElement.addEventListener('mousemove', e => {
    mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
    raycaster.setFromCamera(mouse, camera);
    const hits = raycaster.intersectObjects(interactTargets, true);
    if (hits.length > 0) {
      let obj = hits[0].object;
      while (obj && !(obj.userData && obj.userData.type)) obj = obj.parent;
      if (obj && obj.userData && obj.userData.type) {
        const d = obj.userData;
        tooltip.classList.remove('hidden');
        tooltip.style.left = (e.clientX + 16) + 'px';
        tooltip.style.top = (e.clientY + 16) + 'px';
        let html = '<h4>' + d.name + '</h4>';
        if (d.type === 'track') html += '<p><span class="tag">轨道</span> 类型: ' + (d.track_type || '') + '</p>';
        else if (d.type === 'train') html += '<p><span class="tag">列车</span></p>';
        else if (d.type === 'bogie_ws') html += '<p><span class="tag">转向架工位</span></p>';
        else if (d.type === 'gantry_crane') html += '<p><span class="tag">龙门吊</span></p>';
        else if (d.type === 'bridge_crane') html += '<p><span class="tag">桥式起重机</span></p>';
        else if (d.type === 'vehicle_maint') html += '<p><span class="tag">车体检修</span></p>';
        else if (d.type === 'workshop') html += '<p><span class="tag">检修间</span></p>';
        else if (d.type === 'equipment') html += '<p><span class="tag">设备</span></p>';
        else if (d.type === 'platform') html += '<p><span class="tag">平台</span></p>';
        else if (d.type === 'lift') html += '<p><span class="tag">架车点</span></p>';
        else if (d.type === 'wheel_set') html += '<p><span class="tag">轮对存放</span></p>';
        tooltip.innerHTML = html;
        return;
      }
    }
    tooltip.classList.add('hidden');
  });
}

function drawMinimap() {
  const canvas = document.getElementById('minimap-canvas');
  const ctx = canvas.getContext('2d');
  const cw = canvas.width;
  const ch = canvas.height;

  ctx.fillStyle = '#0d1117';
  ctx.fillRect(0, 0, cw, ch);

  const bx = BCX - BW / 2;
  const bz = BCY - BH / 2;
  const scale = Math.min((cw - 20) / BW, (ch - 20) / BH);
  const ox = (cw - BW * scale) / 2;
  const oy = (ch - BH * scale) / 2;

  const tx = (x) => (x - bx) * scale + ox;
  const ty = (z) => (z - bz) * scale + oy;

  ctx.strokeStyle = '#30363d';
  ctx.lineWidth = 1;
  ctx.strokeRect(tx(bx), ty(bz), BW * scale, BH * scale);

  ctx.fillStyle = 'rgba(30,58,95,0.4)';
  ctx.fillRect(tx(bx), ty(bz), BW * scale, BH * scale);

  (D.greenZoneBorders || []).forEach(gz => {
    if (gz.points && gz.points.length >= 3) {
      ctx.strokeStyle = '#4caf50';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(tx(gz.points[0][0]), ty(gz.points[0][1]));
      gz.points.forEach(p => ctx.lineTo(tx(p[0]), ty(p[1])));
      ctx.closePath();
      ctx.stroke();
    }
  });

  (D.parkingTracks || []).forEach(t => {
    const len = t.length || t.w;
    ctx.strokeStyle = '#2196f3';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(tx(t.x), ty(t.y));
    ctx.lineTo(tx(t.x + len), ty(t.y));
    ctx.stroke();
  });

  (D.workshops || []).forEach(w => {
    ctx.fillStyle = 'rgba(144,164,174,0.4)';
    ctx.fillRect(tx(w.x), ty(w.y), w.w * scale, w.h * scale);
  });

  (D.bogieMaintenance || []).forEach(bw => {
    ctx.fillStyle = 'rgba(21,101,192,0.5)';
    ctx.fillRect(tx(bw.x), ty(bw.y), bw.w * scale, bw.h * scale);
  });
}

function animate() {
  requestAnimationFrame(animate);
  controls.update();
  renderer.render(scene, camera);
}

init();
</script>
</body>
</html>'''

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(html)

print(f"HTML 文件已生成: {OUTPUT}")
print(f"文件大小: {os.path.getsize(OUTPUT) / 1024:.1f} KB")
