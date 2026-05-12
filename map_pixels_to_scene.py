import json

FRAME_W, FRAME_H = 1920, 986
DIAGRAM_X_MIN, DIAGRAM_X_MAX = 131, 1789
DIAGRAM_Y_MIN, DIAGRAM_Y_MAX = 0, 933
DIAGRAM_W = DIAGRAM_X_MAX - DIAGRAM_X_MIN
DIAGRAM_H = DIAGRAM_Y_MAX - DIAGRAM_Y_MIN

SCENE_W = 80
SCENE_D = 50

def px_to_scene(px, py):
    sx = (px - DIAGRAM_X_MIN) / DIAGRAM_W * SCENE_W - SCENE_W / 2
    sz = (py - DIAGRAM_Y_MIN) / DIAGRAM_H * SCENE_D - SCENE_D / 2
    return round(sx, 2), round(sz, 2)

def pw_to_scene(pw):
    return round(pw / DIAGRAM_W * SCENE_W, 2)

def ph_to_scene(ph):
    return round(ph / DIAGRAM_H * SCENE_D, 2)

factory_zones = [
    {"name": "上体检修区3", "sub": "库8 库7", "px": 523, "py": 183, "pw": 130, "ph": 80, "color": 0x4a7c59},
    {"name": "上体检修区3", "sub": "库8 库7", "px": 523, "py": 263, "pw": 130, "ph": 55, "color": 0x4a7c59},
    {"name": "上体检修区2", "sub": "库6 库5 库4", "px": 523, "py": 318, "pw": 130, "ph": 66, "color": 0x4a7c59},
    {"name": "上体检修区2", "sub": "库6 库5 库4", "px": 523, "py": 384, "pw": 130, "ph": 60, "color": 0x4a7c59},
    {"name": "上体检修区1", "sub": "库3 库2 库1", "px": 523, "py": 444, "pw": 130, "ph": 50, "color": 0x4a7c59},
    {"name": "上体检修区1", "sub": "库3 库2 库1", "px": 523, "py": 494, "pw": 130, "ph": 30, "color": 0x4a7c59},
    {"name": "起车区", "sub": "32 31 30", "px": 523, "py": 524, "pw": 130, "ph": 48, "color": 0x5c4033},
    
    {"name": "装备保障区", "sub": "", "px": 1045, "py": 264, "pw": 493, "ph": 69, "color": 0x2e7d32},
    {"name": "部件检修区", "sub": "清车 称重", "px": 1053, "py": 338, "pw": 340, "ph": 32, "color": 0xd4553a},
    {"name": "部件检修区", "sub": "", "px": 1053, "py": 370, "pw": 225, "ph": 58, "color": 0xd4553a},
    {"name": "缓车区", "sub": "", "px": 1054, "py": 428, "pw": 469, "ph": 70, "color": 0xe8a030},
    {"name": "轮对区", "sub": "", "px": 1053, "py": 511, "pw": 339, "ph": 75, "color": 0x7b3f8a},
    {"name": "转向架区", "sub": "", "px": 1053, "py": 586, "pw": 340, "ph": 55, "color": 0x3a6fa0},
    
    {"name": "天车", "sub": "", "px": 541, "py": 625, "pw": 853, "ph": 65, "color": 0xe8a030},
]

factory_tracks = [
    {"id": "24", "label": "有电调试道1", "py": 710, "color": 0x4caf50},
    {"id": "25", "label": "有电调试道2", "py": 730, "color": 0x4caf50},
    {"id": "26", "label": "有电调试道3", "py": 750, "color": 0x4caf50},
    {"id": "27", "label": "无电调试道1", "py": 775, "color": 0xe8a030},
    {"id": "28", "label": "无电调试道2", "py": 795, "color": 0xe8a030},
    {"id": "29", "label": "临修道", "py": 820, "color": 0xef5350},
]

