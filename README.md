# 60篇外刊阅读 · 高考必备核心词（PWA）

📘 21 篇外刊阅读、**568 个高考核心词**的翻转单词卡应用，已整合为 **iOS 可安装的 PWA**（添加到主屏幕即用，支持离线）。

> 由 21 个独立的 `PASSAGE0X.html` 单词闪卡整合而来，保留每篇原始主题色与全部单词数据。

## ✨ 功能特性

- **首页**：单列按钮列表 —— REVIEW 收藏入口 + PASSAGE 1~21 全部篇目
- **单词闪卡**：3D 翻转卡（点卡片/Enter 翻转），上一个 / 下一个 / 随机
- **真人发音**：有道词典接口（HTTPS）+ 系统 TTS 兜底
- **REVIEW 收藏**：闪卡右上角「+」收藏单词，「GO」一键进入收藏词闪卡复习；收藏保存在本地（localStorage）
- **每篇独立主题色**：21 套渐变主题（含浅色主题自动加深文字，保证对比度）
- **PWA 能力**：Service Worker 离线缓存、Standalone 全屏模式、自定义图标

## 📱 安装到 iPhone

1. 用 **Safari** 打开部署地址
2. 点分享按钮 ⬆️ → **「添加到主屏幕」**
3. 命名后添加，主屏即出现应用图标（Standalone 模式，无 Safari 地址栏）

## 🗂 目录结构

```
app/                  # 应用本体（部署目录）
  ├── index.html      # 单页应用（首页 / 闪卡 / REVIEW 三视图）
  ├── data.js         # 21 篇 × 568 词数据（由脚本自动生成）
  ├── manifest.webmanifest
  ├── sw.js           # Service Worker（离线缓存）
  └── icons/          # 应用图标（180/192/512）
build/                # 数据提取与图标生成脚本
  ├── extract.py      # 解析 PASSAGE0X.html → data.js（含词数交叉校验）
  ├── make_icons_pure.py  # 零依赖 PNG 图标生成
  └── apply_icon.py   # 用自定义图生成多尺寸图标
```

## 🛠 本地运行

```bash
cd app
python3 -m http.server 8080     # 打开 http://localhost:8080
```

## 🔄 数据更新

新增/更新篇目后，重新运行 `build/extract.py` 再部署 `app/` 即可：

```bash
python3 build/extract.py        # 重新生成 app/data.js（自动校验词数一致性）
```

## 📄 许可

仅限个人学习使用。
