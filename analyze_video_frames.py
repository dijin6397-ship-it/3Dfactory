import cv2
import numpy as np
import os
import json

FRAMES_DIR = r"F:\自开发程序\工厂建模\video_frames"
OUTPUT_DIR = r"F:\自开发程序\工厂建模\video_analysis"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_img(fname):
    fpath = os.path.join(FRAMES_DIR, fname)
    data = open(fpath, 'rb').read()
    return cv2.imdecode(np.frombuffer(data, dtype=np.uint8), cv2.IMREAD_COLOR)

def detect_horizontal_lines(gray, min_length_px=100):
    edges = cv2.Canny(gray, 50, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 80, minLineLength=min_length_px, maxLineGap=10)
    if lines is None:
        return []
    h_lines = []
    for l in lines:
        x1, y1, x2, y2 = l[0]
        angle = abs(np.arctan2(y2 - y1, x2 - x1))
        if angle < 0.15:
            length = abs(x2 - x1)
            h_lines.append({'y': (y1 + y2) / 2, 'x1': min(x1, x2), 'x2': max(x1, x2), 'length': length})
    h_lines.sort(key=lambda l: l['y'])
    return h_lines

def cluster_y(lines, tolerance=15):
    if not lines:
        return []
    clusters = []
    current = [lines[0]]
    for l in lines[1:]:
        if abs(l['y'] - current[-1]['y']) < tolerance:
            current.append(l)
        else:
            avg_y = sum(c['y'] for c in current) / len(current)
            max_len = max(c['length'] for c in current)
            min_x = min(c['x1'] for c in current)
            max_x = max(c['x2'] for c in current)
            clusters.append({'y': avg_y, 'count': len(current), 'max_length': max_len, 'x_range': (min_x, max_x)})
            current = [l]
    if current:
        avg_y = sum(c['y'] for c in current) / len(current)
        max_len = max(c['length'] for c in current)
        min_x = min(c['x1'] for c in current)
        max_x = max(c['x2'] for c in current)
        clusters.append({'y': avg_y, 'count': len(current), 'max_length': max_len, 'x_range': (min_x, max_x)})
    return clusters

print("=" * 70)
print("FACTORY LAYOUT ANALYSIS")
print("=" * 70)

img = load_img("factory_frame_000_t0.0s.jpg.jpg")
h, w = img.shape[:2]
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

h_lines = detect_horizontal_lines(gray, 200)
track_clusters = cluster_y(h_lines, 12)
long_tracks = [c for c in track_clusters if c['max_length'] > w * 0.3]

print(f"\nImage size: {w}x{h}")
print(f"Horizontal lines found: {len(h_lines)}")
print(f"Line clusters (y-proximity): {len(track_clusters)}")
print(f"Long tracks (>30% width): {len(long_tracks)}")
for i, t in enumerate(long_tracks):
    print(f"  Track {i+1}: y={t['y']:.0f}, len={t['max_length']:.0f}px, x=[{t['x_range'][0]:.0f}-{t['x_range'][1]:.0f}]")

mask_blue = cv2.inRange(hsv, (100, 50, 50), (130, 255, 255))
contours_b, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
big_blue = sorted([c for c in contours_b if cv2.contourArea(c) > 2000], key=lambda c: cv2.contourArea(c), reverse=True)
print(f"\nBlue regions (>2000px): {len(big_blue)}")
for i, c in enumerate(big_blue[:20]):
    x, y, bw, bh = cv2.boundingRect(c)
    area = cv2.contourArea(c)
    print(f"  Blue {i+1}: pos=({x},{y}) size={bw}x{bh} area={area}")

