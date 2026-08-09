#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 PASSAGE01-21.html 提取单词数据与主题色，生成 app/data.js"""
import re, os, json, sys

SRC = "/Users/tea/Library/Mobile Documents/com~apple~CloudDocs/【英语】/60篇外刊/单词卡"
OUT_DIR = "/Users/tea/WorkBuddy/2026-08-09-23-35-37/app"

def extract(path):
    with open(path, encoding="utf-8") as f:
        html = f.read()
    # 编号
    m_id = re.search(r"PASSAGE(\d+)", path.split("/")[-1])
    pid = int(m_id.group(1))
    # 标题
    m_title = re.search(r"<h1>\s*([^<]+)</h1>", html)
    title = m_title.group(1).strip() if m_title else f"PASSAGE {pid}"
    # 页面总词数（计数器 “1 / 24”）
    m_total = re.search(r'id="progressDisplay">\s*1\s*/\s*(\d+)', html)
    counter_total = int(m_total.group(1)) if m_total else None
    # body 渐变（可 2 段或 3 段）取首末色
    m_bg = re.search(r"background:\s*linear-gradient\(135deg,\s*([^)]*)\)", html)
    colors = re.findall(r"#[0-9a-fA-F]{6}", m_bg.group(1)) if m_bg else ["#5a4a8a", "#9a8ac8"]
    c1, c2 = colors[0], colors[-1]
    # 卡片正面渐变第二色（cardBg）
    m_card = re.search(r"\.card-front\s*\{[\s\S]*?linear-gradient\(160deg,\s*#[0-9a-fA-F]{6}\s*0%,\s*(#[0-9a-fA-F]{6})\s*100%\)", html)
    card_bg = m_card.group(1) if m_card else "#f0eaf8"
    # wordsData 数组（首个 `];` 即结尾；词组数组内不会出现 `];`）
    start = html.index("const wordsData = [")
    arr_start = html.index("[", start)
    end = html.index("];", arr_start)  # 指向 ]
    data_js = html[arr_start:end + 1]  # 不含结尾 ;
    # 词数：统计 word: 键（每个对象恰有一个）
    wc = len(re.findall(r"\bword\s*:", data_js))
    return {
        "id": pid,
        "title": title,
        "c1": c1.upper(),
        "c2": c2.upper(),
        "cardBg": card_bg.upper(),
        "count": wc,
        "counter_total": counter_total,
        "data_js": data_js,
    }

def main():
    files = sorted(
        [os.path.join(SRC, f) for f in os.listdir(SRC) if re.fullmatch(r"PASSAGE\d+\.html", f)],
        key=lambda p: int(re.search(r"(\d+)", os.path.basename(p)).group(1)),
    )
    print(f"发现 {len(files)} 个文件")
    passages = []
    total_words = 0
    problems = []
    for p in files:
        item = extract(p)
        if item["counter_total"] is not None and item["counter_total"] != item["count"]:
            problems.append(f"{os.path.basename(p)}: 提取 {item['count']} vs 页面标注 {item['counter_total']}")
        passages.append(item)
        total_words += item["count"]
        print(f"  PASSAGE{item['id']:>2}  {item['count']:>3} 词  {item['c1']} → {item['c2']}  cardBg={item['cardBg']}")
    if problems:
        print("!! 不一致：", *problems, sep="\n")
        sys.exit(1)
    print(f"总计 {len(passages)} 篇 / {total_words} 词")
    # 生成 data.js
    os.makedirs(OUT_DIR, exist_ok=True)
    js = "/* 由 build/extract.py 自动生成 — 60篇外刊单词卡数据 */\n"
    js += "window.PASSAGES = [\n"
    for it in passages:
        js += f"  {{ id: {it['id']}, title: {json.dumps(it['title'], ensure_ascii=False)}, "
        js += f"c1: '{it['c1']}', c2: '{it['c2']}', cardBg: '{it['cardBg']}', words: {it['data_js']} }},\n"
    js += "];\n"
    with open(os.path.join(OUT_DIR, "data.js"), "w", encoding="utf-8") as f:
        f.write(js)
    print(f"已写入 {OUT_DIR}/data.js  ({len(js)/1024:.0f} KB)")
    # 汇总信息
    with open(os.path.join(OUT_DIR, "meta.json"), "w", encoding="utf-8") as f:
        json.dump({"count": len(passages), "total_words": total_words,
                   "passages": [{ "id": it["id"], "title": it["title"], "count": it["count"],
                                  "c1": it["c1"], "c2": it["c2"] } for it in passages]},
                  f, ensure_ascii=False, indent=1)
    print("已写入 meta.json")

if __name__ == "__main__":
    main()
