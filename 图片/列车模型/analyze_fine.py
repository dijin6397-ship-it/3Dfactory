import cv2
import numpy as np
from PIL import Image

img_pil = Image.open(r'F:\自开发程序\工厂建模\图片\列车模型\列车.jpg')
img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

h, w = gray.shape

row_white = np.array([np.sum(gray[r, :] > 235) for r in range(h)])
col_white = np.array([np.sum(gray[:, c] > 235) for c in range(w)])

print("=== 主内容区域(行69-674, 列240-1276)的精细分析 ===")

print("\n--- 列240-1276 中每列的白像素占比 ---")
prev_pct = 0
for c in range(240, 1277):
    white_pct = col_white[c] / h
    if white_pct > 0.88:
        if prev_pct <= 0.88:
            print(f"  白色列开始: {c} ({white_pct:.1%})")
    else:
        if prev_pct > 0.88:
            print(f"  白色列结束: {c-1}")
    prev_pct = white_pct

print("\n--- 行69-674 中每行的白像素占比 ---")
prev_pct = 0
for r in range(69, 675):
    white_pct = row_white[r] / w
    if white_pct > 0.88:
        if prev_pct <= 0.88:
            print(f"  白色行开始: {r} ({white_pct:.1%})")
    else:
        if prev_pct > 0.88:
            print(f"  白色行结束: {r-1}")
    prev_pct = white_pct

print("\n--- 行76-474区域(第一大块)的列分析 ---")
for c in range(240, 1277, 1):
    region = gray[76:475, c]
    white_pct = np.sum(region > 235) / len(region)
    if white_pct > 0.95:
        pass

def find_vertical_splits(img_gray, row_start, row_end, col_start, col_end, threshold=0.90):
    region = img_gray[row_start:row_end, col_start:col_end]
    h_r, w_r = region.shape
    splits = []
    for c in range(w_r):
        white_pct = np.sum(region[:, c] > 235) / h_r
        if white_pct > threshold:
            splits.append(col_start + c)
    return splits

print("\n--- 行76-474, 列240-1276 垂直分割检测 ---")
splits1 = find_vertical_splits(gray, 76, 475, 240, 1277, 0.85)
def group_consecutive(indices, gap=5):
    if not indices:
        return []
    groups = []
    start = indices[0]
    prev = indices[0]
    for idx in indices[1:]:
        if idx - prev > gap:
            groups.append((start, prev))
            start = idx
        prev = idx
    groups.append((start, prev))
    return groups

col_splits1 = group_consecutive(splits1, 5)
print(f"垂直分割线: {col_splits1}")

print("\n--- 行481-576, 列240-1276 垂直分割检测 ---")
splits2 = find_vertical_splits(gray, 481, 577, 240, 1277, 0.85)
col_splits2 = group_consecutive(splits2, 5)
print(f"垂直分割线: {col_splits2}")

print("\n--- 行580-674, 列240-1276 垂直分割检测 ---")
splits3 = find_vertical_splits(gray, 580, 675, 240, 1277, 0.85)
col_splits3 = group_consecutive(splits3, 5)
print(f"垂直分割线: {col_splits3}")

print("\n=== 尝试不同的方法：找内容区块（连通区域）===")
_, bw = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY_INV)
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(bw, connectivity=8)

large_components = []
for i in range(1, num_labels):
    x, y, w_c, h_c, area = stats[i]
    if area > 5000:
        large_components.append((x, y, w_c, h_c, area, centroids[i]))

large_components.sort(key=lambda c: -c[4])
print(f"大面积连通区域 (area > 5000): {len(large_components)}个")
for i, (x, y, w_c, h_c, area, cent) in enumerate(large_components[:30]):
    print(f"  [{i}] 位置({x},{y}) 大小{w_c}x{h_c} 面积{area} 中心({cent[0]:.0f},{cent[1]:.0f})")
