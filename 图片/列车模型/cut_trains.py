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

debug_img = img.copy()
for idx, (i, x, y, w_c, h_c, area) in enumerate(components):
    color = [(0,0,255), (0,255,0), (255,0,0), (0,255,255), (255,0,255), (255,255,0), (128,0,255), (0,128,255), (255,128,0), (128,255,0), (0,255,128), (255,0,128), (128,128,255)]
    c = color[idx % len(color)]
    cv2.rectangle(debug_img, (x, y), (x + w_c, y + h_c), c, 2)
    cv2.putText(debug_img, f"{area}", (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, c, 1)

cv2.imwrite(r'F:\自开发程序\工厂建模\图片\列车模型\debug_all_regions.png', debug_img)

train1_box = (230, 65, 540, 415)

train_boxes = [
    (230, 65, 540, 415),
    (755, 70, 530, 80),
    (755, 143, 530, 85),
    (755, 215, 530, 95),
    (755, 305, 530, 85),
    (755, 386, 530, 95),
    (237, 475, 1045, 107),
    (237, 574, 1045, 107),
]

output_dir = r'F:\自开发程序\工厂建模\图片\列车模型\列车剪切'
os.makedirs(output_dir, exist_ok=True)

for i, (x, y, w_box, h_box) in enumerate(train_boxes):
    x1 = max(0, x)
    y1 = max(0, y)
    x2 = min(w, x + w_box)
    y2 = min(h, y + h_box)
    cropped = img_pil.crop((x1, y1, x2, y2))
    save_path = os.path.join(output_dir, f'列车_{i+1}.png')
    cropped.save(save_path)
    print(f"列车 {i+1}: 区域({x1},{y1},{x2},{y2}) 大小{cropped.size[0]}x{cropped.size[1]} -> {save_path}")

print("\n剪切完成！")
