"""
基于四张工厂3D渲染图分析，重建精确的检修库3D模型数据。
图片展示了一个大型轨道交通检修库，包含：
- 左下区：停车列检线（8-10条平行轨道+列车）
- 左上区：转向架检修区（蓝色工位+黄色龙门吊）
- 右上区：车辆检修区（蓝色区域+绿色标线）
- 右中区：多个功能分间（绿色分隔线）
- 右下区：设备区+辅助用房
- 全局：白色柱子、黄色桥式起重机、绿色安全通道
"""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))

W = 400
H = 180

def rect(x, y, w, h):
    return {"x": round(x, 1), "y": round(y, 1), "w": round(w, 1), "h": round(h, 1)}

building = {
    "width": W,
    "height": H,
    "wallHeight": 14,
    "centerX": 0,
    "centerY": 0,
    "roofHeight": 16,
}

bx = -W / 2
by = -H / 2

parking_tracks = []
for i in range(9):
    ty = by + 12 + i * 8.5
    parking_tracks.append({
        "id": f"PT{i+1:02d}",
        "name": f"停车线{i+1}",
        "type": "停车列检线",
        "x": bx + 10,
        "y": ty,
        "length": W * 0.48,
    })

parking_trains = []
for i in range(9):
    ty = by + 12 + i * 8.5
    for j in range(3):
        tx = bx + 20 + j * 58
        parking_trains.append({
            "id": f"TR{i*3+j+1:02d}",
            "x": tx,
            "y": ty - 1.8,
            "w": 50,
            "h": 3.2,
            "color": 0x3d3d3d,
        })

bogie_maintenance = [
    {"id": "BM01", "name": "转向架检修工位1", "x": bx + 10, "y": by + H*0.55, "w": 22, "h": 14, "color": 0x1565c0},
    {"id": "BM02", "name": "转向架检修工位2", "x": bx + 36, "y": by + H*0.55, "w": 22, "h": 14, "color": 0x1565c0},
    {"id": "BM03", "name": "转向架检修工位3", "x": bx + 62, "y": by + H*0.55, "w": 22, "h": 14, "color": 0x1565c0},
    {"id": "BM04", "name": "转向架检修工位4", "x": bx + 10, "y": by + H*0.55 + 18, "w": 22, "h": 14, "color": 0x1565c0},
    {"id": "BM05", "name": "转向架检修工位5", "x": bx + 36, "y": by + H*0.55 + 18, "w": 22, "h": 14, "color": 0x1565c0},
    {"id": "BM06", "name": "转向架检修工位6", "x": bx + 62, "y": by + H*0.55 + 18, "w": 22, "h": 14, "color": 0x1565c0},
]

bogie_equip = []
for i in range(6):
    for j in range(2):
        ex = bx + 15 + i * 26
        ey = by + H * 0.55 + 4 + j * 18
        bogie_equip.append({
            "id": f"BE{i*2+j+1:02d}",
            "name": "转向架检修设备",
            "x": ex,
            "y": ey,
            "w": 12,
            "h": 6,
            "color": 0x0d47a1,
        })

gantry_cranes_vertical = [
    {"id": "GC01", "name": "龙门吊1", "x": bx + 45, "y": by + H*0.45, "w": 3, "h": H*0.45, "color": 0xf9a825, "height": 10},
    {"id": "GC02", "name": "龙门吊2", "x": bx + 95, "y": by + H*0.45, "w": 3, "h": H*0.45, "color": 0xf9a825, "height": 10},
]

bridge_cranes = [
    {"id": "BC01", "name": "桥式起重机1", "x": bx + W*0.5, "y": by + H*0.72, "w": W*0.35, "h": 3, "color": 0xfbc02d, "height": 13},
    {"id": "BC02", "name": "桥式起重机2", "x": bx + W*0.5, "y": by + H*0.55, "w": W*0.3, "h": 3, "color": 0xfbc02d, "height": 13},
]

vehicle_maintenance = [
    {"id": "VM01", "name": "车体检修区1", "x": bx + W*0.52, "y": by + H*0.68, "w": W*0.25, "h": H*0.15, "color": 0x0d47a1},
    {"id": "VM02", "name": "车体检修区2", "x": bx + W*0.52, "y": by + H*0.52, "w": W*0.15, "h": H*0.12, "color": 0x1565c0},
    {"id": "VM03", "name": "车体检修区3", "x": bx + W*0.52, "y": by + H*0.38, "w": W*0.2, "h": H*0.1, "color": 0x1976d2},
]

vehicle_equip = [
    {"id": "VE01", "name": "车体工作台1", "x": bx + W*0.55, "y": by + H*0.7, "w": 10, "h": 6, "color": 0x42a5f5},
    {"id": "VE02", "name": "车体工作台2", "x": bx + W*0.62, "y": by + H*0.7, "w": 10, "h": 6, "color": 0x42a5f5},
    {"id": "VE03", "name": "车体设备1", "x": bx + W*0.55, "y": by + H*0.54, "w": 8, "h": 5, "color": 0x42a5f5},
    {"id": "VE04", "name": "车体设备2", "x": bx + W*0.62, "y": by + H*0.54, "w": 8, "h": 5, "color": 0x42a5f5},
]

