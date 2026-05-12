"""
基于真实DXF数据，构建结构化的3D工厂布局JSON，
直接输出为JS可在HTML中使用的数据格式。
"""
import json
import os

JSON_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dxf_layout_data.json")

with open(JSON_FILE, "r", encoding="utf-8") as f:
    raw = json.load(f)

texts = raw["texts"]

import re
chinese = [t for t in texts if re.search(r'[\u4e00-\u9fff]', t.get("text", "")) and t.get("text", "").strip()]

all_x = [t["x"] for t in chinese]
all_y = [t["y"] for t in chinese]
cx = (min(all_x) + max(all_x)) / 2
cy = (min(all_y) + max(all_y)) / 2
spread = max(max(all_x) - min(all_x), max(all_y) - min(all_y))

def nx(x):
    return round((x - cx) / spread * 400, 2)

def ny(y):
    return round(-(y - cy) / spread * 400, 2)

def get_text(label):
    for t in chinese:
        txt = t["text"].replace("\n", " ").strip()
        if txt == label:
            return txt, nx(t["x"]), ny(t["y"])
    return None, 0, 0

building_x_range = (nx(min(all_x)) + 2, nx(max(all_x)) - 8)
building_y_range = (ny(max(all_y)) + 2, ny(min(all_y)) - 2)
bx0, bx1 = building_x_range
by0, by1 = building_y_range
bw = round(bx1 - bx0, 2)
bh = round(by1 - by0, 2)
bcx = round((bx0 + bx1) / 2, 2)
bcy = round((by0 + by1) / 2, 2)

tracks_raw = []
track_labels = [
    "22道（静调线）", "23道（定修线）", "24道（定修线）",
    "25道（定修线）", "26道（定修线）", "27道（临修线）",
    "28道（大架修线）", "29道（大架修线）", "30道（大架修线）",
    "库线1（大架修线）", "库线2（大架修线）", "库线3（大架修线）",
    "库线4（大架修线）", "库线5（大架修线）", "库线6（大架修线）",
    "库线7", "库线8"
]

track_start_x = bx0 + 5
track_end_x = bx1 - 15
track_length = round(track_end_x - track_start_x, 2)
n_tracks = len(track_labels)
track_margin = 8
track_span = bh - track_margin * 2
track_spacing = round(track_span / (n_tracks - 1), 2) if n_tracks > 1 else 3

for i, label in enumerate(track_labels):
    ty = round(by0 + track_margin + i * track_spacing, 2)
    short_name = label.split("（")[0] if "（" in label else label
    track_type = ""
    if "大架修" in label:
        track_type = "大架修线"
    elif "临修" in label:
        track_type = "临修线"
    elif "定修" in label:
        track_type = "定修线"
    elif "静调" in label:
        track_type = "静调线"
    else:
        track_type = "辅助线"

    tracks_raw.append({
        "id": f"T{i+1:02d}",
        "name": short_name,
        "type": track_type,
        "x": track_start_x,
        "y": ty,
        "length": track_length,
    })

zone_coords = {}
zone_labels_raw = [
    "编组、静态调试区", "解编、拆解区", "解编、拆解、起车区",
    "上体拆解区", "组装恢复区", "延寿改造区",
    "车体涂装区", "落车调整、称重区",
    "转向架检修区", "物流通道",
    "物料存放区", "下车物料缓存区",
    "部件检修缓存区", "检修物料鉴定、清洁、维修区",
    "待分解转向架存放区", "构架检修缓存区",
    "转向架落成区", "尺寸测量区",
    "轮对轴承轴箱组装区", "成品转向架交检交验及存放区",
    "委外检修零部件存放及包装待发运区",
    "待组装零部件存放区", "轮对退卸零部件存放区",
    "轮对压装零部件存放区",
    "构架检修及焊补探伤区", "构架脱漆后检修及探伤",
    "构架喷漆后交检交验及缓存区", "构架组成翻转场地",
    "构架与轮对落成装置", "转向架加压分解轴箱节点",
    "轴箱、轮对清洗", "轴箱、轮对脱漆",
    "打摩室", "轴承间", "轮对同温存放",
    "打摩室", "废水处理系统（地下）",
    "拖车车轴检修区", "制动管检修区",
    "轮对跑合试验台（申北搬迁25KW）",
    "轮对磁探机（原有不能使用设备拆除）",
    "轮对超探机", "轮对退卸机",
    "车轮车床（申北修复）",
    "构架与轮对落成装置（长客搬迁1.5KW）",
    "立式压力机(申北搬迁)",
    "便携式 称重设备", "单车称重台位（新增）",
    "蠕变、缓冲台位",
    "带装车物料存放区",
]

