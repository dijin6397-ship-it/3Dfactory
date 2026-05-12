# -*- coding: utf-8 -*-
"""
DXF文件解析脚本 - 上海北翟路车辆段检修库
解析DXF文件，提取实体信息并生成3D场景数据
"""

import ezdxf
import json
import math

# 打开DXF文件
dxf_path = r"F:\自开发程序\工厂建模\上海北翟路车辆段检修库厂房工艺布局局图2023.10.26终版-改压轮.dxf"
doc = ezdxf.readfile(dxf_path)

# 获取模型空间
msp = doc.modelspace()

# 数据收集
elements = {
    "lines": [],
    "polylines": [],
    "circles": [],
    "texts": [],
    "arcs": [],
    "dimensions": [],
    "inserts": [],  # 块引用
}

# 遍历所有实体
for entity in msp:
    # 线条
    if entity.dxftype() == "LINE":
        elements["lines"].append({
            "layer": entity.dxf.layer,
            "color": entity.dxf.color if hasattr(entity.dxf, 'color') else None,
            "start": (entity.dxf.start.x, entity.dxf.start.y),
            "end": (entity.dxf.end.x, entity.dxf.end.y),
        })

    # 多段线
    elif entity.dxftype() == "LWPOLYLINE" or entity.dxftype() == "POLYLINE":
        points = []
        if hasattr(entity, 'get_points'):
            for point in entity.get_points():
                points.append((point[0], point[1]))
        elif hasattr(entity, 'vertices'):
            for vertex in entity.vertices:
                points.append((vertex.dxf.location.x, vertex.dxf.location.y))
        if points:
            elements["polylines"].append({
                "layer": entity.dxf.layer,
                "color": entity.dxf.color if hasattr(entity.dxf, 'color') else None,
                "points": points,
                "closed": entity.dxf.closed if hasattr(entity.dxf, 'closed') else False,
            })

    # 圆
    elif entity.dxftype() == "CIRCLE":
        elements["circles"].append({
            "layer": entity.dxf.layer,
            "center": (entity.dxf.center.x, entity.dxf.center.y),
            "radius": entity.dxf.radius,
        })

    # 圆弧
    elif entity.dxftype() == "ARC":
        elements["arcs"].append({
            "layer": entity.dxf.layer,
            "center": (entity.dxf.center.x, entity.dxf.center.y),
            "radius": entity.dxf.radius,
            "start_angle": entity.dxf.start_angle,
            "end_angle": entity.dxf.end_angle,
        })

    # 文字
    elif entity.dxftype() == "MTEXT" or entity.dxftype() == "TEXT":
        if entity.dxftype() == "MTEXT":
            text = entity.text
            insertion = entity.dxf.insert
            height = entity.dxf.char_height
        else:
            text = entity.dxf.text
            insertion = entity.dxf.insert
            height = entity.dxf.height if hasattr(entity.dxf, 'height') else 2.5

        elements["texts"].append({
            "layer": entity.dxf.layer,
            "text": text,
            "location": (insertion.x, insertion.y),
            "height": height,
            "rotation": entity.dxf.rotation if hasattr(entity.dxf, 'rotation') else 0,
        })

    # 块引用
    elif entity.dxftype() == "INSERT":
        elements["inserts"].append({
            "layer": entity.dxf.layer,
            "name": entity.dxf.name,
            "location": (entity.dxf.insert.x, entity.dxf.insert.y),
            "rotation": entity.dxf.rotation if hasattr(entity.dxf, 'rotation') else 0,
            "scale": (entity.dxf.xscale if hasattr(entity.dxf, 'xscale') else 1,
                     entity.dxf.yscale if hasattr(entity.dxf, 'yscale') else 1),
        })

    # 尺寸标注
    elif entity.dxftype() == "DIMENSION":
        elements["dimensions"].append({
            "layer": entity.dxf.layer,
            "type": entity.dxf.dimension_type,
        })

# 统计
print(f"=== DXF解析结果 ===")
print(f"线条: {len(elements['lines'])}")
print(f"多段线: {len(elements['polylines'])}")
print(f"圆: {len(elements['circles'])}")
print(f"圆弧: {len(elements['arcs'])}")
print(f"文字: {len(elements['texts'])}")
print(f"块引用: {len(elements['inserts'])}")
print(f"尺寸标注: {len(elements['dimensions'])}")

# 分析图层
layers = set()
for key in elements:
    for item in elements[key]:
        if 'layer' in item:
            layers.add(item['layer'])

print(f"\n图层列表: {sorted(layers)}")

# 保存原始数据
with open(r"F:\自开发程序\工厂建模\3d-factory-viewer\src\dxf_raw_data.json", "w", encoding="utf-8") as f:
    json.dump(elements, f, ensure_ascii=False, indent=2)

print(f"\n原始数据已保存到 dxf_raw_data.json")