workshops = [
    {"id": "WS01", "name": "电气检修间", "x": bx + W*0.72, "y": by + H*0.68, "w": W*0.12, "h": H*0.15, "color": 0x78909c},
    {"id": "WS02", "name": "制动检修间", "x": bx + W*0.72, "y": by + H*0.52, "w": W*0.12, "h": H*0.12, "color": 0x78909c},
    {"id": "WS03", "name": "空调检修间", "x": bx + W*0.72, "y": by + H*0.38, "w": W*0.12, "h": H*0.1, "color": 0x78909c},
    {"id": "WS04", "name": "门系统检修间", "x": bx + W*0.86, "y": by + H*0.68, "w": W*0.12, "h": H*0.15, "color": 0x78909c},
    {"id": "WS05", "name": "受电弓检修间", "x": bx + W*0.86, "y": by + H*0.52, "w": W*0.12, "h": H*0.12, "color": 0x78909c},
    {"id": "WS06", "name": "转向架存放间", "x": bx + W*0.86, "y": by + H*0.38, "w": W*0.12, "h": H*0.1, "color": 0x78909c},
    {"id": "WS07", "name": "配件仓库", "x": bx + W*0.72, "y": by + H*0.22, "w": W*0.26, "h": H*0.12, "color": 0x90a4ae},
    {"id": "WS08", "name": "材料库", "x": bx + W*0.72, "y": by + H*0.08, "w": W*0.26, "h": H*0.1, "color": 0x90a4ae},
]

workshop_equip = [
    {"id": "WE01", "name": "电气试验台", "x": bx + W*0.76, "y": by + H*0.72, "w": 8, "h": 5, "color": 0x546e7a},
    {"id": "WE02", "name": "制动试验台", "x": bx + W*0.76, "y": by + H*0.55, "w": 8, "h": 5, "color": 0x546e7a},
    {"id": "WE03", "name": "空调试验台", "x": bx + W*0.76, "y": by + H*0.41, "w": 8, "h": 5, "color": 0x546e7a},
    {"id": "WE04", "name": "门机试验台", "x": bx + W*0.9, "y": by + H*0.72, "w": 8, "h": 5, "color": 0x546e7a},
    {"id": "WE05", "name": "弓网试验台", "x": bx + W*0.9, "y": by + H*0.55, "w": 8, "h": 5, "color": 0x546e7a},
]

platforms_yellow = []
for i in range(4):
    for j in range(2):
        platforms_yellow.append({
            "id": f"PY{i*2+j+1:02d}",
            "name": "检修平台",
            "x": bx + 12 + i * 25,
            "y": by + 8 + j * 85,
            "w": 10,
            "h": 6,
            "color": 0xfbc02d,
        })

lift_points = []
for i in range(3):
    for j in range(2):
        lift_points.append({
            "id": f"LP{i*2+j+1:02d}",
            "name": "架车点",
            "x": bx + 30 + i * 30,
            "y": by + H*0.5 + j * 20,
            "radius": 2.5,
            "color": 0xf9a825,
        })

green_safety_lines = [
    {"id": "GL01", "name": "主通道", "x": bx + 10, "y": by + H*0.43, "w": W*0.48, "h": 1.5, "color": 0x00c853},
    {"id": "GL02", "name": "纵向通道1", "x": bx + 10, "y": by + H*0.3, "w": 1.5, "h": H*0.6, "color": 0x00c853},
    {"id": "GL03", "name": "纵向通道2", "x": bx + W*0.5, "y": by + H*0.15, "w": 1.5, "h": H*0.75, "color": 0x00c853},
    {"id": "GL04", "name": "横向通道1", "x": bx + W*0.5, "y": by + H*0.65, "w": W*0.5, "h": 1.5, "color": 0x00c853},
    {"id": "GL05", "name": "横向通道2", "x": bx + W*0.5, "y": by + H*0.5, "w": W*0.48, "h": 1.5, "color": 0x00c853},
    {"id": "GL06", "name": "横向通道3", "x": bx + W*0.5, "y": by + H*0.35, "w": W*0.48, "h": 1.5, "color": 0x00c853},
    {"id": "GL07", "name": "右侧纵向", "x": bx + W*0.7, "y": by + H*0.15, "w": 1.5, "h": H*0.75, "color": 0x00c853},
    {"id": "GL08", "name": "停车场通道", "x": bx + 10, "y": by + H*0.2, "w": W*0.48, "h": 1.5, "color": 0x00c853},
]