zone_color_map = {
    "编组": 0x3498db,
    "解编": 0xe67e22,
    "拆解": 0xe74c3c,
    "上体": 0xc0392b,
    "组装": 0x27ae60,
    "延寿": 0x8e44ad,
    "涂装": 0xf1c40f,
    "落车": 0x1abc9c,
    "转向架": 0x2980b9,
    "物流": 0x7f8c8d,
    "物料": 0x16a085,
    "缓存": 0x95a5a6,
    "部件": 0x2c3e50,
    "检修": 0xd35400,
    "待分解": 0x9b59b6,
    "构架": 0xe74c3c,
    "喷漆": 0xf39c12,
    "翻转": 0x16a085,
    "落成": 0x2ecc71,
    "轴箱": 0x3498db,
    "清洗": 0x00bcd4,
    "脱漆": 0xff9800,
    "打摩": 0x795548,
    "轴承": 0x607d8b,
    "同温": 0x607d8b,
    "探伤": 0x9c27b0,
    "制动": 0x673ab7,
    "试验": 0x3f51b5,
    "退卸": 0x795548,
    "测量": 0x009688,
    "存放": 0x4caf50,
    "称重": 0x009688,
    "蠕变": 0x8bc34a,
    "带装": 0x8bc34a,
}

zones = []
zone_id = 1
used_zone_names = set()

for t in chinese:
    txt = t["text"].replace("\n", " ").strip()
    if not txt or len(txt) < 4 or len(txt) > 40:
        continue

    skip = False
    for kw in ["设计", "审核", "会签", "批准", "审批", "比例", "图幅",
               "绘图软件", "版本", "阶段", "页次", "方案", "主管",
               "标准审查", "插座箱", "电气柜", "代表", "核实",
               "新增电气柜", "新增插座", "信息接入", "风管接入",
               "电源接入", "设备轮廓线", "施工", "基线", "建筑物",
               "申通", "中车", "北翟路", "检修库工艺布局图", "方案二",
               "相对位置", "路线规划", "图例", "双扇门", "单扇门",
               "起重设备", "物料存放区（", "库房面积", "1.5%",
               "t=5", "上水点", "排水管", "北",
               "该辅间", "该地面", "轮对跑合试验台搬出",
               "转向架分解", "构架组成吊运", "清洗后的构架",
               "构架检修合格", "分解后的构架", "轴箱节点压装",
               "牵引梁、牵引拉杆、轴箱", "清洗后"]:
        if kw in txt:
            skip = True
            break
    if skip:
        continue

    if txt in used_zone_names:
        continue

    x = nx(t["x"])
    y = ny(t["y"])

    if not (bx0 - 5 <= x <= bx1 + 10 and by0 - 5 <= y <= by1 + 5):
        continue

    color = 0x546e7a
    for keyword, c in zone_color_map.items():
        if keyword in txt:
            color = c
            break

    w = 15
    h = 8
    if "通道" in txt:
        w, h, color = 6, 3, 0x455a64
    elif "休息室" in txt:
        w, h, color = 4, 3, 0x8d6e63
    elif "卫生间" in txt or "卫" in txt:
        w, h, color = 3, 2, 0x795548
    elif "库房" in txt and "存储" in txt:
        w, h = 25, 12
    elif "办公" in txt:
        w, h, color = 8, 5, 0x5d4037
    elif "起重机" in txt:
        w, h, color = 0, 0, 0
    elif "台位" in txt:
        w, h, color = 5, 3, 0x4db6ac
    elif "间" in txt:
        w, h = 6, 4

    zones.append({
        "id": f"Z{zone_id:03d}",
        "name": txt.split("（")[0] if "（" in txt else txt.split(" ")[0] if " " in txt else txt[:12],
        "fullName": txt[:30],
        "x": x - w/2,
        "y": y - h/2,
        "w": w,
        "h": h,
        "color": color,
    })
    used_zone_names.add(txt)
    zone_id += 1

