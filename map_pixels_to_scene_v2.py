import json

SCENE_W = 80
SCENE_D = 50

# ==================== LEFT SIDE: TRACKS ====================
# Left side tracks - names on the leftmost
# 24-29: complete 8-car trains, only train number
# 30/31/32/库1-8: separated cars, car-segment number (e.g. 2018-1), max 3 cars

left_tracks = []

# 库1-库8 (separated, 3 cars each) - top section
ku_labels = ["库8道", "库7道", "库6道", "库5道", "库4道", "库3道", "库2道", "库1道"]
ku_colors = [0x5c4033, 0x5c4033, 0x5c4033, 0x5c4033, 0x5c4033, 0x5c4033, 0x5c4033, 0x5c4033]
for i, (lab, col) in enumerate(zip(ku_labels, ku_colors)):
    left_tracks.append({
        "id": lab.replace("道", ""),
        "label": "",
        "type": "separated",
        "maxCars": 3,
        "z": round(-15 + i * 1.5, 2),
        "color": col
    })

# 30/31/32 (separated, 3 cars each)
for i, (tid, col) in enumerate([("32", 0x5c4033), ("31", 0x5c4033), ("30", 0x5c4033)]):
    left_tracks.append({
        "id": tid,
        "label": "",
        "type": "separated",
        "maxCars": 3,
        "z": round(-2.5 + i * 1.5, 2),
        "color": col
    })

# 24-29 (complete 8-car trains)
complete_tracks = [
    ("29", "临修道", 0xef5350),
    ("28", "无电调试道2", 0xe8a030),
    ("27", "无电调试道1", 0xe8a030),
    ("26", "有电调试道3", 0x4caf50),
    ("25", "有电调试道2", 0x4caf50),
    ("24", "有电调试道1", 0x4caf50),
]
for i, (tid, lab, col) in enumerate(complete_tracks):
    left_tracks.append({
        "id": tid,
        "label": lab,
        "type": "complete",
        "maxCars": 8,
        "z": round(3.0 + i * 1.5, 2),
        "color": col
    })

# ==================== MIDDLE: TRANSFER TABLE ====================
transfer_table = {
    "x": -3.0,
    "z": -15.0,
    "width": 4.0,
    "depth": round(3.0 + 8 * 1.5 + 1.5 - (-15.0), 2),  # from top track to bottom track
    "label": "移车台"
}

# ==================== RIGHT SIDE: ZONES (1:1 from screenshot) ====================
# Keep exact pixel-to-scene mapping from the screenshot for right side zones
FRAME_W, FRAME_H = 1920, 986
DIAGRAM_LEFT = 131
DIAGRAM_RIGHT = 1789
DIAGRAM_TOP = 0
DIAGRAM_BOTTOM = 933
DIAGRAM_W = DIAGRAM_RIGHT - DIAGRAM_LEFT
DIAGRAM_H = DIAGRAM_BOTTOM - DIAGRAM_TOP

def px2sx(px):
    return round((px - DIAGRAM_LEFT) / DIAGRAM_W * SCENE_W - SCENE_W / 2, 2)

def py2sz(py):
    return round((py - DIAGRAM_TOP) / DIAGRAM_H * SCENE_D - SCENE_D / 2, 2)

def pw2sw(pw):
    return round(pw / DIAGRAM_W * SCENE_W, 2)

def ph2sd(ph):
    return round(ph / DIAGRAM_H * SCENE_D, 2)

right_zones_raw = [
    {"label": "装备保障区", "sub": "", "px": 1045, "py": 199, "pw": 504, "ph": 80, "color": 0x2e7d32},
    {"label": "部件检修区", "sub": "清车 称重", "px": 1044, "py": 279, "pw": 504, "ph": 65, "color": 0xd4553a},
    {"label": "缓车区", "sub": "", "px": 1054, "py": 428, "pw": 469, "ph": 70, "color": 0xe8a030},
    {"label": "轮对区", "sub": "", "px": 1053, "py": 511, "pw": 476, "ph": 75, "color": 0x7b3f8a},
    {"label": "转向架区", "sub": "", "px": 1053, "py": 586, "pw": 340, "ph": 55, "color": 0x3a6fa0},
]

