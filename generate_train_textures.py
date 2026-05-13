from PIL import Image, ImageDraw, ImageFont
import os

def create_train_texture(car_number, output_path):
    width, height = 512, 256
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    colors = [(33, 150, 243), (229, 57, 53), (67, 160, 71), (251, 140, 0), (142, 36, 170), (0, 172, 193), (216, 27, 96), (0, 137, 123)]
    main_color = colors[(car_number - 1) % 8]
    bl, br, bt, bb = 20, 492, 60, 200
    for i in range(5):
        draw.rounded_rectangle([bl+5-i, bt+5-i, br+5-i, bb+5-i], radius=15, fill=(0,0,0,40+i*10))
    draw.rounded_rectangle([bl, bt, br, bb], radius=15, fill=main_color)
    for y in range(bt, bt+(bb-bt)//3):
        draw.line([(bl+15,y),(br-15,y)], fill=(255,255,255,int(60*(1-(y-bt)/((bb-bt)//3)))), width=1)
    for y in range(bb-(bb-bt)//4, bb):
        draw.line([(bl+15,y),(br-15,y)], fill=(0,0,0,int(40*(y-(bb-(bb-bt)//4))/((bb-bt)//4))), width=1)
    draw.rounded_rectangle([bl+10, bt-15, br-10, bt+5], radius=8, fill=(180,180,190))
    for y in range(bt-15, bt-7):
        draw.line([(bl+20,y),(br-20,y)], fill=(255,255,255,int(80*(1-(y-bt+15)/8))), width=1)
    for i in range(7):
        wx = bl+50+i*55
        wy = bt+30
        draw.rounded_rectangle([wx-2, wy-2, wx+37, wy+47], radius=6, fill=(100,100,110))
        draw.rounded_rectangle([wx, wy, wx+35, wy+45], radius=5, fill=(38,50,56,220))
        draw.line([(wx+5,wy+5),(wx+15,wy+5)], fill=(255,255,255,80), width=2)
    for dx in [bl+180, br-220]:
        dy = bt+20
        draw.rounded_rectangle([dx-3, dy-3, dx+43, dy+83], radius=5, fill=(80,80,90))
        draw.rounded_rectangle([dx, dy, dx+40, dy+80], radius=4, fill=(120,120,130))
        draw.line([(dx+20, dy+5),(dx+20, dy+75)], fill=(90,90,100), width=2)
        draw.ellipse([dx+25, dy+37, dx+31, dy+43], fill=(200,200,210))
    draw.rounded_rectangle([bl+5, bt+100, br-5, bt+108], radius=4, fill=(255,255,255,180))
    try:
        fl = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 72)
        fs = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 24)
    except:
        fl = ImageFont.load_default()
        fs = ImageFont.load_default()
    cx, cy, cr = 256, bt+135, 38
    draw.ellipse([cx-cr+3, cy-cr+3, cx+cr+3, cy+cr+3], fill=(0,0,0,60))
    draw.ellipse([cx-cr, cy-cr, cx+cr, cy+cr], fill=(255,255,255,230))
    draw.ellipse([cx-cr, cy-cr, cx+cr, cy+cr], outline=main_color, width=3)
    nt = str(car_number)
    bb2 = draw.textbbox((0,0), nt, font=fl)
    tw, th = bb2[2]-bb2[0], bb2[3]-bb2[1]
    tx, ty = cx-tw//2, cy-th//2-5
    draw.text((tx+2, ty+2), nt, fill=(0,0,0,80), font=fl)
    draw.text((tx, ty), nt, fill=main_color, font=fl)
    draw.rounded_rectangle([bl+15, bb, br-15, bb+20], radius=5, fill=(60,60,70))
    for bx in [bl+60, br-60]:
        draw.rounded_rectangle([bx-30, bb+5, bx+30, bb+25], radius=5, fill=(50,50,60))
        for wo in [-15, 15]:
            wx2 = bx+wo
            wy2 = bb+30
            draw.ellipse([wx2-16, wy2-16, wx2+20, wy2+20], fill=(0,0,0,50))
            draw.ellipse([wx2-18, wy2-18, wx2+18, wy2+18], fill=(40,40,50))
            draw.ellipse([wx2-15, wy2-15, wx2+15, wy2+15], fill=(70,70,80))
            draw.ellipse([wx2-5, wy2-5, wx2+5, wy2+5], fill=(90,90,100))
    for hx, hy, c in [(bl+5, bt+40, (255,241,118)), (bl+5, bb-40, (255,23,68))]:
        for r in range(12, 0, -1):
            draw.ellipse([hx-r, hy-r, hx+r, hy+r], fill=(*c, int(100*(1-r/12))))
        draw.ellipse([hx-6, hy-6, hx+6, hy+6], fill=c)
    label = str(car_number)+"车"
    bb3 = draw.textbbox((0,0), label, font=fs)
    lw = bb3[2]-bb3[0]
    lx = (width-lw)//2
    ly = height-30
    draw.rounded_rectangle([lx-8, ly-4, lx+lw+8, ly+24], radius=8, fill=(0,0,0,120))
    draw.text((lx, ly), label, fill=(255,255,255,220), font=fs)
    rgb = Image.new("RGB", (width, height), (240,240,240))
    rgb.paste(img, mask=img.split()[3])
    rgb.save(output_path, "JPEG", quality=95)
    print(f"Generated: {output_path}")

output_dir = "F:/自开发程序/工厂建模/图片"
os.makedirs(output_dir, exist_ok=True)
for i in range(1, 9):
    create_train_texture(i, os.path.join(output_dir, f"{i}车.jpg"))
print("Done!")
