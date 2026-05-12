import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// 工厂数据 - 基于图纸解析
const factoryData = {
  name: '上海北翟路车辆段检修库',
  // 建筑主体尺寸（米）- 根据图纸比例估算
  building: { width: 160, height: 90, depth: 12 },
  // 股道 - 20条股道（1条股线带多道岔）
  tracks: [
    // 主线1 - 北侧
    { id: 'G1', name: '1号线', x: -65, z: -30, length: 130, width: 3, rotation: 0 },
    { id: 'G2', name: '2号线', x: -65, z: -20, length: 130, width: 3, rotation: 0 },
    { id: 'G3', name: '3号线', x: -65, z: -10, length: 130, width: 3, rotation: 0 },
    { id: 'G4', name: '4号线', x: -65, z: 0, length: 130, width: 3, rotation: 0 },
    { id: 'G5', name: '5号线', x: -65, z: 10, length: 130, width: 3, rotation: 0 },
    { id: 'G6', name: '6号线', x: -65, z: 20, length: 130, width: 3, rotation: 0 },
    // 主线2 - 中部
    { id: 'G7', name: '7号线', x: -65, z: -25, length: 130, width: 3, rotation: 0 },
    { id: 'G8', name: '8号线', x: -65, z: -15, length: 130, width: 3, rotation: 0 },
    { id: 'G9', name: '9号线', x: -65, z: -5, length: 130, width: 3, rotation: 0 },
    { id: 'G10', name: '10号线', x: -65, z: 5, length: 130, width: 3, rotation: 0 },
    // 主线3 - 南侧
    { id: 'G11', name: '11号线', x: -65, z: -20, length: 130, width: 3, rotation: 0 },
    { id: 'G12', name: '12号线', x: -65, z: -10, length: 130, width: 3, rotation: 0 },
    { id: 'G13', name: '13号线', x: -65, z: 0, length: 130, width: 3, rotation: 0 },
    { id: 'G14', name: '14号线', x: -65, z: 10, length: 130, width: 3, rotation: 0 },
    { id: 'G15', name: '15号线', x: -65, z: 20, length: 130, width: 3, rotation: 0 },
    // 辅助线
    { id: 'G16', name: '16号线', x: -65, z: -15, length: 130, width: 3, rotation: 0 },
    { id: 'G17', name: '17号线', x: -65, z: -5, length: 130, width: 3, rotation: 0 },
    { id: 'G18', name: '18号线', x: -65, z: 5, length: 130, width: 3, rotation: 0 },
    { id: 'G19', name: '19号线', x: -65, z: 15, length: 130, width: 3, rotation: 0 },
    { id: 'G20', name: '20号线', x: -65, z: 25, length: 130, width: 3, rotation: 0 },
  ],
  // 区域 - 6个主要区域
  zones: [
    { id: 'Z1', name: '停车列检区', color: 0x2ecc71, x: -50, z: -35, width: 80, height: 20 },
    { id: 'Z2', name: '联合检修区', color: 0xf39c12, x: -50, z: -10, width: 80, height: 25 },
    { id: 'Z3', name: '周月检区', color: 0x3498db, x: -50, z: 20, width: 80, height: 20 },
    { id: 'Z4', name: '吹扫及清洗区', color: 0xe74c3c, x: 20, z: -35, width: 40, height: 20 },
    { id: 'Z5', name: '设备间', color: 0x9b59b6, x: 20, z: -10, width: 40, height: 25 },
    { id: 'Z6', name: '办公区', color: 0x1abc9c, x: 20, z: 20, width: 40, height: 20 },
  ],
  // 工位 - 60个工位（每个区域约10个）
  stations: generateStations(),
};

