#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""用 PIL 生成 PWA 图标：渐变紫底 + 白色圆角卡 + 书本 + “60 外刊阅读”"""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = "/Users/tea/WorkBuddy/2026-08-09-23-35-37/app/icons"
os.makedirs(OUT, exist_ok=True)

# 字体候选
FONT_CANDIDATES = {
    "bold": [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    ],
    "cn": [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/Supplemental/Songti.ttc",
    ],
}
def load_font(kind, size, index=0):
    for p in FONT_CANDIDATES.get(kind, []):
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size, index=index)
            except Exception:
                try:
                    return ImageFont.truetype(p, size)
                except Exception:
                    continue
    return ImageFont.load_default()

def draw_icon(size, maskable=False):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # 对角渐变
    c1 = (90, 74, 138); c2 = (154, 138, 200)   # #5a4a8a → #9a8ac8
    for y in range(size):
        t = y / (size - 1)
        r = int(c1[0] + (c2[0] - c1[0]) * t)
        g = int(c1[1] + (c2[1] - c1[1]) * t)
        b = int(c1[2] + (c2[2] - c1[2]) * t)
        d.line([(0, y), (size, y)], fill=(r, g, b, 255))
    # 底部微光
    glow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([-size * 0.15, size * 0.62, size * 1.15, size * 1.4], fill=(255, 255, 255, 46))
    img = Image.alpha_composite(img, glow)
    d = ImageDraw.Draw(img)

    if maskable:
        # 安全区：内容缩至中间 80%
        area = (size * 0.10, size * 0.10, size * 0.90, size * 0.90)
    else:
        area = (0, 0, size, size)

    # 白色圆角卡片（中心）
    pad = size * 0.13
    card = [area[0] + pad, area[1] + pad, area[2] - pad, area[3] - pad]
    radius = size * 0.11
    # 阴影
    sh = [card[0] + size * 0.008, card[1] + size * 0.012, card[2] + size * 0.008, card[3] + size * 0.012]
    d.rounded_rectangle(sh, radius=radius, fill=(70, 45, 130, 90))
    d.rounded_rectangle(card, radius=radius, fill=(255, 255, 255, 255))

    # 书本图形（两页 + 书脊）
    ink = (90, 74, 138)
    book_w = size * 0.42
    book_h = size * 0.28
    bx = (card[0] + card[2]) / 2
    top = card[1] + size * 0.10
    left_page = [bx - book_w / 2, top, bx, top + book_h]
    right_page = [bx, top, bx + book_w / 2, top + book_h]
    lr = size * 0.035
    d.rounded_rectangle(left_page, radius=lr, fill=ink)
    d.rounded_rectangle(right_page, radius=lr, fill=ink)
    # 书页线
    d.line([(bx, top + size * 0.018), (bx, top + book_h - size * 0.018)], fill=(255, 255, 255, 255), width=max(2, int(size * 0.012)))
    # 左页横线
    for i in range(2):
        ly = top + book_h * (0.32 + i * 0.22)
        d.line([(bx - book_w / 2 + size * 0.05, ly), (bx - size * 0.035, ly)], fill=(255, 255, 255, 200), width=max(1, int(size * 0.008)))

    # 文字 “60 外刊阅读”
    txt_y = top + book_h + size * 0.075
    f60 = load_font("bold", int(size * 0.155), index=1)
    fcn = load_font("cn", int(size * 0.075), index=1)
    s60 = "60"
    s_cn = "外刊阅读"
    # 测量居中
    b60 = d.textbbox((0, 0), s60, font=f60)
    w60 = b60[2] - b60[0]
    bcn = d.textbbox((0, 0), s_cn, font=fcn)
    wcn = bcn[2] - bcn[0]
    # 60 加粗字重（画两次偏移模拟粗体）
    for dx in (-1, 1):
        d.text((bx - w60 / 2 + dx, txt_y - b60[1]), s60, font=f60, fill=ink)
    d.text((bx - w60 / 2, txt_y - b60[1]), s60, font=f60, fill=ink)
    y2 = txt_y + size * 0.155
    for dx in (-1, 1):
        d.text((bx - wcn / 2 + dx, y2 - bcn[1]), s_cn, font=fcn, fill=ink)
    d.text((bx - wcn / 2, y2 - bcn[1]), s_cn, font=fcn, fill=ink)

    # 顶部小高光
    hi = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    hd = ImageDraw.Draw(hi)
    hd.ellipse([-size * 0.2, -size * 0.35, size * 0.9, size * 0.5], fill=(255, 255, 255, 40))
    img = Image.alpha_composite(img, hi)
    return img.convert("RGB")

for size in (180, 192, 512):
    draw_icon(size).save(os.path.join(OUT, f"icon-{size}.png"), "PNG")
draw_icon(512, maskable=True).save(os.path.join(OUT, "icon-maskable-512.png"), "PNG")
print("icons done:", os.listdir(OUT))
