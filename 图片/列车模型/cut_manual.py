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

large = []
for i in range(1, num_labels):
    x, y, w_c, h_c, area = stats[i]
    if area > 3000:
        large.append((i, x, y, w_c, h_c, area))

large.sort(key=lambda c: (c[2], c[1]))
print(f"找到 {len(large)} 个大面积区域:")
for idx, (i, x, y, w_c, h_c, area) in enumerate(large):
    print(f"  [{idx}] ID={i} ({x},{y}) {w_c}x{h_c} area={area}")

train_boxes = [
    (240, 69, 519, 406),
    (761, 76, 516, 70),
    (761, 149, 516, 71),
    (761, 222, 516, 82),
    (761, 311, 516, 78),
    (761, 392, 516, 83),
    (247, 481, 1030, 96),
    (247, 580, 1030, 95),
]

debug_img = img.copy()
colors = [(0,0,255), (0,255,0), (255,0,0), (0,255,255), (255,0,255), (255,255,0), (128,0,255), (0,128,255)]
for i, (x, y, w_b, h_b) in enumerate(train_boxes):
    c = colors[i % len(colors)]
    cv2.rectangle(debug_img, (x, y), (x + w_b, y + h_b), c, 3)
    cv2.putText(debug_img, str(i+1), (x + 10, y + 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, c, 2)
cv2.imwrite(r'F:\自开发程序\工厂建模\图片\列车模型\debug_boxes.png', debug_img)

output_dir = r'F:\自开发程序\工厂建模\图片\列车模型\列车剪切'
os.makedirs(output_dir, exist_ok=True)

padding = 5
for i, (x, y, w_b, h_b) in enumerate(train_boxes):
    x1 = max(0, x - padding)
    y1 = max(0, y - padding)
    x2 = min(w, x + w_b + padding)
    y2 = min(h, y + h_b + padding)
    cropped = img_pil.crop((x1, y1, x2, y2))
    save_path = os.path.join(output_dir, f'列车_{i+1}.png')
    cropped.save(save_path)
    print(f"列车_{i+1}.png: ({x1},{y1})->({x2},{y2}) {cropped.size[0]}x{cropped.size[1]}")

print("\n8个列车图标剪切完成!")