mask_yellow = cv2.inRange(hsv, (20, 50, 50), (35, 255, 255))
contours_y, _ = cv2.findContours(mask_yellow, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
big_yellow = sorted([c for c in contours_y if cv2.contourArea(c) > 2000], key=lambda c: cv2.contourArea(c), reverse=True)
print(f"\nYellow regions (>2000px): {len(big_yellow)}")
for i, c in enumerate(big_yellow[:20]):
    x, y, yw, yh = cv2.boundingRect(c)
    area = cv2.contourArea(c)
    print(f"  Yellow {i+1}: pos=({x},{y}) size={yw}x{yh} area={area}")

mask_green = cv2.inRange(hsv, (35, 50, 50), (85, 255, 255))
contours_g, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
big_green = sorted([c for c in contours_g if cv2.contourArea(c) > 2000], key=lambda c: cv2.contourArea(c), reverse=True)
print(f"\nGreen regions (>2000px): {len(big_green)}")
for i, c in enumerate(big_green[:15]):
    x, y, gw, gh = cv2.boundingRect(c)
    area = cv2.contourArea(c)
    print(f"  Green {i+1}: pos=({x},{y}) size={gw}x{gh} area={area}")

mask_red = cv2.inRange(hsv, (0, 50, 50), (10, 255, 255)) | cv2.inRange(hsv, (170, 50, 50), (180, 255, 255))
contours_r, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
big_red = sorted([c for c in contours_r if cv2.contourArea(c) > 3000], key=lambda c: cv2.contourArea(c), reverse=True)
print(f"\nRed regions (>3000px): {len(big_red)}")
for i, c in enumerate(big_red[:20]):
    x, y, rw, rh = cv2.boundingRect(c)
    area = cv2.contourArea(c)
    ratio = rw / rh if rh > 0 else 0
    print(f"  Red {i+1}: pos=({x},{y}) size={rw}x{rh} ratio={ratio:.2f} area={area}")

annotated = img.copy()
for t in long_tracks:
    y_pos = int(t['y'])
    cv2.line(annotated, (0, y_pos), (w, y_pos), (0, 255, 0), 2)
for c in big_blue[:15]:
    x, y, bw, bh = cv2.boundingRect(c)
    cv2.rectangle(annotated, (x, y), (x + bw, y + bh), (255, 100, 0), 2)
for c in big_yellow[:10]:
    x, y, yw, yh = cv2.boundingRect(c)
    cv2.rectangle(annotated, (x, y), (x + yw, y + yh), (0, 255, 255), 2)

out_path = os.path.join(OUTPUT_DIR, "factory_annotated.jpg")
cv2.imwrite(out_path, annotated)
print(f"\nAnnotated image saved: {out_path}")

print("\n" + "=" * 70)
print("BOGIE AREA ANALYSIS")
print("=" * 70)

img_b = load_img("bogie_frame_000_t0.0s.jpg")
h_b, w_b = img_b.shape[:2]
gray_b = cv2.cvtColor(img_b, cv2.COLOR_BGR2GRAY)
hsv_b = cv2.cvtColor(img_b, cv2.COLOR_BGR2HSV)

h_lines_b = detect_horizontal_lines(gray_b, 150)
track_clusters_b = cluster_y(h_lines_b, 12)
long_tracks_b = [c for c in track_clusters_b if c['max_length'] > w_b * 0.2]

print(f"\nImage size: {w_b}x{h_b}")
print(f"Long tracks (>20% width): {len(long_tracks_b)}")
for i, t in enumerate(long_tracks_b):
    print(f"  Track {i+1}: y={t['y']:.0f}, len={t['max_length']:.0f}px")

mask_blue_b = cv2.inRange(hsv_b, (100, 50, 50), (130, 255, 255))
contours_bb, _ = cv2.findContours(mask_blue_b, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
big_blue_b = sorted([c for c in contours_bb if cv2.contourArea(c) > 2000], key=lambda c: cv2.contourArea(c), reverse=True)
print(f"\nBlue regions (>2000px): {len(big_blue_b)}")
for i, c in enumerate(big_blue_b[:15]):
    x, y, bw, bh = cv2.boundingRect(c)
    area = cv2.contourArea(c)
    print(f"  Blue {i+1}: pos=({x},{y}) size={bw}x{bh} area={area}")

mask_yellow_b = cv2.inRange(hsv_b, (20, 50, 50), (35, 255, 255))
contours_yb, _ = cv2.findContours(mask_yellow_b, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
big_yellow_b = sorted([c for c in contours_yb if cv2.contourArea(c) > 2000], key=lambda c: cv2.contourArea(c), reverse=True)
print(f"\nYellow regions (>2000px): {len(big_yellow_b)}")
for i, c in enumerate(big_yellow_b[:10]):
    x, y, yw, yh = cv2.boundingRect(c)
    area = cv2.contourArea(c)
    print(f"  Yellow {i+1}: pos=({x},{y}) size={yw}x{yh} area={area}")

annotated_b = img_b.copy()
for t in long_tracks_b:
    y_pos = int(t['y'])
    cv2.line(annotated_b, (0, y_pos), (w_b, y_pos), (0, 255, 0), 2)
for c in big_blue_b[:15]:
    x, y, bw, bh = cv2.boundingRect(c)
    cv2.rectangle(annotated_b, (x, y), (x + bw, y + bh), (255, 100, 0), 2)
for c in big_yellow_b[:10]:
    x, y, yw, yh = cv2.boundingRect(c)
    cv2.rectangle(annotated_b, (x, y), (x + yw, y + yh), (0, 255, 255), 2)

out_path_b = os.path.join(OUTPUT_DIR, "bogie_annotated.jpg")
cv2.imwrite(out_path_b, annotated_b)
print(f"\nAnnotated bogie image saved: {out_path_b}")

print("\nDone!")
