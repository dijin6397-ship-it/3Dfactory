"""
分析四张工厂图片的基本信息和颜色分布，
帮助理解图片内容以重建3D模型。
"""
from PIL import Image
import os
import json

BASE = os.path.dirname(os.path.abspath(__file__))

for i in range(1, 5):
    path = os.path.join(BASE, f"{i}.jpg")
    img = Image.open(path)
    w, h = img.size
    mode = img.mode

    img_rgb = img.convert("RGB")
    pixels = list(img_rgb.getdata())

    r_avg = sum(p[0] for p in pixels) / len(pixels)
    g_avg = sum(p[1] for p in pixels) / len(pixels)
    b_avg = sum(p[2] for p in pixels) / len(pixels)

    dark = sum(1 for p in pixels if max(p) < 80)
    medium = sum(1 for p in pixels if 80 <= max(p) < 200)
    bright = sum(1 for p in pixels if max(p) >= 200)
    total = len(pixels)

    from collections import Counter
    quantized = [(p[0]//32*32, p[1]//32*32, p[2]//32*32) for p in pixels]
    color_counts = Counter(quantized).most_common(10)

    print(f"\n=== 图片 {i}.jpg ===")
    print(f"  尺寸: {w} x {h} 像素")
    print(f"  模式: {mode}")
    print(f"  平均颜色: R={r_avg:.0f} G={g_avg:.0f} B={b_avg:.0f}")
    print(f"  亮度分布: 暗区={dark/total*100:.1f}% 中间={medium/total*100:.1f}% 亮区={bright/total*100:.1f}%")
    print(f"  主要颜色 (RGB):")
    for color, count in color_counts[:5]:
        pct = count / total * 100
        print(f"    {color}: {pct:.1f}%")

    top_colors = [(c, cnt) for c, cnt in color_counts[:10]]

    center_region = img_rgb.crop((w//4, h//4, 3*w//4, 3*h//4))
    center_pixels = list(center_region.getdata())
    c_r = sum(p[0] for p in center_pixels) / len(center_pixels)
    c_g = sum(p[1] for p in center_pixels) / len(center_pixels)
    c_b = sum(p[2] for p in center_pixels) / len(center_pixels)
    print(f"  中心区域平均颜色: R={c_r:.0f} G={c_g:.0f} B={c_b:.0f}")
