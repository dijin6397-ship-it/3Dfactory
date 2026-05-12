import cv2
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE, "video_frames")

os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_frames(video_path, prefix, interval_sec=2):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"ERROR: Cannot open {video_path}")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total / fps if fps > 0 else 0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print(f"\n=== {prefix} ===")
    print(f"  Resolution: {width}x{height}")
    print(f"  FPS: {fps:.2f}")
    print(f"  Total frames: {total}")
    print(f"  Duration: {duration:.1f}s ({duration/60:.1f}min)")

    frame_interval = int(fps * interval_sec)
    count = 0
    saved = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if count % frame_interval == 0:
            timestamp = count / fps
            fname = f"{prefix}_frame_{saved:03d}_t{timestamp:.1f}s.jpg"
            out_path = os.path.join(OUTPUT_DIR, fname)
            cv2.imwrite(out_path, frame)
            saved += 1
            if saved <= 3 or saved % 10 == 0:
                print(f"  Saved: {fname}")
        count += 1

    cap.release()
    print(f"  Total saved: {saved} frames")
    return saved

print("Extracting frames from videos...")
n1 = extract_frames(os.path.join(BASE, "总体流程.mp4"), "factory", interval_sec=3)
n2 = extract_frames(os.path.join(BASE, "转向架.mp4"), "bogie", interval_sec=2)
print(f"\nDone! Factory: {n1} frames, Bogie: {n2} frames")
print(f"Output: {OUTPUT_DIR}")