// 生成工位数据
function generateStations() {
  const stations = [];
  const zones = [
    { x: -50, z: -35, w: 80, h: 20, zone: '停车列检区' },
    { x: -50, z: -10, w: 80, h: 25, zone: '联合检修区' },
    { x: -50, z: 20, w: 80, h: 20, zone: '周月检区' },
    { x: 20, z: -35, w: 40, h: 20, zone: '吹扫及清洗区' },
    { x: 20, z: -10, w: 40, h: 25, zone: '设备间' },
    { x: 20, z: 20, w: 40, h: 20, zone: '办公区' },
  ];

  let id = 1;
  zones.forEach(zone => {
    const cols = zone.w > 50 ? 5 : 3;
    const rows = Math.ceil(10 / cols);
    const cellW = zone.w / cols;
    const cellH = zone.h / rows;

    for (let r = 0; r < rows && id <= 60; r++) {
      for (let c = 0; c < cols && id <= 60; c++) {
        stations.push({
          id: `S${String(id).padStart(2, '0')}`,
          name: `工位${id}`,
          zone: zone.zone,
          x: zone.x + cellW * (c + 0.5),
          z: zone.z + cellH * (r + 0.5),
          type: ['检修', '检测', '维修', '清洗', '存放'][id % 5],
        });
        id++;
      }
    }
  });

  return stations;
}

// 场景元素引用
let scene, camera, renderer, controls;
let trackMeshes = [], zoneMeshes = [], stationMeshes = [], labelSprites = [];
let floorMesh;

// 初始化场景
function init() {
  const container = document.getElementById('canvas-container');

  // 场景
  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x1a1a2e);
  scene.fog = new THREE.Fog(0x1a1a2e, 150, 300);

  // 相机
  camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
  camera.position.set(80, 100, 80);

  // 渲染器
  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(window.devicePixelRatio);
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  container.appendChild(renderer.domElement);

  // 控制器
  controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.05;
  controls.minDistance = 20;
  controls.maxDistance = 200;
  controls.maxPolarAngle = Math.PI / 2.1;

  // 光照
  setupLights();

  // 构建场景
  buildScene();

  // 事件监听
  setupEventListeners();

  // 开始动画循环
  animate();

  // 更新统计信息
  document.getElementById('track-count').textContent = factoryData.tracks.length;
  document.getElementById('station-count').textContent = factoryData.stations.length;
}

// 设置光照
function setupLights() {
  // 环境光
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
  scene.add(ambientLight);

  // 主方向光
  const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
  directionalLight.position.set(50, 100, 50);
  directionalLight.castShadow = true;
  directionalLight.shadow.mapSize.width = 2048;
  directionalLight.shadow.mapSize.height = 2048;
  directionalLight.shadow.camera.near = 0.5;
  directionalLight.shadow.camera.far = 300;
  directionalLight.shadow.camera.left = -100;
  directionalLight.shadow.camera.right = 100;
  directionalLight.shadow.camera.top = 100;
  directionalLight.shadow.camera.bottom = -100;
  scene.add(directionalLight);

  // 补光
  const fillLight = new THREE.DirectionalLight(0x4a90d9, 0.3);
  fillLight.position.set(-50, 50, -50);
  scene.add(fillLight);
}

// 构建场景
function buildScene() {
  // 建筑地面
  createFloor();

  // 墙体
  createWalls();

  // 股道
  createTracks();

  // 区域
  createZones();

  // 工位
  createStations();

  // 标签
  createLabels();
}

// 创建地面
function createFloor() {
  const geometry = new THREE.PlaneGeometry(
    factoryData.building.width,
    factoryData.building.height
  );
  const material = new THREE.MeshStandardMaterial({
    color: 0x2c3e50,
    roughness: 0.8,
    metalness: 0.2,
  });
  floorMesh = new THREE.Mesh(geometry, material);
  floorMesh.rotation.x = -Math.PI / 2;
  floorMesh.position.y = 0;
  floorMesh.receiveShadow = true;
  scene.add(floorMesh);
}

