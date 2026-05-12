import cv2
import numpy as np
from PIL import Image

img_pil = Image.open(r'F:\自开发程序\工厂建模\图片\列车模型\列车.jpg')
img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

h, w = gray.shape
print(f"图片大小: {w}x{h}")

row_white_count = np.array([np.sum(gray[r, :] > 240) for r in range(h)])
col_white_count = np.array([np.sum(gray[:, c] > 240) for c in range(w)])

def find_segments(counts, threshold_pct):
    threshold = 0
    if threshold_pct > 1:
        threshold = threshold_pct
    else:
        max_val = counts.max()
        threshold = max_val * threshold_pct
    is_white = counts > threshold
    segments = []
    start = None
    for i, val in enumerate(is_white):
        if val:
            if start is None:
                start = i
        else:
            if start is not None:
                segments.append((start, i - 1))
                start = None
    if start is not None:
        segments.append((start, len(is_white) - 1))
    return segments

row_white_segs = find_segments(row_white_count, 0.7)
col_white_segs = find_segments(col_white_count, 0.7)

print(f"\n水平白色区域 (>70%):")
for s, e in row_white_segs:
    print(f"  行 {s}-{e} (高度{e-s+1}px)")

print(f"\n垂直白色区域 (>70%):")
for s, e in col_white_segs:
    print(f"  列 {s}-{e} (宽度{e-s+1}px)")

row_content_segs = find_segments(1.0 - row_white_count / w, 0.3)
col_content_segs = find_segments(1.0 - col_white_count / h, 0.3)

print(f"\n水平内容区域 (>30%非白):")
for s, e in row_content_segs:
    print(f"  行 {s}-{e} (高度{e-s+1}px)")

print(f"\n垂直内容区域 (>30%非白):")
for s, e in col_content_segs:
    print(f"  列 {s}-{e} (宽度{e-s+1}px)")

print("\n--- 细化分析主内容区域(行76-674)的垂直分隔 ---")
for c in range(240, 1140, 5):
    white_pct = col_white_count[c] / h
    if white_pct > 0.85:
        print(f"  列{c}: 白像素占比{white_pct:.1%}")

print("\n--- 细化分析主内容区域(列243-1131)的水平分隔 ---")
for r in range(69, 680, 3):
    white_pct = row_white_count[r] / w
    if white_pct > 0.85:
        print(f"  行{r}: 白像素占比{white_pct:.1%}")
