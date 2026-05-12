"""
尝试从图片中提取文字信息，理解工厂布局。
使用多种方法尝试。
"""
from PIL import Image
import os
import json

BASE = os.path.dirname(os.path.abspath(__file__))

for i in range(1, 5):
    path = os.path.join(BASE, f"{i}.jpg")
    img = Image.open(path)
    w, h = img.size
    print(f"\n=== 图片 {i}.jpg: {w}x{h} ===")

    gray = img.convert("L")

    width_step = max(w // 20, 1)
    height_step = max(h // 20, 1)

    for y_pos in range(0, h, height_step):
        for x_pos in range(0, w, width_step):
            region = gray.crop((x_pos, y_pos, min(x_pos+width_step, w), min(y_pos+height_step, h)))
            pixels = list(region.getdata())
            avg = sum(pixels) / len(pixels) if pixels else 128
            if avg < 50:
                pass

    img_rgb = img.convert("RGB")
    pixels = list(img_rgb.getdata())

    green_pixels = [(i % w, i // w) for i, p in enumerate(pixels) if p[1] > 120 and p[1] > p[0] * 1.5 and p[1] > p[2] * 1.5]
    print(f"  绿色像素（可能是文字/标注）: {len(green_pixels)} 个")

    if green_pixels:
        min_x = min(p[0] for p in green_pixels)
        max_x = max(p[0] for p in green_pixels)
        min_y = min(p[1] for p in green_pixels)
        max_y = max(p[1] for p in green_pixels)
        print(f"  绿色区域范围: x=[{min_x}, {max_x}], y=[{min_y}, {max_y}]")

    dark_pixels = [(i % w, i // w) for i, p in enumerate(pixels) if max(p) < 40]
    print(f"  深色像素（可能是线条/边框）: {len(dark_pixels)} 个")
    if dark_pixels:
        min_x = min(p[0] for p in dark_pixels)
        max_x = max(p[0] for p in dark_pixels)
        min_y = min(p[1] for p in dark_pixels)
        max_y = max(p[1] for p in dark_pixels)
        print(f"  深色区域范围: x=[{min_x}, {max_x}], y=[{min_y}, {max_y}]")

    img.save(os.path.join(BASE, f"{i}_analysis.png"))

print("\n\n尝试安装 pytesseract...")
try:
    import pytesseract
    print("pytesseract 可用，开始 OCR...")
except ImportError:
    print("pytesseract 不可用")

try:
    import subprocess
    result = subprocess.run(["tesseract", "--version"], capture_output=True, text=True)
    print(f"tesseract 版本: {result.stdout[:100]}")
except Exception:
    print("tesseract 未安装")