// 创建墙体
function createWalls() {
  const wallMaterial = new THREE.MeshStandardMaterial({
    color: 0x34495e,
    roughness: 0.9,
    metalness: 0.1,
  });

  const wallHeight = factoryData.building.depth;

  // 四周墙体
  const walls = [
    // 北墙
    { w: factoryData.building.width, h: wallHeight, d: 1, x: 0, z: -factoryData.building.height / 2 },
    // 南墙
    { w: factoryData.building.width, h: wallHeight, d: 1, x: 0, z: factoryData.building.height / 2 },
    // 西墙
    { w: 1, h: wallHeight, d: factoryData.building.height, x: -factoryData.building.width / 2, z: 0 },
    // 东墙（有门洞简化处理）
    { w: 1, h: wallHeight, d: factoryData.building.height, x: factoryData.building.width / 2, z: 0 },
  ];

  walls.forEach(w => {
    const geometry = new THREE.BoxGeometry(w.w, w.h, w.d);
    const mesh = new THREE.Mesh(geometry, wallMaterial);
    mesh.position.set(w.x, w.h / 2, w.z);
    mesh.castShadow = true;
    mesh.receiveShadow = true;
    scene.add(mesh);
  });
}

// 创建股道
function createTracks() {
  const trackMaterial = new THREE.MeshStandardMaterial({
    color: 0x4a90d9,
    roughness: 0.6,
    metalness: 0.4,
  });

  factoryData.tracks.forEach(track => {
    const geometry = new THREE.BoxGeometry(track.length, 0.2, track.width);
    const mesh = new THREE.Mesh(geometry, trackMaterial);
    mesh.position.set(track.x + track.length / 2, 0.1, track.z);
    mesh.castShadow = true;
    mesh.receiveShadow = true;

    // 存储数据用于交互
    mesh.userData = { type: 'track', ...track };
    trackMeshes.push(mesh);
    scene.add(mesh);

    // 添加轨道装饰（枕木效果）
    const sleeperGeometry = new THREE.BoxGeometry(0.5, 0.15, track.width * 1.2);
    const sleeperMaterial = new THREE.MeshStandardMaterial({ color: 0x3d3d3d });
    for (let i = 0; i < track.length; i += 2) {
      const sleeper = new THREE.Mesh(sleeperGeometry, sleeperMaterial);
      sleeper.position.set(track.x + i, 0.08, track.z);
      scene.add(sleeper);
    }
  });
}

// 创建区域
function createZones() {
  factoryData.zones.forEach(zone => {
    // 区域底面
    const geometry = new THREE.PlaneGeometry(zone.width, zone.height);
    const material = new THREE.MeshStandardMaterial({
      color: zone.color,
      transparent: true,
      opacity: 0.3,
      roughness: 0.8,
    });
    const mesh = new THREE.Mesh(geometry, material);
    mesh.rotation.x = -Math.PI / 2;
    mesh.position.set(zone.x + zone.width / 2, 0.02, zone.z + zone.height / 2);
    mesh.userData = { type: 'zone', ...zone };
    zoneMeshes.push(mesh);
    scene.add(mesh);

    // 区域边框
    const edgesGeometry = new THREE.EdgesGeometry(geometry);
    const edgesMaterial = new THREE.LineBasicMaterial({ color: zone.color, linewidth: 2 });
    const edges = new THREE.LineSegments(edgesGeometry, edgesMaterial);
    edges.rotation.x = -Math.PI / 2;
    edges.position.set(zone.x + zone.width / 2, 0.03, zone.z + zone.height / 2);
    scene.add(edges);
  });
}

// 创建工位
function createStations() {
  const stationGeometry = new THREE.BoxGeometry(4, 0.5, 3);
  const stationMaterial = new THREE.MeshStandardMaterial({
    color: 0x7ed321,
    roughness: 0.5,
    metalness: 0.3,
  });

  factoryData.stations.forEach((station, index) => {
    const mesh = new THREE.Mesh(stationGeometry, stationMaterial.clone());
    mesh.position.set(station.x, 0.25, station.z);
    mesh.castShadow = true;
    mesh.receiveShadow = true;
    mesh.userData = { type: 'station', ...station };
    stationMeshes.push(mesh);
    scene.add(mesh);

    // 工位编号标签
    createStationLabel(station);
  });
}

