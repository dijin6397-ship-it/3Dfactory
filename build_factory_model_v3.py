import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUTPUT = os.path.join(BASE, "factory_model_v3.json")

PIXEL_SCALE = 0.22
IMG_W = 1920
IMG_H = 986

def px2m(px):
    return round(px * PIXEL_SCALE, 2)

def px2scene(px, py):
    x = px2m(px - IMG_W / 2)
    y = px2m(IMG_H - py - IMG_H / 2)
    return x, y

model = {
    "building": {
        "width": px2m(IMG_W * 0.85),
        "height": px2m(IMG_H * 0.85),
        "centerX": 0,
        "centerY": 0,
        "wallHeight": 14
    },
    "tracks": [],
    "bogieWorkstations": [],
    "craneGantry": [],
    "craneBridge": [],
    "vehicleMaintenance": [],
    "workshops": [],
    "equipment": [],
    "platforms": [],
    "liftPoints": [],
    "wheelSetStands": [],
    "safetyLines": [],
    "safetyZoneBorders": [],
    "columns": [],
    "labels": []
}

track_defs = [
    {"name": "1道", "py": 843, "px_start": 340, "px_end": 1579, "type": "停车线"},
    {"name": "2道", "py": 782, "px_start": 475, "px_end": 1558, "type": "停车线"},
    {"name": "3道", "py": 749, "px_start": 525, "px_end": 1414, "type": "停车线"},
    {"name": "4道", "py": 723, "px_start": 525, "px_end": 1414, "type": "停车线"},
    {"name": "5道", "px_start": 525, "px_end": 1414, "py": 689, "type": "停车线"},
    {"name": "6道", "px_start": 475, "px_end": 1403, "py": 654, "type": "停车线"},
    {"name": "7道", "px_start": 475, "px_end": 1559, "py": 602, "type": "停车线"},
    {"name": "8道", "px_start": 523, "px_end": 1522, "py": 191, "type": "检修线"},
    {"name": "9道", "px_start": 336, "px_end": 1583, "py": 147, "type": "检修线"},
]

for td in track_defs:
    x1, y1 = px2scene(td["px_start"], td["py"])
    x2, y2 = px2scene(td["px_end"], td["py"])
    length = abs(x2 - x1)
    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2
    model["tracks"].append({
        "name": td["name"],
        "x": cx,
        "y": cy,
        "length": round(length, 2),
        "type": td["type"],
        "color": "#2196f3" if td["type"] == "停车线" else "#ff9800",
        "gauge": 1.435
    })

bogie_ws_defs = [
    {"name": "1号位", "px": 564, "py": 199},
    {"name": "2号位", "px": 564, "py": 227},
    {"name": "3号位", "px": 564, "py": 276},
    {"name": "4号位", "px": 564, "py": 336},
    {"name": "5号位", "px": 564, "py": 383},
    {"name": "6号位", "px": 564, "py": 444},
]

for bw in bogie_ws_defs:
    x, y = px2scene(bw["px"], bw["py"])
    model["bogieWorkstations"].append({
        "name": f"转向架检修{bw['name']}",
        "x": x,
        "y": y,
        "w": px2m(331),
        "h": px2m(28),
        "color": "#1565c0"
    })

model["craneGantry"] = [
    {
        "name": "1号龙门吊",
        "x": px2scene(540, 625)[0],
        "y": px2scene(540, 625)[1],
        "w": px2m(852),
        "h": px2m(65),
        "height": 10,
        "color": "#ffc107",
        "span": px2m(65)
    }
]

model["craneBridge"] = [
    {
        "name": "1号桥式起重机",
        "x": 0,
        "y": px2m(50),
        "w": px2m(1200),
        "h": px2m(6),
        "height": 13,
        "color": "#ff8f00",
        "span": px2m(1200)
    }
]

vm_defs = [
    {"name": "车体检修区A", "px": 700, "py": 530, "w_px": 350, "h_px": 60},
    {"name": "车体检修区B", "px": 1064, "py": 512, "w_px": 459, "h_px": 69},
]
for vm in vm_defs:
    x, y = px2scene(vm["px"], vm["py"])
    model["vehicleMaintenance"].append({
        "name": vm["name"],
        "x": x,
        "y": y,
        "w": px2m(vm["w_px"]),
        "h": px2m(vm["h_px"]),
        "color": "#2e7d32"
    })