right_zones = []
for z in right_zones_raw:
    cx = px2sx(z["px"] + z["pw"] / 2)
    cz = py2sz(z["py"] + z["ph"] / 2)
    sw = pw2sw(z["pw"])
    sd = ph2sd(z["ph"])
    right_zones.append({
        "x": cx, "z": cz, "w": sw, "d": sd,
        "color": z["color"],
        "label": z["label"],
        "sub": z.get("sub", "")
    })

# ==================== BUILD SCENE DATA ====================
factory_scene = {
    "zones": right_zones,
    "tracks": left_tracks,
    "transferTable": transfer_table,
    "cranes": []
}

# Bogie scene - keep as-is
bogie_zones_raw = [
    {"label": "落车、称重区", "sub": "", "px": 378, "py": 203, "pw": 490, "ph": 170, "color": 0xe8a030},
    {"label": "部件检修缓存区", "sub": "", "px": 868, "py": 193, "pw": 635, "ph": 187, "color": 0x4a7c59},
    {"label": "白莲工序", "sub": "", "px": 370, "py": 404, "pw": 95, "ph": 35, "color": 0x3a6fa0},
    {"label": "冲洗工序", "sub": "", "px": 470, "py": 404, "pw": 95, "ph": 35, "color": 0x3a6fa0},
    {"label": "新造构架工位", "sub": "", "px": 570, "py": 404, "pw": 115, "ph": 35, "color": 0xd4553a},
    {"label": "缓存区1B", "sub": "", "px": 690, "py": 404, "pw": 90, "ph": 30, "color": 0x7b3f8a},
    {"label": "电动设备检测与调试区", "sub": "", "px": 785, "py": 404, "pw": 110, "ph": 30, "color": 0x7b3f8a},
    {"label": "存储区1B", "sub": "构架部件检测工位", "px": 900, "py": 404, "pw": 120, "ph": 35, "color": 0xd4553a},
    {"label": "轴承间工位", "sub": "", "px": 1250, "py": 400, "pw": 150, "ph": 55, "color": 0xff9800},
    {"label": "新造构架存放缓存区1", "sub": "", "px": 530, "py": 445, "pw": 115, "ph": 25, "color": 0x7b3f8a},
    {"label": "缓存区3", "sub": "", "px": 370, "py": 495, "pw": 90, "ph": 35, "color": 0x7b3f8a},
    {"label": "轮渡工位", "sub": "", "px": 465, "py": 495, "pw": 110, "ph": 35, "color": 0x3a6fa0},
    {"label": "缓存区7", "sub": "", "px": 580, "py": 495, "pw": 90, "ph": 35, "color": 0x7b3f8a},
    {"label": "构架调运缓冲存放区", "sub": "", "px": 675, "py": 495, "pw": 145, "ph": 35, "color": 0x3a6fa0},
    {"label": "缓存区1", "sub": "", "px": 825, "py": 495, "pw": 110, "ph": 35, "color": 0x7b3f8a},
    {"label": "检修配合工位", "sub": "", "px": 940, "py": 495, "pw": 110, "ph": 30, "color": 0x3a6fa0},
    {"label": "检修配合工位", "sub": "", "px": 1200, "py": 495, "pw": 90, "ph": 35, "color": 0x3a6fa0},
    {"label": "前期架轮轴压装前缓冲区", "sub": "", "px": 480, "py": 535, "pw": 150, "ph": 25, "color": 0x7b3f8a},
    {"label": "构架部件", "sub": "", "px": 370, "py": 584, "pw": 95, "ph": 30, "color": 0x3a6fa0},
    {"label": "构架部件", "sub": "", "px": 470, "py": 584, "pw": 95, "ph": 30, "color": 0x3a6fa0},
    {"label": "校对", "sub": "", "px": 570, "py": 584, "pw": 75, "ph": 30, "color": 0x3a6fa0},
    {"label": "清洗工艺", "sub": "", "px": 650, "py": 584, "pw": 95, "ph": 30, "color": 0x3a6fa0},
    {"label": "打磨工位", "sub": "", "px": 750, "py": 584, "pw": 95, "ph": 30, "color": 0x3a6fa0},
    {"label": "构架部件分解工位", "sub": "", "px": 850, "py": 584, "pw": 75, "ph": 30, "color": 0x3a6fa0},
    {"label": "构架部件检测工位", "sub": "", "px": 930, "py": 584, "pw": 95, "ph": 30, "color": 0x3a6fa0},
    {"label": "缓存区", "sub": "", "px": 1030, "py": 584, "pw": 95, "ph": 28, "color": 0x7b3f8a},
    {"label": "轴承检测工位", "sub": "", "px": 1130, "py": 584, "pw": 110, "ph": 30, "color": 0x3a6fa0},
    {"label": "线轮总装成套存放区", "sub": "", "px": 370, "py": 620, "pw": 150, "ph": 25, "color": 0x7b3f8a},
    {"label": "缓存区12", "sub": "", "px": 530, "py": 620, "pw": 90, "ph": 25, "color": 0x7b3f8a},
    {"label": "构架部件暂存工位", "sub": "", "px": 630, "py": 620, "pw": 150, "ph": 25, "color": 0x3a6fa0},
    {"label": "缓存区1", "sub": "", "px": 790, "py": 620, "pw": 90, "ph": 25, "color": 0x7b3f8a},
    {"label": "暂存部件存放区", "sub": "", "px": 890, "py": 620, "pw": 110, "ph": 25, "color": 0x3a6fa0},
    {"label": "成品转向架暂存区", "sub": "", "px": 370, "py": 680, "pw": 190, "ph": 50, "color": 0x4caf50},
    {"label": "构架配装工位", "sub": "", "px": 570, "py": 680, "pw": 130, "ph": 50, "color": 0x3a6fa0},
    {"label": "轮轴清洗/装配工位", "sub": "", "px": 710, "py": 680, "pw": 130, "ph": 50, "color": 0x3a6fa0},
    {"label": "缓存区2", "sub": "", "px": 850, "py": 680, "pw": 110, "ph": 45, "color": 0x7b3f8a},
    {"label": "转向架存放", "sub": "", "px": 970, "py": 680, "pw": 95, "ph": 45, "color": 0x3a6fa0},
    {"label": "构架检修工位", "sub": "", "px": 1075, "py": 680, "pw": 130, "ph": 50, "color": 0xd4553a},
]

