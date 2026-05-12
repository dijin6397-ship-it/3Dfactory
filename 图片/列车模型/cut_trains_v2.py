import cv2
import numpy as np
from PIL import Image
import os

img_pil = Image.open(r'F:\自开发程序\工厂建模\图片\列车模型\列车.jpg')
img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
h, w = gray.shape

_, bw = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY_INV)
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(bw, connectivity=8)

components = []
for i in range(1, num_labels):
    x, y, w_c, h_c, area = stats[i]
    if area > 3000:
        components.append((i, x, y, w_c, h_c, area))

components.sort(key=lambda c: (c[2], c[1]))

print("所有连通区域 (area > 3000):")
for idx, (i, x, y, w_c, h_c, area) in enumerate(components):
    print(f"  [{idx}] ID={i} 位置({x},{y}) 大小{w_c}x{h_c} 面积{area}")

train_regions = []

for i, x, y, w_c, h_c, area in components:
    if area > 100000 and x > 200 and y < 200:
        train_regions.append((x, y, w_c, h_c, f"列车1"))
        print(f"\n选定列车1: 位置({x},{y}) 大小{w_c}x{h_c}")

for i, x, y, w_c, h_c, area in components:
    if 700 < x < 800 and 60 < y < 500 and 500 < w_c < 600 and 50 < h_c < 100:
        train_regions.append((x, y, w_c, h_c, f"列车{len(train_regions)+1}"))
        print(f"选定列车{len(train_regions)}: 位置({x},{y}) 大小{w_c}x{h_c}")

for i, x, y, w_c, h_c, area in components:
    if 200 < x < 300 and 450 < y < 700 and 1000 < w_c < 1100 and 80 < h_c < 120:
        train_regions.append((x, y, w_c, h_c, f"列车{len(train_regions)+1}"))
        print(f"选定列车{len(train_regions)}: 位置({x},{y}) 大小{w_c}x{h_c}")

for i, x, y, w_c, h_c, area in components:
    if 200 < x < 300 and 350 < y < 450 and 300 < w_c < 500 and 80 < h_c < 150:
        train_regions.append((x, y, w_c, h_c, f"列车{len(train_regions)+1}"))
        print(f"选定列车{len(train_regions)}: 位置({x},{y}) 大小{w_c}x{h_c}")

train_regions.sort(key=lambda r: r[2])

output_dir = r'F:\自开发程序\工厂建模\图片\列车模型\列车剪切'
os.makedirs(output_dir, exist_ok=True)

padding = 15
for i, (x, y, w_box, h_box, name) in enumerate(train_regions):
    x1 = max(0, x - padding)
    y1 = max(0, y - padding)
    x2 = min(w, x + w_box + padding)
    y2 = min(h, y + h_box + padding)
    cropped = img_pil.crop((x1, y1, x2, y2))
    save_path = os.path.join(output_dir, f'列车_{i+1}.png')
    cropped.save(save_path)
    print(f"保存 {name}: 区域({x1},{y1},{x2},{y2}) 大小{cropped.size[0]}x{cropped.size[1]} -> {save_path}")

print(f"\n共剪切 {len(train_regions)} 个列车图标")

debug_img = img.copy()
for i, (x, y, w_box, h_box, name) in enumerate(train_regions):
    color = [(0,0,255), (0,255,0), (255,0,0), (0,255,255), (255,0,255), (255,255,0), (128,0,255), (0,128,255)]
    c = color[i % len(color)]
    cv2.rectangle(debug_img, (x, y), (x + w_box, y + h_box), c, 3)
    cv2.putText(debug_img, f"{i+1}", (x + 5, y + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, c, 2)

cv2.imwrite(r'F:\自开发程序\工厂建模\图片\列车模型\debug_final.png', debug_img)
print("调试图片已保存为 debug_final.png")
