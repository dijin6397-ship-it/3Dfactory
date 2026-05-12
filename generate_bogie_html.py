import json

with open(r'f:\自开发程序\工厂建模\bogie_scene_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

SCALE = 0.5

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

zones_js = json.dumps(scale_zones(data['zones']), ensure_ascii=False)

html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>转向架产线工艺流程</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{overflow:hidden;font-family:"Microsoft YaHei","SimHei",sans-serif;background:#0d1117}
canvas{display:block}
#panel{position:fixed;top:12px;left:12px;background:rgba(13,17,23,0.94);color:#c9d1d9;padding:14px;border-radius:10px;width:240px;z-index:10;max-height:95vh;overflow-y:auto;border:1px solid rgba(48,54,61,0.8);backdrop-filter:blur(8px)}
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
#tooltip{position:fixed;pointer-events:none;background:rgba(13,17,23,0.96);color:#c9d1d9;padding:8px 12px;border-radius:6px;font-size:12px;display:none;z-index:100;border:1px solid rgba(48,54,61,0.6);max-width:280px}
#legend{position:fixed;bottom:12px;right:12px;background:rgba(13,17,23,0.9);color:#8b949e;padding:10px 12px;border-radius:8px;font-size:10px;z-index:10;border:1px solid rgba(48,54,61,0.6)}
.legend-item{display:flex;align-items:center;gap:5px;margin:2px 0}
.legend-color{width:12px;height:8px;border-radius:2px;flex-shrink:0}
.back-link{position:fixed;top:12px;right:12px;z-index:10}
.back-link a{background:rgba(13,17,23,0.9);color:#58a6ff;border:1px solid rgba(48,54,61,0.6);padding:6px 14px;border-radius:6px;text-decoration:none;font-size:12px}
.back-link a:hover{background:rgba(48,54,61,0.6)}
#detailPanel{position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:rgba(13,17,23,0.97);color:#c9d1d9;padding:20px 24px;border-radius:12px;z-index:200;border:1px solid rgba(56,139,253,0.4);min-width:280px;max-width:400px;display:none;box-shadow:0 8px 32px rgba(0,0,0,0.6)}
#detailPanel h4{color:#58a6ff;font-size:15px;margin-bottom:12px;border-bottom:1px solid rgba(48,54,61,0.6);padding-bottom:8px}
#detailPanel .info-row{display:flex;justify-content:space-between;padding:4px 0;font-size:12px;border-bottom:1px solid rgba(48,54,61,0.3)}
#detailPanel .info-row .info-label{color:#8b949e}
#detailPanel .info-row .info-value{color:#e6edf3;font-weight:bold}
#detailPanel .close-btn{position:absolute;top:8px;right:12px;background:none;border:none;color:#8b949e;cursor:pointer;font-size:18px}
#detailPanel .close-btn:hover{color:#f85149}
#overlay{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.3);z-index:199;display:none}
</style>
</head>
<body>
<div class="back-link"><a href="3d-viewer.html">\u2190 返回总体工艺流程</a></div>
<button id="toggleBtn" onclick="togglePanel()">\u2630 面板</button>
<div id="panel">
  <h3>\u2699 转向架产线工艺流程</h3>
  <details class="panel-section" open>
    <summary>\U0001f441 视图控制</summary>
    <button class="btn" onclick="setView('top',this)">俯视图</button>
    <button class="btn" onclick="setView('front',this)">前视图</button>
    <button class="btn active" onclick="setView('perspective',this)">透视图</button>
    <button class="btn" onclick="resetCamera()">重置相机</button>
  </details>
  <details class="panel-section" open>
    <summary>\U0001f4c2 图层控制</summary>
    <button class="btn active" onclick="toggleLayer('building',this)">厂房结构</button>
    <button class="btn active" onclick="toggleLayer('zones',this)">工位区域</button>
    <button class="btn active" onclick="toggleLayer('labels',this)">文字标注</button>
  </details>
  <details class="panel-section">
    <summary>\U0001f4ca 产线信息</summary>
    <div class="label">工位数量: <span style="color:#58a6ff">''' + str(len(data['zones'])) + '''个区域</span></div>
  </details>
  <div style="margin-top:8px;font-size:10px;color:#484f58;text-align:center">点击区域查看详情 | 滚轮缩放 | 右键旋转</div>
</div>
<div id="tooltip"></div>
<div id="overlay" onclick="closeDetail()"></div>
<div id="detailPanel">
  <button class="close-btn" onclick="closeDetail()">\u2715</button>
  <h4 id="detailTitle"></h4>
  <div id="detailContent"></div>
</div>
<div id="legend">
  <div class="legend-item"><div class="legend-color" style="background:#e8a030"></div>落车/称重区</div>
  <div class="legend-item"><div class="legend-color" style="background:#4a7c59"></div>部件检修缓存区</div>
  <div class="legend-item"><div class="legend-color" style="background:#d4553a"></div>检修工位</div>
  <div class="legend-item"><div class="legend-color" style="background:#3a6fa0"></div>加工工位</div>
  <div class="legend-item"><div class="legend-color" style="background:#7b3f8a"></div>缓存区</div>
  <div class="legend-item"><div class="legend-color" style="background:#4caf50"></div>成品暂存区</div>
  <div class="legend-item"><div class="legend-color" style="background:#ff9800"></div>轴承间</div>
</div>
<script type="importmap">{"imports":{"three":"https://unpkg.com/three@0.160.0/build/three.module.js","three/addons/":"https://unpkg.com/three@0.160.0/examples/jsm/"}}</script>
<script type="module">
import*as THREE from'three';
import{OrbitControls}from'three/addons/controls/OrbitControls.js';

const D_zones=''' + zones_js + r''';
const SC=0.5;

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
scene.fog=new THREE.FogExp2(0x0d1117,0.008);

const camera=new THREE.PerspectiveCamera(50,window.innerWidth/window.innerHeight,0.1,200);
camera.position.set(15,30,25);

const controls=new OrbitControls(camera,renderer.domElement);
controls.enableDamping=true;
controls.dampingFactor=0.08;
controls.target.set(0,0,2);
controls.maxPolarAngle=Math.PI*0.48;
controls.minDistance=8;
controls.maxDistance=80;

scene.add(new THREE.AmbientLight(0xffffff,0.6));
const dl=new THREE.DirectionalLight(0xffffff,0.9);
dl.position.set(20,35,15);
dl.castShadow=true;
dl.shadow.mapSize.set(4096,4096);
dl.shadow.camera.left=-35;dl.shadow.camera.right=35;
dl.shadow.camera.top=25;dl.shadow.camera.bottom=-25;
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
  const sp=mkLabel(text,color||'#ffffff',fontSize||10);
  sp.position.copy(pos);
  g.add(sp);
  sp.userData.layer='labels';
  iMeshes.push(sp);
  return sp;
}

const bg=ensureGroup('building');
const SW=45,SD=28;
const ground=new THREE.Mesh(
  new THREE.BoxGeometry(SW,0.3,SD),
  new THREE.MeshStandardMaterial({color:0x151a28,roughness:0.95})
);
ground.position.set(0,-0.15,2);
ground.receiveShadow=true;
bg.add(ground);

const gridHelper=new THREE.GridHelper(SW,45,0x1a2233,0x1a2233);
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
    new THREE.BoxGeometry(z.w,0.1,z.d),
    new THREE.MeshStandardMaterial({color:z.color,roughness:0.55,metalness:0.05,transparent:true,opacity:0.88})
  );
  base.position.set(0,0.05,0);
  base.receiveShadow=true;
  g.add(base);

  const h=Math.max(0.4,Math.min(z.d*0.25,1.5));
  const edge=new THREE.LineSegments(
    new THREE.EdgesGeometry(new THREE.BoxGeometry(z.w,h,z.d)),
    new THREE.LineBasicMaterial({color:z.color,transparent:true,opacity:0.5})
  );
  edge.position.y=h/2;
  g.add(edge);

  const body=new THREE.Mesh(
    new THREE.BoxGeometry(z.w,h-0.1,z.d),
    new THREE.MeshStandardMaterial({color:z.color,roughness:0.6,transparent:true,opacity:0.2})
  );
  body.position.y=h/2+0.05;
  g.add(body);

  g.position.set(z.x,0,z.z);
  const fullLabel=z.label+(z.sub?' '+z.sub:'');
  g.userData={type:'zone',label:fullLabel,zData:z};
  iMeshes.push(base);
  base.userData={type:'zone',label:fullLabel,zData:z};

  const fs=z.label.length>6?6:8;
  addLabel(g,z.label,new THREE.Vector3(0,h+0.35,0),'#ffffff',fs);
  zg.add(g);
});

