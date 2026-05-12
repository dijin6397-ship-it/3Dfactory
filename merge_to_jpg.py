"""
将 DXF 和 PDF 图纸合并为一张高清晰度 JPG 文件。
- DXF: 上海北翟路车辆段检修库厂房工艺布局局图2023.10.26终版-改压轮.dxf
- PDF: 上海北翟路车辆段检修库厂房布局图.pdf
"""
import os
import io
import fitz  # PyMuPDF
import ezdxf
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DXF_FILE = os.path.join(BASE_DIR, "上海北翟路车辆段检修库厂房工艺布局局图2023.10.26终版-改压轮.dxf")
PDF_FILE = os.path.join(BASE_DIR, "上海北翟路车辆段检修库厂房布局图.pdf")
OUTPUT_FILE = os.path.join(BASE_DIR, "合并图纸_上海北翟路车辆段检修库.jpg")

DPI = 300
GAP = 60
BG_COLOR = (255, 255, 255)


def render_dxf_to_image(dxf_path: str, dpi: int = 300) -> Image.Image:
    """将 DXF 文件渲染为 PIL Image (使用 matplotlib 后端)"""
    print(f"正在读取 DXF 文件: {os.path.basename(dxf_path)}")
    doc = ezdxf.readfile(dxf_path)
    msp = doc.modelspace()

    print("正在使用 matplotlib 渲染 DXF (可能需要几分钟)...")
    ctx = RenderContext(doc)

    # 创建足够大的 figure，宽幅比例
    fig = plt.figure(figsize=(24, 6), dpi=dpi)
    ax = fig.add_axes([0, 0, 1, 1])

    backend = MatplotlibBackend(ax)
    frontend = Frontend(ctx, backend)
    frontend.draw_layout(msp)

    ax.set_facecolor('white')
    ax.autoscale(enable=True)
    ax.set_aspect('equal')
    ax.axis('off')

    print("正在保存为 PNG...")
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=dpi, facecolor='white',
                bbox_inches='tight', pad_inches=0.1)
    plt.close(fig)
    buf.seek(0)

    img = Image.open(buf)
    print(f"DXF 渲染完成: {img.size[0]}x{img.size[1]}")
    return img


def render_pdf_to_image(pdf_path: str, dpi: int = 300) -> Image.Image:
    """将 PDF 文件渲染为 PIL Image"""
    print(f"正在读取 PDF 文件: {os.path.basename(pdf_path)}")
    doc = fitz.open(pdf_path)
    page = doc[0]

    zoom = dpi / 72.0
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)

    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    doc.close()
    print(f"PDF 渲染完成: {img.size[0]}x{img.size[1]}")
    return img


def combine_images(img1: Image.Image, img2: Image.Image, gap: int = 60) -> Image.Image:
    """将两张图片上下合并（PDF 在上，DXF 在下）"""
    # 统一宽度
    target_w = max(img1.width, img2.width)

    def resize_to_width(img, w):
        if img.width == w:
            return img
        ratio = w / img.width
        new_h = int(img.height * ratio)
        return img.resize((w, new_h), Image.LANCZOS)

    img1 = resize_to_width(img1, target_w)
    img2 = resize_to_width(img2, target_w)

    total_h = img1.height + gap + img2.height
    combined = Image.new("RGB", (target_w, total_h), BG_COLOR)
    combined.paste(img1, (0, 0))
    combined.paste(img2, (0, img1.height + gap))

    print(f"合并完成: {target_w}x{total_h}")
    return combined


def main():
    # 渲染 PDF（较快）
    pdf_img = render_pdf_to_image(PDF_FILE, DPI)

    # 渲染 DXF（较慢）
    dxf_img = render_dxf_to_image(DXF_FILE, DPI)

    # 合并
    combined = combine_images(pdf_img, dxf_img, GAP)

    # 保存为高质量 JPG
    combined.save(OUTPUT_FILE, "JPEG", quality=95, dpi=(DPI, DPI))
    file_size_mb = os.path.getsize(OUTPUT_FILE) / (1024 * 1024)
    print(f"\n输出文件: {OUTPUT_FILE}")
    print(f"文件大小: {file_size_mb:.1f} MB")
    print("完成!")


if __name__ == "__main__":
    main()
