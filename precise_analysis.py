import cv2
import numpy as np
import json
import os
import shutil
import tempfile

FRAME_DIR = r'f:\自开发程序\工厂建模\video_frames'
OUT_DIR = r'f:\自开发程序\工厂建模\video_analysis'
TEMP_DIR = tempfile.mkdtemp()

os.makedirs(OUT_DIR, exist_ok=True)

def copy_to_temp(src_path):
    name = os.path.basename(src_path)
    dst = os.path.join(TEMP_DIR, name)
    with open(src_path, 'rb') as f:
        data = f.read()
    with open(dst, 'wb') as f:
        f.write(data)
    return dst

def safe_imread(src_path):
    tmp = copy_to_temp(src_path)
    img = cv2.imread(tmp)
    os.remove(tmp)
    return img

def extract_regions(frame_path, prefix):
    img = safe_imread(frame_path)
    if img is None:
        print(f"Cannot read {frame_path}")
        return None
    h, w = img.shape[:2]
    print(f"\n=== {os.path.basename(frame_path)} ({w}x{h}) ===")
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    color_ranges = {
        'green': [(35, 40, 40), (85, 255, 255)],
        'yellow': [(18, 80, 80), (35, 255, 255)],
        'orange': [(10, 100, 100), (20, 255, 255)],
        'red_low': [(0, 50, 50), (10, 255, 255)],
        'red_high': [(160, 50, 50), (180, 255, 255)],
        'blue': [(100, 40, 40), (130, 255, 255)],
        'purple': [(130, 30, 30), (160, 255, 255)],
        'teal': [(85, 30, 30), (100, 255, 255)],
        'brown': [(10, 30, 50), (20, 150, 180)],
        'dark_green': [(35, 30, 30), (85, 100, 100)],
    }
    
    results = {}
    annotated = img.copy()
    
    for color_name, (lower, upper) in color_ranges.items():
        mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
        kernel = np.ones((5,5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < 500:
                continue
            x, y, rw, rh = cv2.boundingRect(cnt)
            roi = img[y:y+rh, x:x+rw]
            avg_color = cv2.mean(roi)[:3]
            
            results.setdefault(color_name, []).append({
                'x': int(x), 'y': int(y), 'w': int(rw), 'h': int(rh),
                'area': int(area),
                'avg_bgr': [int(avg_color[0]), int(avg_color[1]), int(avg_color[2])]
            })
            
            cv2.rectangle(annotated, (x, y), (x+rw, y+rh), (0, 255, 0), 2)
            cv2.putText(annotated, f"{color_name} {rw}x{rh}", (x, y-5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=80, minLineLength=100, maxLineGap=20)
    
    h_lines = []
    v_lines = []
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            angle = abs(np.arctan2(y2-y1, x2-x1) * 180 / np.pi)
            length = np.sqrt((x2-x1)**2 + (y2-y1)**2)
            if length < 80:
                continue
            if angle < 10:
                h_lines.append({'x1': int(x1), 'y1': int(y1), 'x2': int(x2), 'y2': int(y2), 'length': round(length,1)})
                cv2.line(annotated, (x1,y1), (x2,y2), (255,0,0), 2)
            elif angle > 80:
                v_lines.append({'x1': int(x1), 'y1': int(y1), 'x2': int(x2), 'y2': int(y2), 'length': round(length,1)})
                cv2.line(annotated, (x1,y1), (x2,y2), (0,0,255), 2)
    
    h_lines.sort(key=lambda l: l['y1'])
    v_lines.sort(key=lambda l: l['x1'])
    
    print(f"  Regions: {', '.join(f'{k}({len(v)})' for k,v in results.items())}")
    print(f"  Horizontal lines: {len(h_lines)}")
    print(f"  Vertical lines: {len(v_lines)}")
    
    out_path = os.path.join(OUT_DIR, f'{prefix}_analysis.jpg')
    cv2.imwrite(out_path, annotated)
    print(f"  Saved annotated: {out_path}")
    
    return {
        'image_size': [w, h],
        'regions': results,
        'h_lines': h_lines,
        'v_lines': v_lines
    }

factory_frames = [
    os.path.join(FRAME_DIR, 'factory_frame_000_t0.0s.jpg.jpg'),
    os.path.join(FRAME_DIR, 'factory_frame_010_t30.0s.jpg'),
    os.path.join(FRAME_DIR, 'factory_frame_020_t60.0s.jpg'),
    os.path.join(FRAME_DIR, 'factory_frame_030_t90.0s.jpg'),
    os.path.join(FRAME_DIR, 'factory_frame_043_t129.0s.jpg'),
]

bogie_frames = [
    os.path.join(FRAME_DIR, 'bogie_frame_000_t0.0s.jpg'),
    os.path.join(FRAME_DIR, 'bogie_frame_005_t10.0s.jpg'),
    os.path.join(FRAME_DIR, 'bogie_frame_010_t20.0s.jpg'),
    os.path.join(FRAME_DIR, 'bogie_frame_015_t30.0s.jpg'),
]

print("=" * 60)
print("FACTORY VIDEO FRAMES ANALYSIS")
print("=" * 60)

all_factory = {}
for fp in factory_frames:
    if os.path.exists(fp):
        result = extract_regions(fp, os.path.basename(fp).split('.')[0])
        if result:
            all_factory[os.path.basename(fp)] = result

print("\n" + "=" * 60)
print("BOGIE VIDEO FRAMES ANALYSIS")
print("=" * 60)

all_bogie = {}
for fp in bogie_frames:
    if os.path.exists(fp):
        result = extract_regions(fp, os.path.basename(fp).split('.')[0])
        if result:
            all_bogie[os.path.basename(fp)] = result

with open(os.path.join(OUT_DIR, 'factory_analysis.json'), 'w', encoding='utf-8') as f:
    json.dump(all_factory, f, ensure_ascii=False, indent=2)

with open(os.path.join(OUT_DIR, 'bogie_analysis.json'), 'w', encoding='utf-8') as f:
    json.dump(all_bogie, f, ensure_ascii=False, indent=2)

shutil.rmtree(TEMP_DIR, ignore_errors=True)
print("\n\nAnalysis complete. Results saved to video_analysis/")