function showDetail(zData){
  const dp=document.getElementById('detailPanel');
  const dt=document.getElementById('detailTitle');
  const dc=document.getElementById('detailContent');
  const colorHex='#'+zData.color.toString(16).padStart(6,'0');
  dt.innerHTML='<span style="display:inline-block;width:14px;height:14px;border-radius:3px;background:'+colorHex+';vertical-align:middle;margin-right:6px"></span>'+zData.label;
  const realW=Math.round(zData.w/SC);
  const realD=Math.round(zData.d/SC);
  const area=realW*realD;
  let rows=[
    ['工位名称',zData.label],
    ['实际尺寸',realW+'m \u00d7 '+realD+'m'],
    ['占地面积',area+'m\u00b2']
  ];
  if(zData.sub)rows.push(['备注信息',zData.sub]);
  rows.push(['坐标位置','('+Math.round(zData.x/SC)+', '+Math.round(zData.z/SC)+')']);
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
  if(v==='top'){camera.position.set(0,45,2);controls.target.set(0,0,2);}
  else if(v==='front'){camera.position.set(0,10,35);controls.target.set(0,0,2);}
  else{camera.position.set(15,30,25);controls.target.set(0,0,2);}
  controls.update();
};
window.resetCamera=function(){camera.position.set(15,30,25);controls.target.set(0,0,2);controls.update();};
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
      let h='<div style="color:#58a6ff;font-weight:bold;margin-bottom:3px">'+obj.userData.label+'</div>';
      if(zD){h+='<div style="color:#8b949e;font-size:10px">点击查看详情</div>';}
      tooltip.innerHTML=h;
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

with open(r'f:\自开发程序\工厂建模\bogie-viewer.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('bogie-viewer.html generated OK (' + str(len(html)) + ' bytes)')
