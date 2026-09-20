# -*- coding: utf-8 -*-
"""把中文字体按某个网页实际用到的字符做子集化，输出 woff2。

中文字体动辄 4~20MB，整份塞进网页在手机上没法看。但一个页面通常只用到
几百个汉字，子集化之后一般只剩几十 KB。

iOS Safari 只向 CSS 暴露很少的系统字体（PingFang / Songti 等），
像魏碑、手札体这些内置字体 font-family 根本调不到，所以中文网页想用
特色字体，只能自己嵌 —— 这个脚本就是为这件事准备的。

用法:
    python tools/subset-cn-font.py <源字体.ttf> <页面.html> <输出.woff2>

可选:
    --extra "额外要保留的字"   # 之后可能加进页面、但现在还没出现的字
    --base64                  # 额外打印 base64，便于直接内嵌进 HTML
"""
import argparse
import os
import re
import subprocess
import sys


#: 注释里的中文只有写代码的人看得到，不该占字体体积。
#: 源码里中文注释往往比正文还多，剥掉能省一半以上。
COMMENT_PATTERNS = [
    re.compile(r"<!--.*?-->", re.S),   # HTML
    re.compile(r"/\*.*?\*/", re.S),    # CSS / JS 块注释
    re.compile(r"(?m)^\s*//.*$"),      # JS 整行注释（不动 https:// 这类行内的）
]


def collect_chars(paths, extra=""):
    """扫描文件里会显示出来的字符。

    页面上的中文有的写在 HTML 里，有的藏在 JS 数组中，与其解析结构，
    不如直接取源码的字符集合 —— 多留几个字的代价可以忽略，
    但注释要先剥掉，否则字体里会塞满只有开发者看得见的字。
    """
    chars = set(extra)
    for p in paths:
        with open(p, encoding="utf-8") as f:
            text = f.read()
        for pat in COMMENT_PATTERNS:
            text = pat.sub(" ", text)
        chars |= set(text)
    # 控制字符不需要进字体
    chars = {c for c in chars if c.isprintable() and c != " "}
    return "".join(sorted(chars))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("font", help="源字体 .ttf / .otf")
    ap.add_argument("pages", nargs="+", help="要扫描的页面文件（可多个）")
    ap.add_argument("-o", "--output", required=True, help="输出 .woff2")
    ap.add_argument("--extra", default="", help="额外保留的字符")
    ap.add_argument("--base64", action="store_true", help="同时打印 base64")
    args = ap.parse_args()

    chars = collect_chars(args.pages, args.extra)

    subprocess.run([
        sys.executable, "-m", "fontTools.subset", args.font,
        "--text=" + chars,
        "--flavor=woff2",
        "--layout-features=vert,vrt2,ccmp,locl",
        "--output-file=" + args.output,
    ], check=True)

    src = os.path.getsize(args.font)
    dst = os.path.getsize(args.output)
    print("字符数 %d" % len(chars))
    print("%.2f MB -> %.1f KB (%.1f%%)" % (
        src / 1048576, dst / 1024, dst / src * 100))

    if args.base64:
        import base64
        blob = base64.b64encode(open(args.output, "rb").read()).decode()
        print("\nsrc:url(data:font/woff2;base64,%s...) format('woff2')" % blob[:60])
        print("完整 base64 长度:", len(blob))


if __name__ == "__main__":
    main()