// 创建工位标签
function createStationLabel(station) {
  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d');
  canvas.width = 128;
  canvas.height = 64;

  // 背景
  ctx.fillStyle = 'rgba(74, 144, 217, 0.9)';
  ctx.roundRect(0, 0, 128, 64, 8);
  ctx.fill();

  // 文字
  ctx.fillStyle = '#ffffff';
  ctx.font = 'bold 28px Arial';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText(station.id, 64, 32);

  const texture = new THREE.CanvasTexture(canvas);
  const spriteMaterial = new THREE.SpriteMaterial({ map: texture });
  const sprite = new THREE.Sprite(spriteMaterial);
  sprite.position.set(station.x, 1.5, station.z);
  sprite.scale.set(3, 1.5, 1);
  sprite.userData = { type: 'label', station };
  labelSprites.push(sprite);
  scene.add(sprite);
}

// 创建区域标签
function createLabels() {
  factoryData.zones.forEach(zone => {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = 256;
    canvas.height = 64;

    // 背景
    ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
    ctx.roundRect(0, 0, 256, 64, 8);
    ctx.fill();

    // 文字
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 24px Arial';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(zone.name, 128, 32);

    const texture = new THREE.CanvasTexture(canvas);
    const spriteMaterial = new THREE.SpriteMaterial({ map: texture });
    const sprite = new THREE.Sprite(spriteMaterial);
    sprite.position.set(zone.x + zone.width / 2, 3, zone.z + zone.height / 2);
    sprite.scale.set(zone.width * 0.8, zone.height * 0.3, 1);
    scene.add(sprite);
  });
}

// 事件监听
function setupEventListeners() {
  // 窗口大小调整
  window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  });

  // 鼠标悬停
  const raycaster = new THREE.Raycaster();
  const mouse = new THREE.Vector2();
  const tooltip = document.getElementById('tooltip');

  renderer.domElement.addEventListener('mousemove', (event) => {
    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects([...stationMeshes, ...zoneMeshes]);

    if (intersects.length > 0) {
      const obj = intersects[0].object;
      const data = obj.userData;
      tooltip.classList.remove('hidden');
      tooltip.style.left = event.clientX + 15 + 'px';
      tooltip.style.top = event.clientY + 15 + 'px';
      tooltip.innerHTML = `
        <h4>${data.name || data.id}</h4>
        ${data.zone ? `<p>区域: ${data.zone}</p>` : ''}
        ${data.type ? `<p>类型: ${data.type}</p>` : ''}
      `;
    } else {
      tooltip.classList.add('hidden');
    }
  });

  // 按钮事件
  document.getElementById('btn-reset').addEventListener('click', () => {
    camera.position.set(80, 100, 80);
    controls.target.set(0, 0, 0);
    controls.update();
  });

  document.getElementById('btn-top').addEventListener('click', () => {
    camera.position.set(0, 150, 0);
    controls.target.set(0, 0, 0);
    controls.update();
  });

  document.getElementById('btn-side').addEventListener('click', () => {
    camera.position.set(150, 50, 0);
    controls.target.set(0, 0, 0);
    controls.update();
  });

  // 显示/隐藏控制
  document.getElementById('toggle-tracks').addEventListener('change', (e) => {
    trackMeshes.forEach(m => m.visible = e.target.checked);
  });

  document.getElementById('toggle-zones').addEventListener('change', (e) => {
    zoneMeshes.forEach(m => m.visible = e.target.checked);
  });

  document.getElementById('toggle-labels').addEventListener('change', (e) => {
    labelSprites.forEach(s => s.visible = e.target.checked);
  });

  document.getElementById('toggle-floor').addEventListener('change', (e) => {
    floorMesh.visible = e.target.checked;
  });
}

// 动画循环
function animate() {
  requestAnimationFrame(animate);
  controls.update();
  renderer.render(scene, camera);
}

// 启动
init();