bogie_zones = [
    {"name": "落车、称重区", "sub": "", "px": 378, "py": 203, "pw": 490, "ph": 170, "color": 0xe8a030},
    {"name": "部件检修缓存区", "sub": "", "px": 868, "py": 193, "pw": 635, "ph": 187, "color": 0x4a7c59},
    
    {"name": "白莲工序", "sub": "", "px": 370, "py": 404, "pw": 95, "ph": 35, "color": 0x3a6fa0},
    {"name": "冲洗工序", "sub": "", "px": 470, "py": 404, "pw": 95, "ph": 35, "color": 0x3a6fa0},
    {"name": "新造构架工位", "sub": "", "px": 570, "py": 404, "pw": 115, "ph": 35, "color": 0xd4553a},
    {"name": "缓存区1B", "sub": "", "px": 690, "py": 404, "pw": 90, "ph": 30, "color": 0x7b3f8a},
    {"name": "电动设备检测\n与调试区", "sub": "", "px": 785, "py": 404, "pw": 110, "ph": 30, "color": 0x7b3f8a},
    {"name": "存储区1B\n构架部件检测工位", "sub": "", "px": 900, "py": 404, "pw": 120, "ph": 35, "color": 0xd4553a},
    {"name": "轴承间工位", "sub": "", "px": 1250, "py": 400, "pw": 150, "ph": 55, "color": 0xff9800},
    
    {"name": "新造构架存放\n缓存区1", "sub": "", "px": 530, "py": 445, "pw": 115, "ph": 25, "color": 0x7b3f8a},
    
    {"name": "缓存区3", "sub": "", "px": 370, "py": 495, "pw": 90, "ph": 35, "color": 0x7b3f8a},
    {"name": "轮渡工位", "sub": "", "px": 465, "py": 495, "pw": 110, "ph": 35, "color": 0x3a6fa0},
    {"name": "缓存区7", "sub": "", "px": 580, "py": 495, "pw": 90, "ph": 35, "color": 0x7b3f8a},
    {"name": "构架调运\n缓冲存放区", "sub": "", "px": 675, "py": 495, "pw": 145, "ph": 35, "color": 0x3a6fa0},
    {"name": "缓存区1", "sub": "", "px": 825, "py": 495, "pw": 110, "ph": 35, "color": 0x7b3f8a},
    {"name": "检修配合工位", "sub": "", "px": 940, "py": 495, "pw": 110, "ph": 30, "color": 0x3a6fa0},
    {"name": "检修配合工位", "sub": "", "px": 1200, "py": 495, "pw": 90, "ph": 35, "color": 0x3a6fa0},
    
    {"name": "前期架轮轴\n压装前缓冲区", "sub": "", "px": 480, "py": 535, "pw": 150, "ph": 25, "color": 0x7b3f8a},
    
    {"name": "构架部件", "sub": "", "px": 370, "py": 584, "pw": 95, "ph": 30, "color": 0x3a6fa0},
    {"name": "构架部件", "sub": "", "px": 470, "py": 584, "pw": 95, "ph": 30, "color": 0x3a6fa0},
    {"name": "校对", "sub": "", "px": 570, "py": 584, "pw": 75, "ph": 30, "color": 0x3a6fa0},
    {"name": "清洗工艺", "sub": "", "px": 650, "py": 584, "pw": 95, "ph": 30, "color": 0x3a6fa0},
    {"name": "打磨工位", "sub": "", "px": 750, "py": 584, "pw": 95, "ph": 30, "color": 0x3a6fa0},
    {"name": "构架部件\n分解工位", "sub": "", "px": 850, "py": 584, "pw": 75, "ph": 30, "color": 0x3a6fa0},
    {"name": "构架部件\n检测工位", "sub": "", "px": 930, "py": 584, "pw": 95, "ph": 30, "color": 0x3a6fa0},
    {"name": "缓存区", "sub": "", "px": 1030, "py": 584, "pw": 95, "ph": 28, "color": 0x7b3f8a},
    {"name": "轴承检测工位", "sub": "", "px": 1130, "py": 584, "pw": 110, "ph": 30, "color": 0x3a6fa0},
    
    {"name": "线轮总装成套\n存放区", "sub": "", "px": 370, "py": 620, "pw": 150, "ph": 25, "color": 0x7b3f8a},
    {"name": "缓存区12", "sub": "", "px": 530, "py": 620, "pw": 90, "ph": 25, "color": 0x7b3f8a},
    {"name": "构架部件\n暂存工位", "sub": "", "px": 630, "py": 620, "pw": 150, "ph": 25, "color": 0x3a6fa0},
    {"name": "缓存区1", "sub": "", "px": 790, "py": 620, "pw": 90, "ph": 25, "color": 0x7b3f8a},
    {"name": "暂存部件\n存放区", "sub": "", "px": 890, "py": 620, "pw": 110, "ph": 25, "color": 0x7b3f8a},
    
    {"name": "成品转向架\n暂存区", "sub": "", "px": 370, "py": 680, "pw": 190, "ph": 50, "color": 0x4caf50},
    {"name": "构架配装工位", "sub": "", "px": 570, "py": 680, "pw": 130, "ph": 50, "color": 0x3a6fa0},
    {"name": "轮轴清洗/\n装配工位", "sub": "", "px": 710, "py": 680, "pw": 130, "ph": 50, "color": 0x3a6fa0},
    {"name": "缓存区2", "sub": "", "px": 850, "py": 680, "pw": 110, "ph": 45, "color": 0x7b3f8a},
    {"name": "转向架存放", "sub": "", "px": 970, "py": 680, "pw": 95, "ph": 45, "color": 0x3a6fa0},
    {"name": "构架检修工位", "sub": "", "px": 1075, "py": 680, "pw": 130, "ph": 50, "color": 0xd4553a},
]

