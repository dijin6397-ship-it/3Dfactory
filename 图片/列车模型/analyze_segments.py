import cv2
import numpy as np
from PIL import Image
import os

img_pil = Image.open(r'F:\自开发程序\工厂建模\图片\列车模型\列车.jpg')
img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
h, w = gray.shape

row_nonwhite = np.array([np.sum(gray[r, :] < 220) for r in range(h)])
col_nonwhite = np.array([np.sum(gray[:, c] < 220) for c in range(w)])

row_active = row_nonwhite > 50
col_active = col_nonwhite > 30

row_changes = np.diff(row_active.astype(int))
row_starts = np.where(row_changes == 1)[0] + 1
row_ends = np.where(row_changes == -1)[0] + 1

if row_active[0]:
    row_starts = np.insert(row_starts, 0, 0)
if row_active[-1]:
    row_ends = np.append(row_ends, h)

row_segments = []
for s, e in zip(row_starts, row_ends):
    if e - s > 20:
        row_segments.append((s, e))

print("行内容段落 (>20px):")
for i, (s, e) in enumerate(row_segments):
    print(f"  [{i}] 行 {s}-{e} (高度{e-s}px)")

col_changes = np.diff(col_active.astype(int))
col_starts = np.where(col_changes == 1)[0] + 1
col_ends = np.where(col_changes == -1)[0] + 1

if col_active[0]:
    col_starts = np.insert(col_starts, 0, 0)
if col_active[-1]:
    col_ends = np.append(col_ends, w)

col_segments = []
for s, e in zip(col_starts, col_ends):
    if e - s > 20:
        col_segments.append((s, e))

print("\n列内容段落 (>20px):")
for i, (s, e) in enumerate(col_segments):
    print(f"  [{i}] 列 {s}-{e} (宽度{e-s}px)")

print(f"\n图片: {w}x{h}")

print("\n--- 上部大区域(row 69-475)内部列分布 ---")
for c in range(240, 760, 10):
    region = gray[69:475, c:c+10]
    nonwhite_pct = np.sum(region < 220) / region.size
    if nonwhite_pct < 0.05:
        print(f"  列{c}-{c+9}: 空白({nonwhite_pct:.1%})")
