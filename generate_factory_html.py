import json

with open(r'f:\自开发程序\工厂建模\factory_scene_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

SCALE = 0.5

def scale_val(v):
    return round(v * SCALE, 2)

def scale_zones(zones):
    out = []
    for z in zones:
        out.append({
            "x": round(z["x"] * SCALE, 2),
            "z": round(z["z"] * SCALE, 2),
            "w": round(z["w"] * SCALE, 2),
            "d": round(z["d"] * SCALE, 2),
            "color": z["color"],
            "label": z["label"],
            "sub": z.get("sub", "")
        })
    return out

def scale_tracks(tracks):
    out = []
    for t in tracks:
        out.append({
            "id": t["id"],
            "label": t.get("label", ""),
            "type": t.get("type", "complete"),
            "maxCars": t.get("maxCars", 8),
            "z": round(t["z"] * SCALE, 2),
            "color": t["color"]
        })
    return out

def scale_transfer(tt):
    return {
        "x": round(tt["x"] * SCALE, 2),
        "z": round(tt["z"] * SCALE, 2),
        "width": round(tt["width"] * SCALE, 2),
        "depth": round(tt["depth"] * SCALE, 2),
        "label": tt["label"]
    }

zones_js = json.dumps(scale_zones(data['zones']), ensure_ascii=False)
tracks_js = json.dumps(scale_tracks(data['tracks']), ensure_ascii=False)
transfer_js = json.dumps(scale_transfer(data.get('transferTable', {"x":0,"z":0,"width":2,"depth":1,"label":"移车台"})), ensure_ascii=False)

html = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>上海北翟路车辆段检修库 - 改造后总体工艺流程</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{overflow:hidden;font-family:"Microsoft YaHei","SimHei",sans-serif;background:#0d1117}
canvas{display:block}
#panel{position:fixed;top:12px;left:12px;background:rgba(13,17,23,0.94);color:#c9d1d9;padding:14px;border-radius:10px;width:260px;z-index:10;max-height:95vh;overflow-y:auto;border:1px solid rgba(48,54,61,0.8);backdrop-filter:blur(8px)}
#panel::-webkit-scrollbar{width:4px}
#panel::-webkit-scrollbar-thumb{background:rgba(48,54,61,0.6);border-radius:2px}
#panel h3{font-size:14px;margin-bottom:10px;color:#58a6ff;text-align:center;border-bottom:1px solid rgba(48,54,61,0.6);padding-bottom:8px}
#toggleBtn{position:fixed;top:12px;left:12px;z-index:11;background:rgba(13,17,23,0.9);color:#58a6ff;border:1px solid rgba(48,54,61,0.6);padding:6px 12px;border-radius:6px;cursor:pointer;font-size:13px;display:none}
.panel-section{margin-bottom:10px}
.panel-section summary{font-size:12px;color:#8b949e;cursor:pointer;padding:3px 0;user-select:none}
.panel-section summary:hover{color:#58a6ff}
.label{font-size:11px;color:#8b949e;margin:2px 0}
.btn{display:block;width:100%;padding:6px;margin:3px 0;border:1px solid rgba(48,54,61,0.5);background:rgba(22,27,34,0.8);color:#c9d1d9;border-radius:5px;cursor:pointer;font-size:11px;text-align:left}
.btn:hover{background:rgba(48,54,61,0.6);color:#fff}
.btn.active{background:rgba(56,139,253,0.15);color:#58a6ff;border-color:rgba(56,139,253,0.4)}
.input-group{display:flex;gap:4px;margin:4px 0}
.input-group input,.input-group select{flex:1;padding:5px;background:rgba(22,27,34,0.9);border:1px solid rgba(48,54,61,0.5);color:#c9d1d9;border-radius:4px;font-size:11px}
.input-group input::placeholder{color:#484f58}
.add-btn{padding:6px 12px;background:rgba(56,139,253,0.2);color:#58a6ff;border:1px solid rgba(56,139,253,0.4);border-radius:4px;cursor:pointer;font-size:11px;width:100%;margin-top:4px}
.add-btn:hover{background:rgba(56,139,253,0.3)}
#tooltip{position:fixed;pointer-events:none;background:rgba(13,17,23,0.96);color:#c9d1d9;padding:8px 12px;border-radius:6px;font-size:12px;display:none;z-index:100;border:1px solid rgba(48,54,61,0.6);max-width:280px}
#trainList{max-height:180px;overflow-y:auto}
.train-item{display:flex;justify-content:space-between;align-items:center;padding:4px 6px;margin:2px 0;background:rgba(22,27,34,0.6);border-radius:4px;font-size:10px}
.train-item span{color:#8b949e}
.del-btn{background:none;border:none;color:#f85149;cursor:pointer;font-size:13px;padding:0 4px}
#legend{position:fixed;bottom:12px;right:12px;background:rgba(13,17,23,0.9);color:#8b949e;padding:10px 12px;border-radius:8px;font-size:10px;z-index:10;border:1px solid rgba(48,54,61,0.6)}
.legend-item{display:flex;align-items:center;gap:5px;margin:2px 0}
.legend-color{width:12px;height:8px;border-radius:2px;flex-shrink:0}
#detailPanel{position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:rgba(13,17,23,0.97);color:#c9d1d9;padding:20px 24px;border-radius:12px;z-index:200;border:1px solid rgba(56,139,253,0.4);min-width:280px;max-width:400px;display:none;box-shadow:0 8px 32px rgba(0,0,0,0.6)}
#detailPanel h4{color:#58a6ff;font-size:15px;margin-bottom:12px;border-bottom:1px solid rgba(48,54,61,0.6);padding-bottom:8px}
#detailPanel .info-row{display:flex;justify-content:space-between;padding:4px 0;font-size:12px;border-bottom:1px solid rgba(48,54,61,0.3)}
#detailPanel .info-row .info-label{color:#8b949e}
#detailPanel .info-row .info-value{color:#e6edf3;font-weight:bold}
#detailPanel .close-btn{position:absolute;top:8px;right:12px;background:none;border:none;color:#8b949e;cursor:pointer;font-size:18px}
#detailPanel .close-btn:hover{color:#f85149}
#overlay{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.3);z-index:199;display:none}
.sect-header{font-size:11px;color:#58a6ff;font-weight:bold;margin:6px 0 3px;padding-top:4px;border-top:1px solid rgba(48,54,61,0.4)}
</style>
</head>
<body>
<button id="toggleBtn" onclick="togglePanel()">☰ 面板</button>
<div id="panel">
  <h3>🏭 改造后总体工艺流程</h3>
  <details class="panel-section" open>
    <summary>👁 视图控制</summary>
    <button class="btn" onclick="setView('top',this)">俯视图</button>
    <button class="btn" onclick="setView('front',this)">前视图</button>
    <button class="btn active" onclick="setView('perspective',this)">透视图</button>
    <button class="btn" onclick="resetCamera()">重置相机</button>
  </details>
  <details class="panel-section" open>
    <summary>📂 图层控制</summary>
    <button class="btn active" id="lyr_building" onclick="toggleLayer('building',this)">厂房结构</button>
    <button class="btn active" id="lyr_tracks" onclick="toggleLayer('tracks',this)">股道线路</button>
    <button class="btn active" id="lyr_transfer" onclick="toggleLayer('transfer',this)">移车台</button>
    <button class="btn active" id="lyr_zones" onclick="toggleLayer('zones',this)">检修区域</button>
    <button class="btn active" id="lyr_trains" onclick="toggleLayer('trains',this)">列车模型</button>
    <button class="btn active" id="lyr_labels" onclick="toggleLayer('labels',this)">文字标注</button>
  </details>
  <details class="panel-section" open>
    <summary>🚂 整列列车管理 (24-29道)</summary>
    <div class="label" style="color:#58a6ff;font-size:10px;margin-bottom:4px">8节编组，仅需车号</div>
    <div class="input-group"><input id="trainId" placeholder="车号(如201)"></div>
    <div class="input-group"><select id="trainTrack"><option value="">选择股道</option></select></div>
    <button class="add-btn" onclick="addCompleteTrain()">添加整列列车</button>
    <div id="trainList"></div>
  </details>
  <details class="panel-section" open>
    <summary>🔧 解编车辆管理 (30/库道)</summary>
    <div class="label" style="color:#58a6ff;font-size:10px;margin-bottom:4px">最多3节，格式:车号-节号</div>
    <div class="input-group"><input id="sepId" placeholder="车辆号(如2018-1)"></div>
    <div class="input-group"><select id="sepTrack"><option value="">选择股道</option></select></div>
    <button class="add-btn" onclick="addSeparatedCar()">添加解编车辆</button>
    <div id="sepList"></div>
  </details>
  <details class="panel-section">
    <summary>📊 统计信息</summary>
    <div class="label">右侧区域: <span style="color:#58a6ff">''' + str(len(data['zones'])) + '''个</span></div>
    <div class="label">股道总数: <span style="color:#58a6ff">''' + str(len(data['tracks'])) + '''条</span></div>
    <div class="label">移车台: <span style="color:#58a6ff">1座</span></div>
  </details>
  <div style="margin-top:8px;font-size:10px;color:#484f58;text-align:center">点击区域查看详情 | 滚轮缩放 | 右键旋转</div>
</div>
<div id="tooltip"></div>
<div id="overlay" onclick="closeDetail()"></div>
<div id="detailPanel">
  <button class="close-btn" onclick="closeDetail()">✕</button>
  <h4 id="detailTitle"></h4>
  <div id="detailContent"></div>
</div>
<div id="legend">
  <div class="legend-item"><div class="legend-color" style="background:#4caf50"></div>有电调试道</div>
  <div class="legend-item"><div class="legend-color" style="background:#e8a030"></div>无电调试道</div>
  <div class="legend-item"><div class="legend-color" style="background:#ef5350"></div>临修道</div>
  <div class="legend-item"><div class="legend-color" style="background:#5c4033"></div>库道/存车线</div>
  <div class="legend-item"><div class="legend-color" style="background:#00897b"></div>移车台</div>
  <div class="legend-item"><div class="legend-color" style="background:#2e7d32"></div>装备保障区</div>
  <div class="legend-item"><div class="legend-color" style="background:#d4553a"></div>部件检修区</div>
  <div class="legend-item"><div class="legend-color" style="background:#e8a030"></div>缓车区</div>
  <div class="legend-item"><div class="legend-color" style="background:#7b3f8a"></div>轮对区</div>
  <div class="legend-item"><div class="legend-color" style="background:#3a6fa0"></div>转向架区</div>
</div>
<script type="importmap">{"imports":{"three":"https://unpkg.com/three@0.160.0/build/three.module.js","three/addons/":"https://unpkg.com/three@0.160.0/examples/jsm/"}}</script>
<script type="module">
import*as THREE from'three';
import{OrbitControls}from'three/addons/controls/OrbitControls.js';

const D_zones=''' + zones_js + r''';
const D_tracks=''' + tracks_js + r''';
const D_transfer=''' + transfer_js + r''';

const renderer=new THREE.WebGLRenderer({antialias:true});
renderer.setSize(window.innerWidth,window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio,2));
renderer.shadowMap.enabled=true;
renderer.shadowMap.type=THREE.PCFSoftShadowMap;
renderer.toneMapping=THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure=1.2;
document.body.appendChild(renderer.domElement);

const scene=new THREE.Scene();
scene.background=new THREE.Color(0x0d1117);
scene.fog=new THREE.FogExp2(0x0d1117,0.006);

const camera=new THREE.PerspectiveCamera(50,window.innerWidth/window.innerHeight,0.1,200);
camera.position.set(25,40,30);

const controls=new OrbitControls(camera,renderer.domElement);
controls.enableDamping=true;
controls.dampingFactor=0.08;
controls.target.set(0,0,2);
controls.maxPolarAngle=Math.PI*0.48;
controls.minDistance=10;
controls.maxDistance=120;

scene.add(new THREE.AmbientLight(0xffffff,0.65));
const dl=new THREE.DirectionalLight(0xffffff,0.9);
dl.position.set(20,40,15);
dl.castShadow=true;
dl.shadow.mapSize.set(4096,4096);
dl.shadow.camera.left=-45;dl.shadow.camera.right=45;
dl.shadow.camera.top=35;dl.shadow.camera.bottom=-35;
scene.add(dl);
scene.add(new THREE.HemisphereLight(0x87ceeb,0x362a28,0.35));

const raycaster=new THREE.Raycaster();
const mouse=new THREE.Vector2();
const tooltip=document.getElementById('tooltip');
const layers={};
const iMeshes=[];

function ensureGroup(n){
  if(!layers[n]){const g=new THREE.Group();g.name=n;scene.add(g);layers[n]=g;}
  return layers[n];
}

function mkLabel(text,color,fontSize){
  const c=document.createElement('canvas');
  const ctx=c.getContext('2d');
  const s=4;
  const fs=fontSize*s;
  const lines=text.split('\n');
  ctx.font='bold '+fs+'px "Microsoft YaHei","SimHei",sans-serif';
  let mw=0;
  lines.forEach(l=>{const m=ctx.measureText(l);if(m.width>mw)mw=m.width;});
  const lh=fs*1.3;
  c.width=Math.ceil(mw+12*s);
  c.height=Math.ceil(lines.length*lh+6*s);
  ctx.font='bold '+fs+'px "Microsoft YaHei","SimHei",sans-serif';
  ctx.fillStyle=color||'#ffffff';
  ctx.textAlign='center';
  ctx.textBaseline='middle';
  const cx=c.width/2,cy=c.height/2;
  lines.forEach((l,i)=>{
    ctx.fillText(l,cx,cy+(i-(lines.length-1)/2)*lh);
  });
  const tex=new THREE.CanvasTexture(c);
  tex.minFilter=THREE.LinearFilter;
  const mat=new THREE.SpriteMaterial({map:tex,transparent:true,depthWrite:false,depthTest:false});
  const sp=new THREE.Sprite(mat);
  const sc=Math.min(c.width/(s*10),c.height/(s*5));
  sp.scale.set(sc,sc*(c.height/c.width),1);
  return sp;
}

function addLabel(g,text,pos,color,fontSize){
  const sp=mkLabel(text,color||'#ffffff',fontSize||12);
  sp.position.copy(pos);
  g.add(sp);
  sp.userData.layer='labels';
  iMeshes.push(sp);
  return sp;
}

const SW=60,SD=40;
const bg=ensureGroup('building');
const ground=new THREE.Mesh(
  new THREE.BoxGeometry(SW,0.3,SD),
  new THREE.MeshStandardMaterial({color:0x151a28,roughness:0.95})
);
ground.position.set(0,-0.15,2);
ground.receiveShadow=true;
bg.add(ground);

const gridHelper=new THREE.GridHelper(SW,60,0x1a2233,0x1a2233);
gridHelper.position.y=0.01;
bg.add(gridHelper);

const wallMat=new THREE.MeshStandardMaterial({color:0x2a3040,roughness:0.8,transparent:true,opacity:0.15});
const wallH=2.5;
[[-SW/2,0,SD/2,0.2],[SW/2,0,SD/2,0.2],[0,0,-SD/2,SW],[0,0,SD/2,SW]].forEach(([x,_,z,w])=>{
  const isX=w<1;
  const m=new THREE.Mesh(new THREE.BoxGeometry(isX?0.15:w,wallH,isX?SD:0.15),wallMat);
  m.position.set(x,wallH/2,z);
  bg.add(m);
});

const zg=ensureGroup('zones');
D_zones.forEach(z=>{
  const g=new THREE.Group();
  const base=new THREE.Mesh(
    new THREE.BoxGeometry(z.w,0.12,z.d),
    new THREE.MeshStandardMaterial({color:z.color,roughness:0.55,metalness:0.05,transparent:true,opacity:0.88})
  );
  base.position.set(0,0.06,0);
  base.receiveShadow=true;
  g.add(base);

  const h=Math.max(0.6,Math.min(z.d*0.35,2));
  const edge=new THREE.LineSegments(
    new THREE.EdgesGeometry(new THREE.BoxGeometry(z.w,h,z.d)),
    new THREE.LineBasicMaterial({color:z.color,transparent:true,opacity:0.5})
  );
  edge.position.y=h/2;
  g.add(edge);

  const body=new THREE.Mesh(
    new THREE.BoxGeometry(z.w,h-0.12,z.d),
    new THREE.MeshStandardMaterial({color:z.color,roughness:0.6,transparent:true,opacity:0.2})
  );
  body.position.y=h/2+0.06;
  g.add(body);

  g.position.set(z.x,0,z.z);
  const fullLabel=z.label+(z.sub?' '+z.sub:'');
  g.userData={type:'zone',label:fullLabel,zData:z};
  iMeshes.push(base);
  base.userData={type:'zone',label:fullLabel,zData:z};

  const labelSize=z.label.length>6?7:9;
  addLabel(g,z.label,new THREE.Vector3(0,h+0.5,0),'#ffffff',labelSize);
  if(z.sub)addLabel(g,z.sub,new THREE.Vector3(0,h+1.1,0),'#8b949e',6);
  zg.add(g);
});

const tg=ensureGroup('tracks');
const trackZMap={};
D_tracks.forEach(t=>{
  trackZMap[t.id]=t.z;
  const rc=t.color;
  const zone=new THREE.Mesh(
    new THREE.BoxGeometry(SW,0.06,1.0),
    new THREE.MeshStandardMaterial({color:rc,roughness:0.7,transparent:true,opacity:0.2})
  );
  zone.position.set(0,0.03,t.z);
  tg.add(zone);

  const rm=new THREE.MeshStandardMaterial({color:0x999999,roughness:0.3,metalness:0.6});
  const r1=new THREE.Mesh(new THREE.BoxGeometry(SW,0.08,0.08),rm);
  r1.position.set(0,0.1,t.z-0.2);
  tg.add(r1);
  const r2=new THREE.Mesh(new THREE.BoxGeometry(SW,0.08,0.08),rm);
  r2.position.set(0,0.1,t.z+0.2);
  tg.add(r2);

  const sm=new THREE.MeshStandardMaterial({color:0x555555,roughness:0.8});
  for(let x=-SW/2+1;x<=SW/2-1;x+=1.2){
    const s=new THREE.Mesh(new THREE.BoxGeometry(0.1,0.04,0.5),sm);
    s.position.set(x,0.06,t.z);
    tg.add(s);
  }

  const lc=t.type==='complete'
    ? (t.color===0x4caf50?'#66bb6a':t.color===0xe8a030?'#ffcc66':'#ef9a9a')
    : '#8d6e63';
  const trackLabel=t.label?t.id+'道 '+t.label:t.id+'道';
  addLabel(tg,trackLabel,new THREE.Vector3(-SW/2+3,0.7,t.z),lc,8);
});

const ttg=ensureGroup('transfer');
const tt=new THREE.Mesh(
  new THREE.BoxGeometry(D_transfer.width,0.15,D_transfer.depth),
  new THREE.MeshStandardMaterial({color:0x00897b,roughness:0.5,metalness:0.2,transparent:true,opacity:0.7})
);
tt.position.set(D_transfer.x,0.075,D_transfer.z+D_transfer.depth/2);
tt.receiveShadow=true;
ttg.add(tt);

const ttEdge=new THREE.LineSegments(
  new THREE.EdgesGeometry(new THREE.BoxGeometry(D_transfer.width,0.8,D_transfer.depth)),
  new THREE.LineBasicMaterial({color:0x00897b,transparent:true,opacity:0.6})
);
ttEdge.position.set(D_transfer.x,0.4,D_transfer.z+D_transfer.depth/2);
ttg.add(ttEdge);

const ttArrow=new THREE.Mesh(
  new THREE.ConeGeometry(0.3,0.6,4),
  new THREE.MeshStandardMaterial({color:0x00897b,transparent:true,opacity:0.5})
);
ttArrow.position.set(D_transfer.x,1.2,D_transfer.z+D_transfer.depth/2);
ttArrow.rotation.x=Math.PI;
ttg.add(ttArrow);

addLabel(ttg,'移车台',new THREE.Vector3(D_transfer.x,1.8,D_transfer.z+D_transfer.depth/2),'#4dd0e1',9);

const trainColors=['#1565c0','#c62828','#2e7d32','#e65100','#6a1b9a','#00838f','#ad1457','#00695c'];
const trainsG=ensureGroup('trains');
const trainMap={};

function mkCompleteTrain(color){
  const g=new THREE.Group();
  const c=new THREE.Color(color);
  const cw=1.5,ch=0.8,cd=0.6,gap=0.1;
  const carCount=8;
  const tw=carCount*(cw+gap)-gap;
  for(let i=0;i<carCount;i++){
    const body=new THREE.Mesh(
      new THREE.BoxGeometry(cw,ch,cd),
      new THREE.MeshStandardMaterial({color:c,roughness:0.4,metalness:0.3})
    );
    body.position.x=i*(cw+gap)-tw/2+cw/2;
    body.position.y=ch/2+0.12;
    body.castShadow=true;
    g.add(body);
    const roof=new THREE.Mesh(
      new THREE.BoxGeometry(cw-0.04,0.08,cd-0.04),
      new THREE.MeshStandardMaterial({color:new THREE.Color(color).multiplyScalar(0.7),roughness:0.5})
    );
    roof.position.set(body.position.x,ch+0.16,0);
    g.add(roof);
    for(let s=-1;s<=1;s+=2){
      for(let ax=-1;ax<=1;ax+=2){
        const wh=new THREE.Mesh(
          new THREE.CylinderGeometry(0.1,0.1,0.05,12),
          new THREE.MeshStandardMaterial({color:0x333333,roughness:0.3,metalness:0.7})
        );
        wh.rotation.z=Math.PI/2;
        wh.position.set(body.position.x+ax*0.4,0.08,s*0.25);
        g.add(wh);
      }
    }
  }
  return g;
}

function mkSeparatedCar(color){
  const g=new THREE.Group();
  const c=new THREE.Color(color);
  const cw=1.8,ch=0.8,cd=0.6;
  const body=new THREE.Mesh(
    new THREE.BoxGeometry(cw,ch,cd),
    new THREE.MeshStandardMaterial({color:c,roughness:0.4,metalness:0.3})
  );
  body.position.y=ch/2+0.12;
  body.castShadow=true;
  g.add(body);
  const roof=new THREE.Mesh(
    new THREE.BoxGeometry(cw-0.04,0.08,cd-0.04),
    new THREE.MeshStandardMaterial({color:new THREE.Color(color).multiplyScalar(0.7),roughness:0.5})
  );
  roof.position.y=ch+0.16;
  g.add(roof);
  for(let s=-1;s<=1;s+=2){
    for(let ax=-1;ax<=1;ax+=2){
      const wh=new THREE.Mesh(
        new THREE.CylinderGeometry(0.1,0.1,0.05,12),
        new THREE.MeshStandardMaterial({color:0x333333,roughness:0.3,metalness:0.7})
      );
      wh.rotation.z=Math.PI/2;
      wh.position.set(ax*0.5,0.08,s*0.25);
      g.add(wh);
    }
  }
  return g;
}

function addCompleteTrainToScene(train){
  const z=trackZMap[train.track];
  if(z===undefined)return;
  const key='c_'+train.id;
  if(trainMap[key]){trainsG.remove(trainMap[key]);delete trainMap[key];}
  const colIdx=Object.keys(trainMap).length%trainColors.length;
  const shape=mkCompleteTrain(trainColors[colIdx]);
  shape.position.set(8,0,z);
  const fullLabel=train.id+'车 (8节) -> '+train.track+'道';
  shape.userData={type:'train',label:fullLabel};
  trainsG.add(shape);
  trainMap[key]=shape;
  iMeshes.push(shape.children[0]);
  shape.children[0].userData={type:'train',label:fullLabel};
  addLabel(shape,train.id+'车',new THREE.Vector3(0,1.8,0),'#ffffff',9);
}

function addSeparatedCarToScene(car){
  const z=trackZMap[car.track];
  if(z===undefined)return;
  const key='s_'+car.id;
  if(trainMap[key]){trainsG.remove(trainMap[key]);delete trainMap[key];}
  const trackCars=separatedCars.filter(c=>c.track===car.track);
  const idx=trackCars.indexOf(car);
  const colIdx=Object.keys(trainMap).length%trainColors.length;
  const shape=mkSeparatedCar(trainColors[colIdx]);
  const xOff=5+idx*3;
  shape.position.set(xOff,0,z);
  const fullLabel=car.id+' -> '+car.track+'道';
  shape.userData={type:'train',label:fullLabel};
  trainsG.add(shape);
  trainMap[key]=shape;
  iMeshes.push(shape.children[0]);
  shape.children[0].userData={type:'train',label:fullLabel};
  addLabel(shape,car.id,new THREE.Vector3(0,1.5,0),'#ffffff',8);
}

const defaultCompleteTrains=[
  {id:'201',track:'29'},
  {id:'202',track:'28'},
  {id:'203',track:'27'},
  {id:'204',track:'26'},
  {id:'205',track:'25'},
  {id:'206',track:'24'}
];

const defaultSeparatedCars=[
  {id:'2018-1',track:'30'},
  {id:'2018-2',track:'30'},
  {id:'2018-3',track:'30'},
  {id:'2019-1',track:'31'},
  {id:'2019-2',track:'31'},
  {id:'2020-1',track:'32'},
  {id:'2020-2',track:'32'},
  {id:'2020-3',track:'32'},
  {id:'2021-1',track:'库1'},
  {id:'2021-2',track:'库1'},
  {id:'2021-3',track:'库1'},
  {id:'2022-1',track:'库2'},
  {id:'2022-2',track:'库2'},
  {id:'2023-1',track:'库3'},
  {id:'2023-2',track:'库3'},
  {id:'2023-3',track:'库3'}
];

let completeTrains=JSON.parse(localStorage.getItem('factory_complete')||'null');
if(!completeTrains||!completeTrains.length){completeTrains=defaultCompleteTrains;}

let separatedCars=JSON.parse(localStorage.getItem('factory_separated')||'null');
if(!separatedCars||!separatedCars.length){separatedCars=defaultSeparatedCars;}

completeTrains.forEach(t=>addCompleteTrainToScene(t));
separatedCars.forEach(c=>addSeparatedCarToScene(c));
renderCompleteList();
renderSeparatedList();

const completeTracks=D_tracks.filter(t=>t.type==='complete');
const separatedTracks=D_tracks.filter(t=>t.type==='separated');

const ts=document.getElementById('trainTrack');
completeTracks.forEach(t=>{
  const o=document.createElement('option');
  o.value=t.id;o.textContent=t.id+'道 '+t.label;
  ts.appendChild(o);
});

const ss=document.getElementById('sepTrack');
separatedTracks.forEach(t=>{
  const o=document.createElement('option');
  o.value=t.id;o.textContent=t.id+'道';
  ss.appendChild(o);
});

window.addCompleteTrain=function(){
  const id=document.getElementById('trainId').value.trim();
  const track=document.getElementById('trainTrack').value;
  if(!id||!track){alert('请输入车号并选择股道');return;}
  const existing=completeTrains.findIndex(t=>t.id===id);
  const train={id:id,track:track};
  if(existing>=0)completeTrains[existing]=train;else completeTrains.push(train);
  localStorage.setItem('factory_complete',JSON.stringify(completeTrains));
  addCompleteTrainToScene(train);
  renderCompleteList();
  document.getElementById('trainId').value='';
};

window.removeCompleteTrain=function(id){
  completeTrains=completeTrains.filter(t=>t.id!==id);
  localStorage.setItem('factory_complete',JSON.stringify(completeTrains));
  const key='c_'+id;
  if(trainMap[key]){trainsG.remove(trainMap[key]);delete trainMap[key];}
  renderCompleteList();
};

function renderCompleteList(){
  const el=document.getElementById('trainList');
  el.innerHTML=completeTrains.map(function(t){
    return '<div class="train-item"><span>'+t.id+'车 → '+t.track+'道 (8节)</span><button class="del-btn" onclick="removeCompleteTrain(\''+t.id+'\')">&#10005;</button></div>';
  }).join('');
}

window.addSeparatedCar=function(){
  const id=document.getElementById('sepId').value.trim();
  const track=document.getElementById('sepTrack').value;
  if(!id||!track){alert('请输入车辆号并选择股道');return;}
  const trackCars=separatedCars.filter(c=>c.track===track);
  if(trackCars.length>=3){alert(track+'道最多存放3节车');return;}
  const existing=separatedCars.findIndex(c=>c.id===id);
  const car={id:id,track:track};
  if(existing>=0)separatedCars[existing]=car;else separatedCars.push(car);
  localStorage.setItem('factory_separated',JSON.stringify(separatedCars));
  addSeparatedCarToScene(car);
  renderSeparatedList();
  document.getElementById('sepId').value='';
};

window.removeSeparatedCar=function(id){
  separatedCars=separatedCars.filter(c=>c.id!==id);
  localStorage.setItem('factory_separated',JSON.stringify(separatedCars));
  const key='s_'+id;
  if(trainMap[key]){trainsG.remove(trainMap[key]);delete trainMap[key];}
  renderSeparatedList();
};

function renderSeparatedList(){
  const el=document.getElementById('sepList');
  const grouped={};
  separatedCars.forEach(c=>{
    if(!grouped[c.track])grouped[c.track]=[];
    grouped[c.track].push(c);
  });
  let html='';
  Object.keys(grouped).sort().forEach(track=>{
    html+='<div style="font-size:10px;color:#58a6ff;margin:4px 0 2px">'+track+'道:</div>';
    grouped[track].forEach(c=>{
      html+='<div class="train-item"><span>'+c.id+'</span><button class="del-btn" onclick="removeSeparatedCar(\''+c.id+'\')">&#10005;</button></div>';
    });
  });
  el.innerHTML=html;
}

function showDetail(zData){
  const dp=document.getElementById('detailPanel');
  const dt=document.getElementById('detailTitle');
  const dc=document.getElementById('detailContent');
  const colorHex='#'+zData.color.toString(16).padStart(6,'0');
  dt.innerHTML='<span style="display:inline-block;width:14px;height:14px;border-radius:3px;background:'+colorHex+';vertical-align:middle;margin-right:6px"></span>'+zData.label;
  const realW=Math.round(zData.w/0.5);
  const realD=Math.round(zData.d/0.5);
  const area=realW*realD;
  let rows=[
    ['区域名称',zData.label],
    ['实际尺寸',realW+'m × '+realD+'m'],
    ['占地面积',area+'m²']
  ];
  if(zData.sub)rows.push(['包含工位',zData.sub]);
  rows.push(['坐标位置','('+Math.round(zData.x/0.5)+', '+Math.round(zData.z/0.5)+')']);
  dc.innerHTML=rows.map(function(r){
    return '<div class="info-row"><span class="info-label">'+r[0]+'</span><span class="info-value">'+r[1]+'</span></div>';
  }).join('');
  dp.style.display='block';
  document.getElementById('overlay').style.display='block';
}

window.closeDetail=function(){
  document.getElementById('detailPanel').style.display='none';
  document.getElementById('overlay').style.display='none';
};

window.setView=function(v,btn){
  document.querySelectorAll('.panel-section .btn').forEach(function(b){b.classList.remove('active')});
  if(btn)btn.classList.add('active');
  if(v==='top'){camera.position.set(0,55,2);controls.target.set(0,0,2);}
  else if(v==='front'){camera.position.set(0,15,50);controls.target.set(0,0,2);}
  else{camera.position.set(25,40,30);controls.target.set(0,0,2);}
  controls.update();
};

window.resetCamera=function(){camera.position.set(25,40,30);controls.target.set(0,0,2);controls.update();};
window.toggleLayer=function(n,btn){const g=layers[n];if(g){g.visible=!g.visible;btn.classList.toggle('active');}};
window.togglePanel=function(){const p=document.getElementById('panel');const b=document.getElementById('toggleBtn');if(p.style.display==='none'){p.style.display='';b.style.display='none';}else{p.style.display='none';b.style.display='';}};

function onMM(e){
  mouse.x=(e.clientX/window.innerWidth)*2-1;
  mouse.y=-(e.clientY/window.innerHeight)*2+1;
  raycaster.setFromCamera(mouse,camera);
  const hits=raycaster.intersectObjects(iMeshes,true);
  if(hits.length>0){
    let obj=hits[0].object;
    while(obj&&!obj.userData.label)obj=obj.parent;
    if(obj&&obj.userData.label){
      tooltip.style.display='block';
      tooltip.style.left=(e.clientX+12)+'px';
      tooltip.style.top=(e.clientY+12)+'px';
      const zD=obj.userData.zData;
      let html='<div style="color:#58a6ff;font-weight:bold;margin-bottom:3px">'+obj.userData.label+'</div>';
      if(zD){html+='<div style="color:#8b949e;font-size:10px">点击查看详情</div>';}
      tooltip.innerHTML=html;
      document.body.style.cursor='pointer';
      return;
    }
  }
  tooltip.style.display='none';
  document.body.style.cursor='default';
}
renderer.domElement.addEventListener('mousemove',onMM);

renderer.domElement.addEventListener('click',function(e){
  mouse.x=(e.clientX/window.innerWidth)*2-1;
  mouse.y=-(e.clientY/window.innerHeight)*2+1;
  raycaster.setFromCamera(mouse,camera);
  const hits=raycaster.intersectObjects(iMeshes,true);
  if(hits.length>0){
    let obj=hits[0].object;
    while(obj&&!obj.userData.zData)obj=obj.parent;
    if(obj&&obj.userData.zData){
      showDetail(obj.userData.zData);
      return;
    }
  }
});

document.addEventListener('keydown',function(e){if(e.key==='Escape')closeDetail();});

window.addEventListener('resize',function(){
  camera.aspect=window.innerWidth/window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth,window.innerHeight);
});

(function animate(){requestAnimationFrame(animate);controls.update();renderer.render(scene,camera);})();
</script>
</body>
</html>'''

with open(r'f:\自开发程序\工厂建模\3d-viewer.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('3d-viewer.html generated OK (' + str(len(html)) + ' bytes)')
