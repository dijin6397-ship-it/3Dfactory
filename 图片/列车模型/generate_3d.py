import cv2
import numpy as np
from PIL import Image
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def estimate_depth_map(img_gray):
    h, w = img_gray.shape
    grad_x = cv2.Sobel(img_gray, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(img_gray, cv2.CV_64F, 0, 1, ksize=3)
    gradient_mag = np.sqrt(grad_x**2 + grad_y**2)
    gradient_mag = cv2.GaussianBlur(gradient_mag, (5, 5), 0)
    
    depth = np.zeros_like(img_gray, dtype=np.float64)
    center_x, center_y = w // 2, h // 2
    
    Y, X = np.mgrid[0:h, 0:w]
    dist_from_center = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
    dist_norm = dist_from_center / dist_from_center.max()
    
    img_norm = img_gray.astype(np.float64) / 255.0
    depth = (1.0 - img_norm) * 0.6 + (1.0 - dist_norm) * 0.3 + (gradient_mag / gradient_mag.max()) * 0.1
    
    depth = cv2.GaussianBlur(depth, (7, 7), 0)
    depth = (depth - depth.min()) / (depth.max() - depth.min())
    
    return depth

def render_3d_model(img_rgb, depth_map, elevation, azimuth, save_path, title=""):
    h, w = depth_map.shape
    
    step = max(2, min(h, w) // 100)
    
    X = np.arange(0, w, step)
    Y = np.arange(0, h, step)
    X, Y = np.meshgrid(X, Y)
    
    Z = depth_map[::step, ::step] * 100
    
    colors = img_rgb[::step, ::step, :].astype(np.float64) / 255.0
    colors_flat = colors.reshape(-1, 3)
    
    fig = plt.figure(figsize=(12, 9), dpi=100, facecolor='white')
    ax = fig.add_subplot(111, projection='3d')
    
    surf = ax.plot_surface(X, -Y, Z, facecolors=colors, 
                          rstride=1, cstride=1, shade=True, 
                          antialiased=True, alpha=0.95)
    
    ax.set_xlim(0, w)
    ax.set_ylim(-h, 0)
    ax.set_zlim(0, 100)
    
    ax.view_init(elev=elevation, azim=azimuth)
    
    ax.set_xlabel('X', fontsize=8)
    ax.set_ylabel('Y', fontsize=8)
    ax.set_zlabel('Z', fontsize=8)
    ax.set_title(title, fontsize=12, fontweight='bold')
    
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('lightgray')
    ax.yaxis.pane.set_edgecolor('lightgray')
    ax.zaxis.pane.set_edgecolor('lightgray')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_path, bbox_inches='tight', dpi=100, 
                facecolor='white', edgecolor='none')
    plt.close(fig)

def render_multi_views(img_rgb, depth_map, save_dir, train_name):
    views = [
        (25, -60, f"{train_name}_front"),
        (25, 30, f"{train_name}_side"),
        (45, -30, f"{train_name}_top"),
        (15, -120, f"{train_name}_perspective"),
    ]
    
    for elev, azim, name in views:
        save_path = os.path.join(save_dir, f"{name}.png")
        render_3d_model(img_rgb, depth_map, elev, azim, save_path, title=name)

input_dir = r'F:\自开发程序\工厂建模\图片\列车模型\列车剪切'
output_dir = r'F:\自开发程序\工厂建模\图片\列车模型\列车3D模型'
os.makedirs(output_dir, exist_ok=True)

for i in range(1, 9):
    input_path = os.path.join(input_dir, f'列车_{i}.png')
    if not os.path.exists(input_path):
        print(f"跳过列车_{i}: 文件不存在")
        continue
    
    img_pil = Image.open(input_path).convert('RGB')
    img_rgb = np.array(img_pil)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    
    print(f"处理列车_{i}: {img_rgb.shape[1]}x{img_rgb.shape[0]}...")
    
    depth = estimate_depth_map(img_gray)
    
    train_output_dir = os.path.join(output_dir, f'列车_{i}')
    os.makedirs(train_output_dir, exist_ok=True)
    
    cv2.imwrite(os.path.join(train_output_dir, 'depth_map.png'), 
                (depth * 255).astype(np.uint8))
    
    render_multi_views(img_rgb, depth, train_output_dir, f'列车_{i}')
    
    print(f"  已生成4个视角的3D效果图")

print("\n所有列车3D模型效果图生成完成!")
print(f"输出目录: {output_dir}")