workshop_defs = [
    {"name": "电气检修间", "px": 661, "py": 308, "w_px": 114, "h_px": 24},
    {"name": "制动检修间", "px": 781, "py": 308, "w_px": 114, "h_px": 24},
    {"name": "空调检修间", "px": 661, "py": 415, "w_px": 114, "h_px": 24},
    {"name": "门系统检修间", "px": 781, "py": 415, "w_px": 114, "h_px": 24},
    {"name": "受电弓检修间", "px": 1052, "py": 199, "w_px": 284, "h_px": 23},
    {"name": "转向架存放", "px": 1052, "py": 228, "w_px": 285, "h_px": 22},
    {"name": "配件仓库", "px": 1044, "py": 263, "w_px": 494, "h_px": 71},
    {"name": "材料库", "px": 1044, "py": 344, "w_px": 246, "h_px": 42},
]

for ws in workshop_defs:
    x, y = px2scene(ws["px"], ws["py"])
    model["workshops"].append({
        "name": ws["name"],
        "x": x,
        "y": y,
        "w": px2m(ws["w_px"]),
        "h": px2m(ws["h_px"]),
        "color": "#546e7a"
    })

lift_defs = [
    {"name": "1号架车机", "px": 525, "py": 602},
    {"name": "2号架车机", "px": 525, "py": 654},
    {"name": "3号架车机", "px": 525, "py": 723},
]
for lp in lift_defs:
    x, y = px2scene(lp["px"], lp["py"])
    model["liftPoints"].append({
        "name": lp["name"],
        "x": x,
        "y": y,
        "radius": 2.5,
        "color": "#ffc107"
    })

platform_defs = [
    {"name": "1号检修平台", "px": 800, "py": 190, "w_px": 200, "h_px": 15},
    {"name": "2号检修平台", "px": 1100, "py": 190, "w_px": 200, "h_px": 15},
    {"name": "3号检修平台", "px": 800, "py": 620, "w_px": 200, "h_px": 15},
    {"name": "4号检修平台", "px": 1100, "py": 620, "w_px": 200, "h_px": 15},
]
for p in platform_defs:
    x, y = px2scene(p["px"], p["py"])
    model["platforms"].append({
        "name": p["name"],
        "x": x,
        "y": y,
        "w": px2m(p["w_px"]),
        "h": px2m(p["h_px"]),
        "color": "#ffc107"
    })

green_zone_defs = [
    {"name": "停车区安全通道", "px": 541, "py": 694, "w_px": 1008, "h_px": 89},
    {"name": "检修区安全通道", "px": 640, "py": 595, "w_px": 898, "h_px": 96},
]
for gz in green_zone_defs:
    x, y = px2scene(gz["px"], gz["py"])
    model["safetyZoneBorders"].append({
        "name": gz["name"],
        "x": x,
        "y": y,
        "w": px2m(gz["w_px"]),
        "h": px2m(gz["h_px"]),
        "color": "#00c853",
        "points": [
            [x - px2m(gz["w_px"]) / 2, y - px2m(gz["h_px"]) / 2],
            [x + px2m(gz["w_px"]) / 2, y - px2m(gz["h_px"]) / 2],
            [x + px2m(gz["w_px"]) / 2, y + px2m(gz["h_px"]) / 2],
            [x - px2m(gz["w_px"]) / 2, y + px2m(gz["h_px"]) / 2],
        ]
    })

col_spacing = 20
bw = model["building"]["width"]
bh = model["building"]["height"]
for xi in range(int(-bw / 2 / col_spacing), int(bw / 2 / col_spacing) + 1):
    for yi in range(int(-bh / 2 / col_spacing), int(bh / 2 / col_spacing) + 1):
        model["columns"].append({
            "x": xi * col_spacing,
            "y": yi * col_spacing
        })

model["labels"] = [
    {"text": "停车线区域", "x": px2scene(960, 800)[0], "y": px2scene(960, 800)[1], "size": "large", "color": "#ffffff"},
    {"text": "检修线区域", "x": px2scene(960, 170)[0], "y": px2scene(960, 170)[1], "size": "large", "color": "#ffffff"},
    {"text": "转向架检修", "x": px2scene(564, 250)[0], "y": px2scene(564, 250)[1], "size": "medium", "color": "#64b5f6"},
    {"text": "部件检修间", "x": px2scene(720, 360)[0], "y": px2scene(720, 360)[1], "size": "medium", "color": "#90a4ae"},
]

model["trainConfig"] = {
    "defaultCarLength": 22,
    "defaultCarWidth": 3.0,
    "defaultCarHeight": 3.8,
    "carsPerTrain": 6,
    "carGap": 0.4,
    "colors": {
        "body": "#455a64",
        "roof": "#37474f",
        "stripe": "#f44336",
        "window": "#1a237e"
    }
}

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(model, f, ensure_ascii=False, indent=2)

print(f"Model saved: {OUTPUT}")
print(f"Tracks: {len(model['tracks'])}")
print(f"Bogie WS: {len(model['bogieWorkstations'])}")
print(f"Columns: {len(model['columns'])}")
