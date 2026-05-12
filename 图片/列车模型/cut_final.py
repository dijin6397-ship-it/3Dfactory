import cv2
import numpy as np
from PIL import Image
import os

img_pil = Image.open(r'F:\自开发程序\工厂建模\图片\列车模型\列车.jpg')
img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
h, w = gray.shape

_, bw = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY_INV)
kernel = np.ones((15, 15), np.uint8)
bw_dilated = cv2.dilate(bw, kernel, iterations=2)

num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(bw_dilated, connectivity=8)

components = []
for i in range(1, num_labels):
    x, y, w_c, h_c, area = stats[i]
    if area > 10000:
        components.append((i, x, y, w_c, h_c, area))

components.sort(key=lambda c: (c[2], c[1]))

print(f"形态学处理后连通区域 ({len(components)}个):")
for idx, (i, x, y, w_c, h_c, area) in enumerate(components):
    print(f"  [{idx}] 位置({x},{y}) 大小{w_c}x{h_c} 面积{area}")

train_regions = []
for i, x, y, w_c, h_c, area in components:
    if area > 100000:
        train_regions.append((x, y, w_c, h_c))
    elif 20000 < area < 100000 and w_c > 300:
        train_regions.append((x, y, w_c, h_c))

train_regions.sort(key=lambda r: (r[1], r[0]))

print(f"\n选定 {len(train_regions)} 个列车区域:")
for i, (x, y, w_c, h_c) in enumerate(train_regions):
    print(f"  列车{i+1}: 位置({x},{y}) 大小{w_c}x{h_c}")

debug_img = img.copy()
colors = [(0,0,255), (0,255,0), (255,0,0), (0,255,255), (255,0,255), (255,255,0), (128,0,255), (0,128,255)]
for i, (x, y, w_c, h_c) in enumerate(train_regions):
    c = colors[i % len(colors)]
    cv2.rectangle(debug_img, (x, y), (x + w_c, y + h_c), c, 3)
    cv2.putText(debug_img, f"{i+1}", (x + 10, y + 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, c, 2)

cv2.imwrite(r'F:\自开发程序\工厂建模\图片\列车模型\debug_final_boxes.png', debug_img)

if len(train_regions) >= 8:
    output_dir = r'F:\自开发程序\工厂建模\图片\列车模型\列车剪切'
    os.makedirs(output_dir, exist_ok=True)
    
    padding = 5
    for i, (x, y, w_box, h_box) in enumerate(train_regions[:8]):
        x1 = max(0, x - padding)
        y1 = max(0, y - padding)
        x2 = min(w, x + w_box + padding)
        y2 = min(h, y + h_box + padding)
        cropped = img_pil.crop((x1, y1, x2, y2))
        save_path = os.path.join(output_dir, f'列车_{i+1}.png')
        cropped.save(save_path)
        print(f"保存: 列车_{i+1}.png ({cropped.size[0]}x{cropped.size[1]})")
    print("\n8个列车图标剪切完成!")
else:
    print(f"\n只找到{len(train_regions)}个区域，不足8个，需要手动调整")
