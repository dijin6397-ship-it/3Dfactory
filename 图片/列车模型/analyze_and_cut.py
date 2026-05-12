import cv2
import numpy as np
from PIL import Image

img_pil = Image.open(r'F:\自开发程序\工厂建模\图片\列车模型\列车.jpg')
img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
thresh = cv2.dilate(thresh, kernel, iterations=2)
thresh = cv2.erode(thresh, kernel, iterations=2)

contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

boxes = []
for c in contours:
    x, y, w, h = cv2.boundingRect(c)
    area = w * h
    if area > 10000 and h > 100 and w > 100:
        boxes.append((x, y, w, h, area))

boxes.sort(key=lambda b: b[0])

print(f"找到 {len(boxes)} 个候选区域:")
for i, (x, y, w, h, area) in enumerate(boxes):
    print(f"  [{i}] 位置:({x},{y}) 大小:{w}x{h} 面积:{area}")

if len(boxes) < 8:
    print("\n尝试降低阈值...")
    boxes2 = []
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        area = w * h
        if area > 5000 and h > 50:
            boxes2.append((x, y, w, h, area))
    boxes2.sort(key=lambda b: b[0])
    print(f"降低阈值后找到 {len(boxes2)} 个候选区域:")
    for i, (x, y, w, h, area) in enumerate(boxes2):
        print(f"  [{i}] 位置:({x},{y}) 大小:{w}x{h} 面积:{area}")

def merge_overlapping(boxes, overlap_thresh=0.3):
    if not boxes:
        return []
    result = list(boxes)
    changed = True
    while changed:
        changed = False
        new_result = []
        used = set()
        for i in range(len(result)):
            if i in used:
                continue
            x1, y1, w1, h1, _ = result[i]
            merged = False
            for j in range(i + 1, len(result)):
                if j in used:
                    continue
                x2, y2, w2, h2, _ = result[j]
                ix = max(0, min(x1 + w1, x2 + w2) - max(x1, x2))
                iy = max(0, min(y1 + h1, y2 + h2) - max(y1, y2))
                intersection = ix * iy
                min_area = min(w1 * h1, w2 * h2)
                if min_area > 0 and intersection / min_area > overlap_thresh:
                    nx = min(x1, x2)
                    ny = min(y1, y2)
                    nw = max(x1 + w1, x2 + w2) - nx
                    nh = max(y1 + h1, y2 + h2) - ny
                    new_result.append((nx, ny, nw, nh, nw * nh))
                    used.add(j)
                    merged = True
                    changed = True
                    break
            if not merged and i not in used:
                new_result.append(result[i])
        result = new_result
    return result

merged = merge_overlapping(boxes)
merged.sort(key=lambda b: b[0])
print(f"\n合并后找到 {len(merged)} 个区域:")
for i, (x, y, w, h, area) in enumerate(merged):
    print(f"  [{i}] 位置:({x},{y}) 大小:{w}x{h} 面积:{area}")
