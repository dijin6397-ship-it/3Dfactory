"""
从 DXF 文件提取实际布局数据：文字标签、区域范围、建筑结构等
"""
import ezdxf
import json
import os

DXF_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
    "上海北翟路车辆段检修库厂房工艺布局局图2023.10.26终版-改压轮.dxf")

doc = ezdxf.readfile(DXF_FILE)
msp = doc.modelspace()

texts = []
lines = []
polylines = []
circles = []
arcs = []
rectangles = []
blocks_ref = []

for entity in msp:
    dtype = entity.dxftype()
    if dtype == "TEXT" or dtype == "MTEXT":
        text_content = entity.dxf.text if dtype == "TEXT" else entity.plain_text()
        pos = entity.dxf.insert
        texts.append({
            "type": dtype,
            "text": text_content.strip(),
            "x": round(pos.x, 2),
            "y": round(pos.y, 2),
            "height": round(entity.dxf.height, 2) if hasattr(entity.dxf, 'height') else 0,
        })
    elif dtype == "LINE":
        lines.append({
            "start": [round(entity.dxf.start.x, 2), round(entity.dxf.start.y, 2)],
            "end": [round(entity.dxf.end.x, 2), round(entity.dxf.end.y, 2)],
        })
    elif dtype == "LWPOLYLINE":
        pts = [(round(p[0], 2), round(p[1], 2)) for p in entity.get_points()]
        polylines.append({
            "points": pts,
            "closed": entity.closed if hasattr(entity, 'closed') else False,
        })
    elif dtype == "POLYLINE":
        try:
            pts = [(round(p.dxf.location.x, 2), round(p.dxf.location.y, 2)) for p in entity.vertices]
        except Exception:
            pts = []
        polylines.append({
            "points": pts,
            "closed": entity.is_closed if hasattr(entity, 'is_closed') else False,
        })
    elif dtype == "CIRCLE":
        circles.append({
            "center": [round(entity.dxf.center.x, 2), round(entity.dxf.center.y, 2)],
            "radius": round(entity.dxf.radius, 2),
        })
    elif dtype == "ARC":
        arcs.append({
            "center": [round(entity.dxf.center.x, 2), round(entity.dxf.center.y, 2)],
            "radius": round(entity.dxf.radius, 2),
            "start_angle": round(entity.dxf.start_angle, 2),
            "end_angle": round(entity.dxf.end_angle, 2),
        })
    elif dtype == "INSERT":
        blocks_ref.append({
            "block": entity.dxf.name,
            "insert": [round(entity.dxf.insert.x, 2), round(entity.dxf.insert.y, 2)],
        })

print(f"=== DXF 数据提取结果 ===")
print(f"文字标注: {len(texts)} 个")
print(f"直线: {len(lines)} 条")
print(f"多段线: {len(polylines)} 条")
print(f"圆形: {len(circles)} 个")
print(f"圆弧: {len(arcs)} 个")
print(f"块引用: {len(blocks_ref)} 个")

print(f"\n=== 文字标注（前80条）===")
for t in texts[:80]:
    print(f"  [{t['type']}] \"{t['text']}\" @ ({t['x']}, {t['y']}) h={t['height']}")

print(f"\n=== 文字标注（共{len(texts)}条，显示所有）===")
for t in texts:
    print(f"  \"{t['text']}\" @ ({t['x']}, {t['y']})")

all_x = []
all_y = []
for t in texts:
    all_x.append(t['x'])
    all_y.append(t['y'])
for l in lines:
    all_x.extend([l['start'][0], l['end'][0]])
    all_y.extend([l['start'][1], l['end'][1]])
for pl in polylines:
    for pt in pl['points']:
        all_x.append(pt[0])
        all_y.append(pt[1])

if all_x:
    print(f"\n=== 坐标范围 ===")
    print(f"X: {min(all_x):.2f} ~ {max(all_x):.2f}  (跨度: {max(all_x)-min(all_x):.2f})")
    print(f"Y: {min(all_y):.2f} ~ {max(all_y):.2f}  (跨度: {max(all_y)-min(all_y):.2f})")

blocks_in_doc = list(doc.blocks)
print(f"\n=== 块定义 ({len(blocks_in_doc)} 个) ===")
for b in blocks_in_doc:
    if not b.name.startswith('*'):
        entity_types = [e.dxftype() for e in b]
        print(f"  {b.name}: {len(list(b))} entities, types={entity_types[:10]}")

result = {
    "texts": texts,
    "summary": {
        "text_count": len(texts),
        "line_count": len(lines),
        "polyline_count": len(polylines),
        "circle_count": len(circles),
        "arc_count": len(arcs),
        "block_ref_count": len(blocks_ref),
        "x_range": [min(all_x), max(all_x)] if all_x else [0, 0],
        "y_range": [min(all_y), max(all_y)] if all_y else [0, 0],
    }
}

output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dxf_layout_data.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
print(f"\n数据已保存到: {output_path}")
