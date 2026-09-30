#!/usr/bin/env python3
"""
submit_indexnow.py — 把站点 URL 推送给 Bing IndexNow。

前置:
    - 仓库根已存在 indexnow-<key>.txt（内容为 key）
    - host = pet.goods-infinite.com

用法:
    python tools/submit_indexnow.py            # 推送 sitemap 内全部 URL
    python tools/submit_indexnow.py URL1 URL2  # 仅推送指定 URL

说明:
    - IndexNow 用于"新增/变更"即时推送，不要每次部署狂推全量（会被限流）。
    - 首次上线可全量推一次；之后只推改动页。
"""
import sys, os, re, json, urllib.request, urllib.error

HOST = "pet.goods-infinite.com"

def load_key(root):
    for f in os.listdir(root):
        if f.startswith("indexnow-") and f.endswith(".txt"):
            key = open(os.path.join(root, f), encoding="utf-8").read().strip()
            return key, f"https://{HOST}/{f}"
    raise SystemExit("未找到 indexnow-<key>.txt，请先生成密钥文件")

def get_sitemap_urls(root):
    sp = os.path.join(root, "sitemap.xml")
    s = open(sp, encoding="utf-8").read()
    return re.findall(r"<loc>(.*?)</loc>", s)

def post(key, keyloc, urls):
    body = json.dumps({"host": HOST, "key": key, "keyLocation": keyloc, "urlList": urls}).encode()
    req = urllib.request.Request("https://www.bing.com/indexnow", data=body,
                                 headers={"Content-Type": "application/json"})
    try:
        r = urllib.request.urlopen(req, timeout=30)
        print(f"  HTTP {r.status} 已推送 {len(urls)} 条")
    except urllib.error.HTTPError as e:
        print(f"  HTTP {e.code}: {e.read().decode()[:300]}")

def main():
    root = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("http") else "."
    key, keyloc = load_key(root)
    if len(sys.argv) > 1 and sys.argv[1].startswith("http"):
        urls = sys.argv[1:]
    else:
        urls = get_sitemap_urls(root)
    print(f"IndexNow key: {key[:8]}...  keyLocation: {keyloc}")
    print(f"准备推送 {len(urls)} 条 URL:")
    post(key, keyloc, urls)

if __name__ == "__main__":
    main()