bogie_zones = []
for z in bogie_zones_raw:
    cx = px2sx(z["px"] + z["pw"] / 2)
    cz = py2sz(z["py"] + z["ph"] / 2)
    sw = pw2sw(z["pw"])
    sd = ph2sd(z["ph"])
    bogie_zones.append({
        "x": cx, "z": cz, "w": sw, "d": sd,
        "color": z["color"],
        "label": z["label"],
        "sub": z.get("sub", "")
    })

bogie_scene = {
    "zones": bogie_zones,
    "cranes": []
}

with open(r'f:\自开发程序\工厂建模\factory_scene_data.json', 'w', encoding='utf-8') as f:
    json.dump(factory_scene, f, ensure_ascii=False, indent=2)

with open(r'f:\自开发程序\工厂建模\bogie_scene_data.json', 'w', encoding='utf-8') as f:
    json.dump(bogie_scene, f, ensure_ascii=False, indent=2)

print(f"Factory: {len(right_zones)} right zones, {len(left_tracks)} left tracks, transfer table")
print(f"\nLeft tracks (top to bottom):")
for t in left_tracks:
    print(f"  {t['id']} z={t['z']} type={t['type']} max={t['maxCars']}")
print(f"\nTransfer table: x={transfer_table['x']} z={transfer_table['z']} w={transfer_table['width']} d={transfer_table['depth']}")
print(f"\nBogie: {len(bogie_zones)} zones")
print("\nDone!")
