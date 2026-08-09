#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""用用户提供的 icon.jpg 生成填充满整个图标的多尺寸 PNG。"""
import os
from PIL import Image

SRC = "/Users/tea/Library/Mobile Documents/com~apple~CloudDocs/【英语】/60篇外刊/单词卡/60篇外刊单词卡App/icon.jpg"
OUT = "/Users/tea/WorkBuddy/2026-08-09-23-35-37/app/icons"
os.makedirs(OUT, exist_ok=True)

img = Image.open(SRC).convert("RGBA")
w, h = img.size
print("源图:", img.size)

for size in (180, 192, 512):
    resized = img.resize((size, size), Image.LANCZOS)
    resized.save(os.path.join(OUT, f"icon-{size}.png"), "PNG")
    print(f"icon-{size}.png: {size}x{size}")
resized = img.resize((512, 512), Image.LANCZOS)
resized.save(os.path.join(OUT, "icon-maskable-512.png"), "PNG")
print("icon-maskable-512.png: 512x512 (full fill)")