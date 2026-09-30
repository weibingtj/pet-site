#!/usr/bin/env python3
"""
inject_ga4.py — 把宠物站全站 GA ID 从主站 G-68HRE7BJFK 换成 pet 独立 GA4 流。

用法:
    python tools/inject_ga4.py <pet-site目录> <新GA4_ID>

示例:
    python tools/inject_ga4.py . G-ABC123XYZ

行为:
    - 递归扫描所有 *.html
    - 替换 gtag/js?id=G-68HRE7BJFK  -> 新 ID
    - 替换 gtag('config','G-68HRE7BJFK') -> 新 ID
    - 仅改这两处，不动其他内容
    - 默认 dry-run (加 --apply 才真写)

注意:
    若文章 HTML 由 ../build_pet_site.py 生成，需在生成器模板里同步改，
    否则 regenerate 后本脚本的改动会被覆盖。
"""
import sys, os, re, glob

OLD_ID = "G-68HRE7BJFK"
RE_SRC = re.compile(r"gtag/js\?id=" + re.escape(OLD_ID))
RE_CFG = re.compile(r"gtag\('config',\s*'" + re.escape(OLD_ID) + r"'\)")

def process(html, new_id, apply):
    n = 0
    new, c1 = RE_SRC.subn("gtag/js?id=" + new_id, html)
    n += c1
    new, c2 = RE_CFG.subn("gtag('config','" + new_id + "')", new)
    n += c2
    if apply and n:
        with open(html, "w", encoding="utf-8") as f:
            f.write(new)
    return n

def main():
    if len(sys.argv) < 3:
        print("用法: python inject_ga4.py <目录> <新GA4_ID> [--apply]")
        sys.exit(1)
    root, new_id = sys.argv[1], sys.argv[2]
    apply = "--apply" in sys.argv
    files = glob.glob(os.path.join(root, "**", "*.html"), recursive=True)
    total = 0
    for f in files:
        c = process(open(f, encoding="utf-8").read(), new_id, apply)
        if c:
            total += c
            print(("WRITE " if apply else "DRY   ") + f + f"  ({c} 处)")
    print(f"\n共处理 {len(files)} 个文件，替换 {total} 处。" + ("" if apply else " [dry-run, 加 --apply 真正写入]"))

if __name__ == "__main__":
    main()
