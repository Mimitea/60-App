#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""零依赖生成 PWA 图标：渐变紫底 + 白色开本书本 + 金色书签。
纯标准库：手写 PNG 编码（zlib）+ 光栅绘制。"""
import os, struct, zlib

OUT = "/Users/tea/WorkBuddy/2026-08-09-23-35-37/app/icons"
os.makedirs(OUT, exist_ok=True)

def lerp(a, b, t):
    return a + (b - a) * t

def write_png(path, size, rgba):
    raw = b""
    for y in range(size):
        raw += b"\x00"
        for x in range(size):
            raw += bytes(rgba[y * size + x])
    def chunk(tag, data):
        c = struct.pack(">I", len(data)) + tag + data
        return c + struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff)
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(raw, 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)

def make_icon(size, maskable=False):
    px = [(0, 0, 0, 0)] * (size * size)
    c1 = (90, 74, 138)    # #5a4a8a
    c2 = (154, 138, 200)  # #9a8ac8
    accent = (245, 200, 66, 255)  # 金色书签 #F5C842

    def setpx(x, y, col):
        if 0 <= x < size and 0 <= y < size:
            base = px[y * size + x]
            if col[3] == 255:
                px[y * size + x] = col
            else:
                a = col[3] / 255
                br, bg, bb = base[0], base[1], base[2]
                nr = int(col[0] * a + br * (1 - a))
                ng = int(col[1] * a + bg * (1 - a))
                nb = int(col[2] * a + bb * (1 - a))
                px[y * size + x] = (nr, ng, nb, 255)

    def rounded_rect(x0, y0, x1, y1, rad, fill):
        x0c = max(0, int(x0)); x1c = min(size, int(x1))
        y0c = max(0, int(y0)); y1c = min(size, int(y1))
        for y in range(y0c, y1c):
            for x in range(x0c, x1c):
                if x < x0 + rad and y < y0 + rad:
                    dx, dy = x - (x0 + rad), y - (y0 + rad)
                    if dx * dx + dy * dy > rad * rad: continue
                elif x >= x1 - rad and y < y0 + rad:
                    dx, dy = x - (x1 - rad - 1), y - (y0 + rad)
                    if dx * dx + dy * dy > rad * rad: continue
                elif x < x0 + rad and y >= y1 - rad:
                    dx, dy = x - (x0 + rad), y - (y1 - rad - 1)
                    if dx * dx + dy * dy > rad * rad: continue
                elif x >= x1 - rad and y >= y1 - rad:
                    dx, dy = x - (x1 - rad - 1), y - (y1 - rad - 1)
                    if dx * dx + dy * dy > rad * rad: continue
                setpx(x, y, fill)

    # 1) 对角渐变背景
    for y in range(size):
        for x in range(size):
            t = (x + y) / (2 * (size - 1))
            r = int(lerp(c1[0], c2[0], t))
            g = int(lerp(c1[1], c2[1], t))
            b = int(lerp(c1[2], c2[2], t))
            px[y * size + x] = (r, g, b, 255)

    # 2) 左上柔光
    cx, cy = size * 0.28, -size * 0.12
    rx, ry = size * 0.78, size * 0.52
    for y in range(int(cy - ry), int(cy + ry) + 1):
        for x in range(int(cx - rx), int(cx + rx) + 1):
            if 0 <= x < size and 0 <= y < size:
                t = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
                if t <= 1:
                    a = int(55 * (1 - t))
                    setpx(x, y, (255, 255, 255, a))

    # 3) 安全区
    if maskable:
        x0, y0, x1, y1 = size * 0.08, size * 0.08, size * 0.92, size * 0.92
    else:
        x0, y0, x1, y1 = 0, 0, size, size

    # 4) 书本 — 占据中央 ~60%
    ink = (255, 255, 255, 255)
    bw = (x1 - x0) * 0.62
    bh = (y1 - y0) * 0.58
    bx = (x0 + x1) / 2
    by = (y0 + y1) / 2
    top = by - bh / 2
    page_thick = max(2, int(size * 0.012))
    brad = int(size * 0.04)
    # 左页
    lx0, lx1 = bx - bw / 2, bx - page_thick / 2
    rx0, rx1 = bx + page_thick / 2, bx + bw / 2
    rounded_rect(lx0, top, lx1, top + bh, brad, ink)
    rounded_rect(rx0, top, rx1, top + bh, brad, ink)
    # 书脊底 V 形（书本弧度）
    spine_y = top + bh - int(size * 0.005)
    for yy in range(int(top), int(spine_y)):
        # 越往下，书脊偏移使两页呈 V
        t = (yy - top) / (spine_y - top)
        offset = t * size * 0.025
        for xx in range(int(bx - offset), int(bx + offset + page_thick)):
            setpx(xx, yy, ink)
    # 左页文本线（3 条）
    lw = max(1, int(size * 0.011))
    for i in range(3):
        ly = top + bh * (0.18 + i * 0.22)
        for xx in range(int(lx0 + size * 0.045), int(bx - size * 0.05)):
            for yy in range(int(ly), int(ly + lw)):
                setpx(xx, yy, (c1[0], c1[1], c1[2], 230))
    # 右页文本线
    for i in range(3):
        ly = top + bh * (0.18 + i * 0.22)
        for xx in range(int(bx + size * 0.05), int(rx1 - size * 0.045)):
            for yy in range(int(ly), int(ly + lw)):
                setpx(xx, yy, (c1[0], c1[1], c1[2], 230))

    # 5) 金色书签丝带（右上页）
    bm_x = rx1 - size * 0.10
    bm_top = top - size * 0.06
    bm_w = size * 0.07
    bm_h = bh * 0.42
    # 矩形主体
    rounded_rect(bm_x, bm_top, bm_x + bm_w, bm_top + bm_h, int(size * 0.018), accent)
    # 底部 V 形切口
    notch_w = bm_w * 0.85
    for yy in range(int(bm_top + bm_h - bm_w * 0.3), int(bm_top + bm_h)):
        t = (yy - (bm_top + bm_h - bm_w * 0.3)) / max(1, bm_w * 0.3)
        half = (notch_w / 2) * t
        for xx in range(int(bm_x + bm_w / 2 - half), int(bm_x + bm_w / 2 + half)):
            if 0 <= xx < size:
                px[yy * size + xx] = (0, 0, 0, 0)

    return px

for size in (180, 192, 512):
    write_png(os.path.join(OUT, f"icon-{size}.png"), size, make_icon(size, False))
write_png(os.path.join(OUT, "icon-maskable-512.png"), 512, make_icon(512, True))
print("icons written:", sorted(os.listdir(OUT)))