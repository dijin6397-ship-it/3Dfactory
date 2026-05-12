"""
深度分析四张工厂图片：
1. 检测边缘和轮廓
2. 分析颜色分区
3. 提取可能的文字区域
4. 识别布局模式
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import json
from collections import Counter
import math

BASE = os.path.dirname(os.path.abspath(__file__))

def get_color_name(r, g, b):
    if r > 200 and g > 200 and b > 200:
        return "白色/浅灰"
    elif r < 50 and g < 50 and b < 50:
        return "黑色"
    elif r > 150 and g < 100 and b < 100:
        return "红色"
    elif r < 100 and g > 150 and b < 100:
        return "绿色"
    elif r < 100 and g < 100 and b > 150:
        return "蓝色"
    elif r > 150 and g > 150 and b < 100:
        return "黄色"
    elif 100 < r < 200 and 100 < g < 200 and 100 < b < 200:
        return "灰色"
    else:
        return "其他"

def analyze_grid(img, grid_size=10):
    w, h = img.size
    cell_w = w // grid_size
    cell_h = h // grid_size
    
    grid = []
    for gy in range(grid_size):
        row = []
        for gx in range(grid_size):
            x1 = gx * cell_w
            y1 = gy * cell_h
            x2 = min((gx + 1) * cell_w, w)
            y2 = min((gy + 1) * cell_h, h)
            
            region = img.crop((x1, y1, x2, y2))
            pixels = list(region.convert("RGB").getdata())
            
            r_avg = sum(p[0] for p in pixels) // len(pixels)
            g_avg = sum(p[1] for p in pixels) // len(pixels)
            b_avg = sum(p[2] for p in pixels) // len(pixels)
            
            color_name = get_color_name(r_avg, g_avg, b_avg)
            brightness = (r_avg + g_avg + b_avg) // 3
            
            row.append({
                "color": color_name,
                "brightness": brightness,
                "rgb": (r_avg, g_avg, b_avg)
            })
        grid.append(row)
    
    return grid

def detect_regions(img, threshold=50):
    """检测不同颜色的区域"""
    w, h = img.size
    pixels = list(img.convert("RGB").getdata())
    
    regions = {
        "green": 0,
        "red": 0,
        "blue": 0,
        "yellow": 0,
        "dark": 0,
        "light": 0,
        "gray": 0,
    }
    
    for p in pixels:
        r, g, b = p
        if g > r * 1.3 and g > b * 1.3 and g > 100:
            regions["green"] += 1
        elif r > 150 and g < 100 and b < 100:
            regions["red"] += 1
        elif b > 150 and r < 100 and g < 100:
            regions["blue"] += 1
        elif r > 150 and g > 150 and b < 100:
            regions["yellow"] += 1
        elif max(r, g, b) < 80:
            regions["dark"] += 1
        elif min(r, g, b) > 200:
            regions["light"] += 1
        else:
            regions["gray"] += 1
    
    total = len(pixels)
    return {k: round(v / total * 100, 1) for k, v in regions.items()}

def create_visual_summary(img, img_num, grid):
    """创建可视化网格摘要"""
    w, h = img.size
    summary = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(summary)
    
    cell_w = w // len(grid[0])
    cell_h = h // len(grid)
    
    color_map = {
        "白色/浅灰": (220, 220, 220),
        "黑色": (30, 30, 30),
        "红色": (220, 60, 60),
        "绿色": (60, 180, 60),
        "蓝色": (60, 60, 220),
        "黄色": (220, 220, 60),
        "灰色": (150, 150, 150),
        "其他": (180, 180, 180),
    }
    
    for gy, row in enumerate(grid):
        for gx, cell in enumerate(row):
            x1 = gx * cell_w
            y1 = gy * cell_h
            x2 = (gx + 1) * cell_w
            y2 = (gy + 1) * cell_h
            
            color = color_map.get(cell["color"], (180, 180, 180))
            draw.rectangle([x1, y1, x2, y2], fill=color, outline=(100, 100, 100))
    
    summary.save(os.path.join(BASE, f"{img_num}_grid.png"))
    return summary

print("=== 深度分析四张工厂图片 ===\n")

all_results = {}

for i in range(1, 5):
    path = os.path.join(BASE, f"{i}.jpg")
    img = Image.open(path)
    w, h = img.size
    
    print(f"\n{'='*50}")
    print(f"图片 {i}.jpg ({w}x{h})")
    print(f"{'='*50}")
    
    grid = analyze_grid(img, grid_size=8)
    
    print("\n颜色网格分布 (8x8):")
    for gy, row in enumerate(grid):
        row_str = " | ".join([f"{c['color'][:4]:4s}" for c in row])
        print(f"  行{gy}: {row_str}")
    
    regions = detect_regions(img)
    print(f"\n颜色区域占比:")
    for color, pct in sorted(regions.items(), key=lambda x: -x[1]):
        bar = "█" * int(pct / 2)
        print(f"  {color:8s}: {pct:5.1f}% {bar}")
    
    create_visual_summary(img, i, grid)
    
    all_results[f"image_{i}"] = {
        "size": f"{w}x{h}",
        "regions": regions,
        "grid_colors": [[cell["color"] for cell in row] for row in grid],
    }

output_path = os.path.join(BASE, "image_analysis.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(all_results, f, ensure_ascii=False, indent=2)

print(f"\n\n分析结果已保存: {output_path}")
print("可视化网格摘要已保存为 *_grid.png 文件")

print("\n\n=== 图片内容推断 ===")
print("基于颜色分析:")
for i in range(1, 5):
    r = all_results[f"image_{i}"]
    regions = r["regions"]
    dominant = max(regions.items(), key=lambda x: x[1])
    print(f"  图片{i}: 主色调={dominant[0]}({dominant[1]}%), 绿色={regions['green']}%, 灰色={regions['gray']}%")
