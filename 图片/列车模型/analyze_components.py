import cv2
import numpy as np
from PIL import Image
import os

img_pil = Image.open(r'F:\自开发程序\工厂建模\图片\列车模型\列车.jpg')
img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
h, w = gray.shape
print(f"图片尺寸: {w}x{h}")

_, bw = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY_INV)
kernel = np.ones((10, 10), np.uint8)
bw_dilated = cv2.dilate(bw, kernel, iterations=3)
bw_closed = cv2.erode(bw_dilated, kernel, iterations=3)

num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(bw_closed, connectivity=8)

components = []
for i in range(1, num_labels):
    x, y, w_c, h_c, area = stats[i]
    if area > 5000:
        components.append((i, x, y, w_c, h_c, area))

components.sort(key=lambda c: (-c[5], c[2], c[1]))

print(f"\n形态学处理后的连通区域 (area > 5000): {len(components)}个")
for idx, (i, x, y, w_c, h_c, area) in enumerate(components):
    print(f"  [{idx}] ID={i} 位置({x},{y}) 大小{w_c}x{h_c} 面积{area}")

train_boxes = []
for i, x, y, w_c, h_c, area in components:
    if area > 100000:
        train_boxes.append((x, y, w_c, h_c))
    elif 30000 < area < 100000 and w_c > 200:
        train_boxes.append((x, y, w_c, h_c))

train_boxes.sort(key=lambda b: (b[1], b[0]))

print(f"\n选定 {len(train_boxes)} 个列车区域:")
for i, (x, y, w_c, h_c) in enumerate(train_boxes):
    print(f"  列车{i+1}: 位置({x},{y}) 大小{w_c}x{h_c}")

debug_img = img.copy()
colors = [(0,0,255), (0,255,0), (255,0,0), (0,255,255), (255,0,255), (255,255,0), (128,0,255), (0,128,255)]
for i, (x, y, w_c, h_c) in enumerate(train_boxes):
    c = colors[i % len(colors)]
    cv2.rectangle(debug_img, (x, y), (x + w_c, y + h_c), c, 3)
    cv2.putText(debug_img, f"{i+1}", (x + 10, y + 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, c, 2)

cv2.imwrite(r'F:\自开发程序\工厂建模\图片\列车模型\debug_components.png', debug_img)
print("调试图已保存")
