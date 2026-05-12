import cv2
import numpy as np
from PIL import Image

img_pil = Image.open(r'F:\自开发程序\工厂建模\图片\列车模型\列车.jpg')
img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

_, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

cv2.imwrite(r'F:\自开发程序\工厂建模\图片\列车模型\debug_thresh.png', thresh)

h, w = gray.shape
print(f"图片大小: {w}x{h}")

row_white_count = []
for r in range(h):
    white_pixels = np.sum(gray[r, :] > 240)
    row_white_count.append(white_pixels)

col_white_count = []
for c in range(w):
    white_pixels = np.sum(gray[:, c] > 240)
    col_white_count.append(white_pixels)

row_white_count = np.array(row_white_count)
col_white_count = np.array(col_white_count)

horizontal_lines = np.where(row_white_count > w * 0.9)[0]
vertical_lines = np.where(col_white_count > h * 0.9)[0]

def group_indices(indices, gap=5):
    if len(indices) == 0:
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

h_groups = group_indices(horizontal_lines, 5)
v_groups = group_indices(vertical_lines, 5)

print(f"水平白色线段 (>90%白): {h_groups}")
print(f"垂直白色线段 (>90%白): {v_groups}")

horizontal_lines2 = np.where(row_white_count > w * 0.8)[0]
vertical_lines2 = np.where(col_white_count > h * 0.8)[0]
h_groups2 = group_indices(horizontal_lines2, 5)
v_groups2 = group_indices(vertical_lines2, 5)
print(f"\n水平白色线段 (>80%白): {h_groups2}")
print(f"垂直白色线段 (>80%白): {v_groups2}")

h_lines3 = np.where(row_white_count > w * 0.7)[0]
v_lines3 = np.where(col_white_count > h * 0.7)[0]
h_groups3 = group_indices(h_lines3, 5)
v_groups3 = group_indices(v_lines3, 5)
print(f"\n水平白色线段 (>70%白): {h_groups3}")
print(f"垂直白色线段 (>70%白): {v_groups3}")

print("\n--- 尝试检测低白像素列（分隔线候选）---")
# 找列中白像素占比高的（即可能的分割线是高白列）
# 反过来：找每列中白像素少的区域
low_white_cols = np.where(col_white_count < h * 0.3)[0]
low_groups = group_indices(low_white_cols, 5)
print(f"低白像素列 (<30%白): {low_groups[:20]}")

low_white_rows = np.where(row_white_count < w * 0.3)[0]
low_row_groups = group_indices(low_white_rows, 5)
print(f"低白像素行 (<30%白): {low_row_groups[:20]}")