green_zone_borders = [
    {"id": "GZ01", "name": "停车区边界", "points": [
        [bx+8, by+8], [bx+W*0.5, by+8], [bx+W*0.5, by+H*0.42], [bx+8, by+H*0.42]
    ], "color": 0x00c853},
    {"id": "GZ02", "name": "检修区边界", "points": [
        [bx+8, by+H*0.44], [bx+W*0.5, by+H*0.44], [bx+W*0.5, by+H-8], [bx+8, by+H-8]
    ], "color": 0x00c853},
    {"id": "GZ03", "name": "右侧区边界", "points": [
        [bx+W*0.5+2, by+H*0.15], [bx+W-8, by+H*0.15], [bx+W-8, by+H-8], [bx+W*0.5+2, by+H-8]
    ], "color": 0x00c853},
]

columns = []
col_spacing_x = 20
col_spacing_y = 20
for cx_i in range(int(W / col_spacing_x) + 1):
    for cy_i in range(int(H / col_spacing_y) + 1):
        px = bx + cx_i * col_spacing_x
        py = by + cy_i * col_spacing_y
        columns.append({
            "x": round(px, 1),
            "y": round(py, 1),
            "size": 1.2,
        })

parking_vehicles = []
for i in range(9):
    ty = by + 12 + i * 8.5
    parking_vehicles.append({
        "id": f"PV{i+1:02d}",
        "name": f"列车{i+1}",
        "x": bx + 25,
        "y": ty,
        "w": 120,
        "h": 3.5,
        "color": 0x455a64,
    })

wheel_set_stands = []
for i in range(6):
    for j in range(2):
        wheel_set_stands.append({
            "id": f"WS{i*2+j+1:02d}",
            "name": "轮对存放架",
            "x": bx + 15 + i * 14,
            "y": by + H*0.45 + j * 12,
            "w": 8,
            "h": 4,
            "color": 0xf9a825,
        })

labels = []

for t in parking_tracks:
    labels.append({
        "text": t["name"],
        "x": t["x"] + 2,
        "y": t["y"],
        "size": "small",
        "color": "#b0bec5",
    })

zone_labels = [
    {"text": "停车列检区", "x": bx + W*0.25, "y": by + H*0.22, "size": "large"},
    {"text": "转向架检修区", "x": bx + W*0.25, "y": by + H*0.68, "size": "large"},
    {"text": "车体检修区", "x": bx + W*0.6, "y": by + H*0.68, "size": "medium"},
    {"text": "部件检修间", "x": bx + W*0.84, "y": by + H*0.62, "size": "medium"},
    {"text": "配件仓库", "x": bx + W*0.84, "y": by + H*0.28, "size": "small"},
    {"text": "材料库", "x": bx + W*0.84, "y": by + H*0.13, "size": "small"},
]
labels.extend(zone_labels)

for g in gantry_cranes_vertical:
    labels.append({"text": g["name"], "x": g["x"], "y": g["y"] + g["h"]/2, "size": "small", "color": "#f9a825"})

for b in bridge_cranes:
    labels.append({"text": b["name"], "x": b["x"], "y": b["y"], "size": "small", "color": "#fbc02d"})

result = {
    "building": building,
    "parkingTracks": parking_tracks,
    "parkingVehicles": parking_vehicles,
    "parkingTrains": parking_trains,
    "bogieMaintenance": bogie_maintenance,
    "bogieEquipment": bogie_equip,
    "gantryCranes": gantry_cranes_vertical,
    "bridgeCranes": bridge_cranes,
    "vehicleMaintenance": vehicle_maintenance,
    "vehicleEquipment": vehicle_equip,
    "workshops": workshops,
    "workshopEquipment": workshop_equip,
    "platforms": platforms_yellow,
    "liftPoints": lift_points,
    "wheelSetStands": wheel_set_stands,
    "greenLines": green_safety_lines,
    "greenZoneBorders": green_zone_borders,
    "columns": columns,
    "labels": labels,
}

output = os.path.join(BASE, "factory_model_v2.json")
with open(output, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"建筑尺寸: {W} x {H}")
print(f"停车线: {len(parking_tracks)} 条")
print(f"列车: {len(parking_vehicles)} 辆")
print(f"转向架检修工位: {len(bogie_maintenance)} 个")
print(f"龙门吊: {len(gantry_cranes_vertical)} 台")
print(f"桥式起重机: {len(bridge_cranes)} 台")
print(f"车体检修区: {len(vehicle_maintenance)} 个")
print(f"部件检修间: {len(workshops)} 个")
print(f"检修平台: {len(platforms_yellow)} 个")
print(f"架车点: {len(lift_points)} 个")
print(f"轮对存放架: {len(wheel_set_stands)} 个")
print(f"绿色标线: {len(green_safety_lines)} 条")
print(f"柱子: {len(columns)} 根")
print(f"标签: {len(labels)} 个")
print(f"数据已保存: {output}")