equipment_labels = [
    ("地坑式架车", 0xff5722, 4, 3),
    ("电动单梁起重机", 0xff9800, 0, 0),
    ("电动单梁悬挂起重机", 0xff9800, 0, 0),
    ("轮对压装机", 0xf44336, 5, 4),
    ("轮对退卸机", 0xf44336, 5, 4),
    ("轮对磁探机", 0x9c27b0, 5, 4),
    ("轮对超探机", 0x9c27b0, 5, 4),
    ("轮对跑合试验台", 0x673ab7, 6, 4),
    ("车轮车床", 0x3f51b5, 5, 4),
    ("立式压力机", 0xff5722, 4, 4),
    ("1t行架车", 0xff9800, 3, 2),
    ("升降台", 0x00897b, 3, 2),
    ("空压机", 0xd32f2f, 5, 5),
    ("划线测量机", 0x009688, 4, 3),
    ("构架组装升降装置", 0xff5722, 5, 4),
    ("构架与轮对落成装置", 0xff5722, 6, 5),
    ("转向架静压试验", 0x673ab7, 6, 4),
    ("废水处理系统", 0x455a64, 6, 6),
    ("智能紧固系统", 0x00897b, 3, 3),
    ("轮对转盘", 0x795548, 4, 4),
]

equip_items = []
eq_id = 1
for eq_label, eq_color, ew, eh in equipment_labels:
    count = 0
    for t in chinese:
        txt = t["text"].replace("\n", " ").strip()
        if eq_label in txt and count < 4:
            x = nx(t["x"])
            y = ny(t["y"])
            if bx0 - 5 <= x <= bx1 + 5 and by0 - 5 <= y <= by1 + 5:
                equip_items.append({
                    "id": f"E{eq_id:03d}",
                    "name": eq_label,
                    "x": x,
                    "y": y,
                    "w": ew,
                    "h": eh,
                    "color": eq_color,
                })
                eq_id += 1
                count += 1

workstations = []
ws_id = 1
ws_patterns = [
    ("组装台位", 0x4caf50, 3, 2),
    ("延寿改造台位", 0x8bc34a, 4, 2),
    ("蠕变、缓冲台位", 0xcddc39, 4, 2),
    ("落车台位", 0x26a69a, 5, 3),
    ("升降台", 0x009688, 2, 2),
    ("双层作业平台", 0xff9800, 4, 3),
    ("小件脱漆托盘", 0xff5722, 2, 2),
    ("小件清洗托盘", 0x00bcd4, 2, 2),
    ("小件清洗槽", 0x00acc1, 3, 2),
    ("移动支架装置", 0x607d8b, 3, 2),
]

for ws_label, ws_color, ww, wh in ws_patterns:
    count = 0
    for t in chinese:
        txt = t["text"].replace("\n", " ").strip()
        if txt.startswith(ws_label) and count < 8:
            x = nx(t["x"])
            y = ny(t["y"])
            if bx0 - 5 <= x <= bx1 + 5 and by0 - 5 <= y <= by1 + 5:
                workstations.append({
                    "id": f"W{ws_id:03d}",
                    "name": ws_label[:8],
                    "x": x,
                    "y": y,
                    "w": ww,
                    "h": wh,
                    "color": ws_color,
                })
                ws_id += 1
                count += 1

labels = []
for z in zones:
    labels.append({
        "text": z["name"],
        "x": z["x"] + z["w"] / 2,
        "y": z["y"] + z["h"] / 2,
        "size": "medium",
    })

for t in tracks_raw:
    labels.append({
        "text": t["name"],
        "x": t["x"] + 2,
        "y": t["y"],
        "size": "small",
    })

result = {
    "building": {
        "width": round(bw, 2),
        "height": round(bh, 2),
        "wallHeight": 10,
        "centerX": bcx,
        "centerY": bcy,
    },
    "tracks": tracks_raw,
    "zones": zones,
    "equipment": equip_items,
    "workstations": workstations,
    "labels": labels,
}

output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "factory_3d_data.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"Building: {bw:.1f} x {bh:.1f}")
print(f"Tracks: {len(tracks_raw)}")
print(f"Zones: {len(zones)}")
print(f"Equipment: {len(equip_items)}")
print(f"Workstations: {len(workstations)}")
print(f"Labels: {len(labels)}")
print(f"Data saved: {output_path}")