bogie_cranes = [
    {"px": 365, "py": 584, "pw": 51, "ph": 72, "label": "桥式起重机"},
    {"px": 1186, "py": 591, "pw": 298, "ph": 49, "label": "桥式起重机"},
    {"px": 1248, "py": 417, "pw": 185, "ph": 89, "label": "桥式起重机"},
    {"px": 378, "py": 272, "pw": 490, "ph": 101, "label": "桥式起重机"},
]

factory_scene = {
    "zones": [],
    "tracks": [],
    "cranes": [{"x": -2, "z": 10, "w": 40, "d": 8, "label": "天车"},
               {"x": -2, "z": 0, "w": 40, "d": 7, "label": "天车"}]
}

for z in factory_zones:
    sx, sz = px_to_scene(z["px"], z["py"])
    sw = pw_to_scene(z["pw"])
    sd = ph_to_scene(z["ph"])
    sx += sw / 2
    sz += sd / 2
    factory_scene["zones"].append({
        "x": sx, "z": sz, "w": sw, "d": sd,
        "color": z["color"], "label": z["name"], "sub": z.get("sub", "")
    })

for t in factory_tracks:
    sx, sz = px_to_scene(DIAGRAM_X_MIN, t["py"])
    factory_scene["tracks"].append({
        "z": round(sz, 2), "id": t["id"], "label": t["label"], "color": t["color"]
    })

bogie_scene = {
    "zones": [],
    "cranes": []
}

for z in bogie_zones:
    sx, sz = px_to_scene(z["px"], z["py"])
    sw = pw_to_scene(z["pw"])
    sd = ph_to_scene(z["ph"])
    sx += sw / 2
    sz += sd / 2
    bogie_scene["zones"].append({
        "x": sx, "z": sz, "w": sw, "d": sd,
        "color": z["color"], "label": z["name"], "sub": z.get("sub", "")
    })

for c in bogie_cranes:
    sx, sz = px_to_scene(c["px"], c["py"])
    sw = pw_to_scene(c["pw"])
    sd = ph_to_scene(c["ph"])
    sx += sw / 2
    sz += sd / 2
    bogie_scene["cranes"].append({
        "x": sx, "z": round(sz, 2), "w": round(sw, 2), "d": round(sd, 2), "label": c["label"]
    })

with open(r'f:\自开发程序\工厂建模\factory_scene_data.json', 'w', encoding='utf-8') as f:
    json.dump(factory_scene, f, ensure_ascii=False, indent=2)

with open(r'f:\自开发程序\工厂建模\bogie_scene_data.json', 'w', encoding='utf-8') as f:
    json.dump(bogie_scene, f, ensure_ascii=False, indent=2)

print(f"Factory: {len(factory_scene['zones'])} zones, {len(factory_scene['tracks'])} tracks")
print(f"Bogie: {len(bogie_scene['zones'])} zones, {len(bogie_scene['cranes'])} cranes")
print("Scene data saved!")
