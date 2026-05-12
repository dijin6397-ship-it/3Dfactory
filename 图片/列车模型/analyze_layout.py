import cv2
import numpy as np
from PIL import Image

img_pil = Image.open(r'F:\自开发程序\工厂建模\图片\列车模型\列车.jpg')
img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

h, w = gray.shape

_, bw = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY_INV)
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(bw, connectivity=8)

debug_img = img.copy()
for i in range(1, num_labels):
    x, y, w_c, h_c, area = stats[i]
    if area > 3000:
        cv2.rectangle(debug_img, (x, y), (x + w_c, y + h_c), (0, 0, 255), 2)
        cv2.putText(debug_img, f"{i}:({x},{y}){w_c}x{h_c}", (x, y-5), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)

cv2.imwrite(r'F:\自开发程序\工厂建模\图片\列车模型\debug_regions.png', debug_img)

print("所有连通区域 (area > 3000):")
for i in range(1, num_labels):
    x, y, w_c, h_c, area = stats[i]
    if area > 3000:
        aspect = w_c / h_c if h_c > 0 else 0
        print(f"  [{i}] 位置({x},{y}) 大小{w_c}x{h_c} 面积{area} 宽高比{aspect:.2f} 中心({centroids[i][0]:.0f},{centroids[i][1]:.0f})")

print("\n\n=== 尝试检测数字标签 ===")
_, bw2 = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
num_labels2, labels2, stats2, centroids2 = cv2.connectedComponentsWithStats(bw2, connectivity=8)

number_candidates = []
for i in range(1, num_labels2):
    x, y, w_c, h_c, area = stats2[i]
    if 50 < area < 3000 and 0.3 < w_c/h_c < 1.5 and w_c > 8 and h_c > 12:
        number_candidates.append((x, y, w_c, h_c, area, centroids2[i]))

number_candidates.sort(key=lambda c: (c[1], c[0]))
print(f"数字候选区域 (50<area<3000): {len(number_candidates)}个")
for i, (x, y, w_c, h_c, area, cent) in enumerate(number_candidates[:50]):
    print(f"  [{i}] 位置({x},{y}) 大小{w_c}x{h_c} 面积{area} 中心({cent[0]:.0f},{cent[1]:.0f})")
