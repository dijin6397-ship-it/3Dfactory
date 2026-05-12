"""
从提取的DXF文字数据中，分类整理所有关键区域标注及其坐标位置，
输出归一化后的布局数据供3D HTML使用。
"""
import json
import os
import re

JSON_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dxf_layout_data.json")

with open(JSON_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

texts = data["texts"]

chinese_texts = [t for t in texts if re.search(r'[\u4e00-\u9fff]', t.get("text", "")) and t.get("text", "").strip()]

KEY_ZONES = [
    "编组、静态调试区", "转向架检修区", "落车、称重、调整区",
    "解编、拆解区", "解编、拆解、起车区", "组装恢复区",
    "上体拆解区", "车体涂装区", "延寿改造区", "物料存放区",
    "停车列检区", "联合检修区", "周月检区", "吹扫及清洗区",
    "设备间", "办公区", "检修库工艺布局图"
]

TRACK_KEYWORDS = ["库线", "道（", "移车台"]

EQUIPMENT_KEYWORDS = [
    "架车", "起重机", "轮对", "空压机", "压装", "车床",
    "试验台", "称重", "探伤", "清洗", "脱漆", "打磨",
    "升降台", "充电区", "平台"
]

ROOM_KEYWORDS = [
    "库房", "办公", "休息室", "配电间", "电源间", "测试间",
    "检修间", "检修分间", "仓库", "卫生间", "男卫", "女卫",
    "工具间", "更衣室", "值班室", "机房", "消防"
]

LOGISTICS_KEYWORDS = ["物流通道", "通道", "物流"]

print("=" * 60)
print("上海北翟路车辆段检修库 - 实际CAD布局分析")
print("=" * 60)

print("\n=== 主要功能区域 ===")
for t in chinese_texts:
    text = t["text"].replace("\n", " ")
    for zone in KEY_ZONES:
        if zone in text:
            print(f"  [{zone}] @ ({t['x']:.0f}, {t['y']:.0f}) h={t.get('height', 0):.0f}")
            break

print("\n=== 库线/轨道 ===")
for t in chinese_texts:
    text = t["text"].replace("\n", " ")
    for kw in TRACK_KEYWORDS:
        if kw in text:
            print(f"  [{text}] @ ({t['x']:.0f}, {t['y']:.0f})")
            break

print("\n=== 设备标注 ===")
seen_equip = set()
for t in chinese_texts:
    text = t["text"].replace("\n", " ")
    for kw in EQUIPMENT_KEYWORDS:
        if kw in text and text not in seen_equip:
            seen_equip.add(text)
            print(f"  [{text}] @ ({t['x']:.0f}, {t['y']:.0f})")
            break

print("\n=== 辅助用房 ===")
seen_room = set()
for t in chinese_texts:
    text = t["text"].replace("\n", " ")
    for kw in ROOM_KEYWORDS:
        if kw in text and text not in seen_room:
            seen_room.add(text)
            print(f"  [{text}] @ ({t['x']:.0f}, {t['y']:.0f})")
            break

print("\n=== 物流通道 ===")
seen_log = set()
for t in chinese_texts:
    text = t["text"].replace("\n", " ")
    for kw in LOGISTICS_KEYWORDS:
        if kw in text and text not in seen_log:
            seen_log.add(text)
            print(f"  [{text}] @ ({t['x']:.0f}, {t['y']:.0f})")
            break

all_x = [t["x"] for t in chinese_texts]
all_y = [t["y"] for t in chinese_texts]
cx = (min(all_x) + max(all_x)) / 2
cy = (min(all_y) + max(all_y)) / 2
scale_x = max(all_x) - min(all_x)
scale_y = max(all_y) - min(all_y)

print(f"\n=== 坐标范围 ===")
print(f"X: {min(all_x):.0f} ~ {max(all_x):.0f} (跨度: {scale_x:.0f})")
print(f"Y: {min(all_y):.0f} ~ {max(all_y):.0f} (跨度: {scale_y:.0f})")
print(f"中心: ({cx:.0f}, {cy:.0f})")

def norm_x(x):
    return round((x - cx) / max(scale_x, scale_y) * 100, 1)

def norm_y(y):
    return round(-(y - cy) / max(scale_x, scale_y) * 100, 1)

result = {}
print(f"\n=== 归一化后坐标（以米为单位，约100m范围） ===")
for t in chinese_texts:
    text = t["text"].replace("\n", " ").strip()
    if not text:
        continue
    nx = norm_x(t["x"])
    ny = norm_y(t["y"])
    result[text] = {"x": nx, "y": ny}
    if len(text) < 30:
        print(f"  {text}: ({nx}, {ny})")

output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "normalized_layout.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
print(f"\n归一化数据已保存: {output_path}")
