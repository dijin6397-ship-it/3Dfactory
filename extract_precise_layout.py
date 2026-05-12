import cv2
import numpy as np
import json
import shutil
import tempfile
import os

TEMP_DIR = tempfile.mkdtemp()
FRAME_DIR = r'f:\自开发程序\工厂建模\video_frames'
OUT_DIR = r'f:\自开发程序\工厂建模\video_analysis'
os.makedirs(OUT_DIR, exist_ok=True)

def safe_imread(src_path):
    name = os.path.basename(src_path)
    dst = os.path.join(TEMP_DIR, name)
    with open(src_path, 'rb') as f:
        data = f.read()
    with open(dst, 'wb') as f:
        f.write(data)
    img = cv2.imread(dst)
    os.remove(dst)
    return img

def find_color_regions(img, hsv, color_name, lower, upper, min_area=300):
    mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    regions = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < min_area:
            continue
        x, y, w, h = cv2.boundingRect(cnt)
        regions.append({'x': x, 'y': y, 'w': w, 'h': h, 'area': int(area)})
    regions.sort(key=lambda r: (r['y'], r['x']))
    return regions

def find_text_regions(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    kernel = np.ones((3,3), np.uint8)
    dilated = cv2.dilate(thresh, kernel, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    text_regions = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if 10 < w < 400 and 10 < h < 60:
            roi = img[y:y+h, x:x+w]
            avg_brightness = np.mean(cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY))
            if avg_brightness > 180:
                text_regions.append({'x': x, 'y': y, 'w': w, 'h': h})
    text_regions.sort(key=lambda r: (r['y'], r['x']))
    return text_regions

print("=" * 70)
print("FACTORY LAYOUT: factory_frame_000_t0.0s.jpg.jpg")
print("=" * 70)

fp = os.path.join(FRAME_DIR, 'factory_frame_000_t0.0s.jpg.jpg')
img = safe_imread(fp)
h, w = img.shape[:2]
print(f"Image size: {w}x{h}")

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

green_regions = find_color_regions(img, hsv, 'green', (35, 40, 40), (85, 255, 255), 500)
print(f"\nGreen zones (上体检修区): {len(green_regions)}")
for i, r in enumerate(green_regions):
    print(f"  [{i}] x={r['x']}, y={r['y']}, w={r['w']}, h={r['h']}, area={r['area']}")

brown_regions = find_color_regions(img, hsv, 'brown', (10, 30, 50), (20, 180, 200), 500)
print(f"\nBrown zones (起车区): {len(brown_regions)}")
for i, r in enumerate(brown_regions):
    print(f"  [{i}] x={r['x']}, y={r['y']}, w={r['w']}, h={r['h']}, area={r['area']}")

dark_green_regions = find_color_regions(img, hsv, 'dark_green', (35, 20, 30), (85, 80, 90), 500)
print(f"\nDark green zones (装备保障区): {len(dark_green_regions)}")
for i, r in enumerate(dark_green_regions):
    print(f"  [{i}] x={r['x']}, y={r['y']}, w={r['w']}, h={r['h']}, area={r['area']}")

red_regions = find_color_regions(img, hsv, 'red_low', (0, 50, 50), (12, 255, 255), 500)
red2 = find_color_regions(img, hsv, 'red_high', (160, 50, 50), (180, 255, 255), 500)
red_regions.extend(red2)
print(f"\nRed zones (部件检修区): {len(red_regions)}")
for i, r in enumerate(red_regions):
    print(f"  [{i}] x={r['x']}, y={r['y']}, w={r['w']}, h={r['h']}, area={r['area']}")

orange_regions = find_color_regions(img, hsv, 'orange', (10, 80, 80), (22, 255, 255), 500)
print(f"\nOrange zones (缓车区/天车): {len(orange_regions)}")
for i, r in enumerate(orange_regions):
    print(f"  [{i}] x={r['x']}, y={r['y']}, w={r['w']}, h={r['h']}, area={r['area']}")

yellow_regions = find_color_regions(img, hsv, 'yellow', (22, 80, 80), (35, 255, 255), 300)
print(f"\nYellow zones (天车): {len(yellow_regions)}")
for i, r in enumerate(yellow_regions):
    print(f"  [{i}] x={r['x']}, y={r['y']}, w={r['w']}, h={r['h']}, area={r['area']}")

purple_regions = find_color_regions(img, hsv, 'purple', (125, 30, 30), (155, 255, 255), 500)
print(f"\nPurple zones (轮对区): {len(purple_regions)}")
for i, r in enumerate(purple_regions):
    print(f"  [{i}] x={r['x']}, y={r['y']}, w={r['w']}, h={r['h']}, area={r['area']}")

blue_regions = find_color_regions(img, hsv, 'blue', (95, 40, 40), (130, 255, 255), 500)
print(f"\nBlue zones (转向架区): {len(blue_regions)}")
for i, r in enumerate(blue_regions):
    print(f"  [{i}] x={r['x']}, y={r['y']}, w={r['w']}, h={r['h']}, area={r['area']}")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 150)
lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=80, minLineLength=80, maxLineGap=15)

h_lines = []
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        angle = abs(np.arctan2(y2-y1, x2-x1) * 180 / np.pi)
        length = np.sqrt((x2-x1)**2 + (y2-y1)**2)
        if length < 100 or angle > 15:
            continue
        h_lines.append({'y': int((y1+y2)/2), 'x1': min(x1,x2), 'x2': max(x1,x2), 'length': round(length,1)})

h_lines.sort(key=lambda l: l['y'])
merged_h = []
for line in h_lines:
    if not merged_h or abs(line['y'] - merged_h[-1]['y']) > 8:
        merged_h.append(line)
    else:
        merged_h[-1]['x1'] = min(merged_h[-1]['x1'], line['x1'])
        merged_h[-1]['x2'] = max(merged_h[-1]['x2'], line['x2'])

print(f"\nHorizontal track lines: {len(merged_h)}")
for i, l in enumerate(merged_h):
    print(f"  [{i}] y={l['y']}, x={l['x1']}-{l['x2']}, len={l['x2']-l['x1']}")

print("\n" + "=" * 70)
print("BOGIE LAYOUT: bogie_frame_000_t0.0s.jpg")
print("=" * 70)

fp2 = os.path.join(FRAME_DIR, 'bogie_frame_000_t0.0s.jpg')
img2 = safe_imread(fp2)
h2, w2 = img2.shape[:2]
print(f"Image size: {w2}x{h2}")

hsv2 = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)

green2 = find_color_regions(img2, hsv2, 'green', (35, 40, 40), (85, 255, 255), 500)
print(f"\nGreen zones (部件检修缓存区): {len(green2)}")
for i, r in enumerate(green2):
    print(f"  [{i}] x={r['x']}, y={r['y']}, w={r['w']}, h={r['h']}, area={r['area']}")

orange2 = find_color_regions(img2, hsv2, 'orange', (10, 80, 80), (22, 255, 255), 500)
print(f"\nOrange zones (落车/称重区): {len(orange2)}")
for i, r in enumerate(orange2):
    print(f"  [{i}] x={r['x']}, y={r['y']}, w={r['w']}, h={r['h']}, area={r['area']}")

blue2 = find_color_regions(img2, hsv2, 'blue', (95, 40, 40), (130, 255, 255), 200)
print(f"\nBlue zones (工位): {len(blue2)}")
for i, r in enumerate(blue2):
    print(f"  [{i}] x={r['x']}, y={r['y']}, w={r['w']}, h={r['h']}, area={r['area']}")

red2_b = find_color_regions(img2, hsv2, 'red_low', (0, 50, 50), (12, 255, 255), 200)
red2_h = find_color_regions(img2, hsv2, 'red_high', (160, 50, 50), (180, 255, 255), 200)
red2_b.extend(red2_h)
print(f"\nRed zones (检修工位): {len(red2_b)}")
for i, r in enumerate(red2_b):
    print(f"  [{i}] x={r['x']}, y={r['y']}, w={r['w']}, h={r['h']}, area={r['area']}")

purple2 = find_color_regions(img2, hsv2, 'purple', (125, 30, 30), (155, 255, 255), 200)
print(f"\nPurple zones (缓存区): {len(purple2)}")
for i, r in enumerate(purple2):
    print(f"  [{i}] x={r['x']}, y={r['y']}, w={r['w']}, h={r['h']}, area={r['area']}")

yellow2 = find_color_regions(img2, hsv2, 'yellow', (22, 80, 80), (38, 255, 255), 300)
print(f"\nYellow zones (轴承间): {len(yellow2)}")
for i, r in enumerate(yellow2):
    print(f"  [{i}] x={r['x']}, y={r['y']}, w={r['w']}, h={r['h']}, area={r['area']}")

green_dark2 = find_color_regions(img2, hsv2, 'dark_green', (35, 20, 30), (85, 80, 90), 200)
print(f"\nDark green zones (成品转向架): {len(green_dark2)}")
for i, r in enumerate(green_dark2):
    print(f"  [{i}] x={r['x']}, y={r['y']}, w={r['w']}, h={r['h']}, area={r['area']}")

gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
edges2 = cv2.Canny(gray2, 50, 150)
lines2 = cv2.HoughLinesP(edges2, 1, np.pi/180, threshold=80, minLineLength=80, maxLineGap=15)

h_lines2 = []
if lines2 is not None:
    for line in lines2:
        x1, y1, x2, y2 = line[0]
        angle = abs(np.arctan2(y2-y1, x2-x1) * 180 / np.pi)
        length = np.sqrt((x2-x1)**2 + (y2-y1)**2)
        if length < 100 or angle > 15:
            continue
        h_lines2.append({'y': int((y1+y2)/2), 'x1': min(x1,x2), 'x2': max(x1,x2), 'length': round(length,1)})

h_lines2.sort(key=lambda l: l['y'])
merged_h2 = []
for line in h_lines2:
    if not merged_h2 or abs(line['y'] - merged_h2[-1]['y']) > 8:
        merged_h2.append(line)
    else:
        merged_h2[-1]['x1'] = min(merged_h2[-1]['x1'], line['x1'])
        merged_h2[-1]['x2'] = max(merged_h2[-1]['x2'], line['x2'])

print(f"\nHorizontal lines: {len(merged_h2)}")
for i, l in enumerate(merged_h2):
    print(f"  [{i}] y={l['y']}, x={l['x1']}-{l['x2']}")

annotated = img.copy()
for i, r in enumerate(green_regions):
    cv2.rectangle(annotated, (r['x'],r['y']), (r['x']+r['w'],r['y']+r['h']), (0,255,0), 2)
    cv2.putText(annotated, f"green{i}", (r['x'],r['y']-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
for i, r in enumerate(brown_regions):
    cv2.rectangle(annotated, (r['x'],r['y']), (r['x']+r['w'],r['y']+r['h']), (0,128,255), 2)
    cv2.putText(annotated, f"brown{i}", (r['x'],r['y']-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,128,255), 1)
for i, r in enumerate(orange_regions):
    cv2.rectangle(annotated, (r['x'],r['y']), (r['x']+r['w'],r['y']+r['h']), (0,165,255), 2)
    cv2.putText(annotated, f"orange{i}", (r['x'],r['y']-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,165,255), 1)
for i, r in enumerate(purple_regions):
    cv2.rectangle(annotated, (r['x'],r['y']), (r['x']+r['w'],r['y']+r['h']), (255,0,255), 2)
    cv2.putText(annotated, f"purple{i}", (r['x'],r['y']-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,255), 1)
for i, r in enumerate(blue_regions):
    cv2.rectangle(annotated, (r['x'],r['y']), (r['x']+r['w'],r['y']+r['h']), (255,0,0), 2)
    cv2.putText(annotated, f"blue{i}", (r['x'],r['y']-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1)
for l in merged_h:
    cv2.line(annotated, (l['x1'],l['y']), (l['x2'],l['y']), (255,255,0), 2)

cv2.imwrite(os.path.join(OUT_DIR, 'factory_precise.jpg'), annotated)

annotated2 = img2.copy()
for i, r in enumerate(orange2):
    cv2.rectangle(annotated2, (r['x'],r['y']), (r['x']+r['w'],r['y']+r['h']), (0,165,255), 2)
for i, r in enumerate(green2):
    cv2.rectangle(annotated2, (r['x'],r['y']), (r['x']+r['w'],r['y']+r['h']), (0,255,0), 2)
for i, r in enumerate(blue2):
    cv2.rectangle(annotated2, (r['x'],r['y']), (r['x']+r['w'],r['y']+r['h']), (255,0,0), 2)
for i, r in enumerate(red2_b):
    cv2.rectangle(annotated2, (r['x'],r['y']), (r['x']+r['w'],r['y']+r['h']), (0,0,255), 2)
for i, r in enumerate(purple2):
    cv2.rectangle(annotated2, (r['x'],r['y']), (r['x']+r['w'],r['y']+r['h']), (255,0,255), 2)
for i, r in enumerate(yellow2):
    cv2.rectangle(annotated2, (r['x'],r['y']), (r['x']+r['w'],r['y']+r['h']), (0,255,255), 2)

cv2.imwrite(os.path.join(OUT_DIR, 'bogie_precise.jpg'), annotated2)

print("\nAnnotated images saved to video_analysis/")
shutil.rmtree(TEMP_DIR, ignore_errors=True)
