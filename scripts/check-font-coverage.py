# -*- coding: utf-8 -*-
"""检查页面用到的汉字有没有落在嵌入字体的子集之外。

子集化是按「当时页面上有哪些字」做的，所以任何一次改文案、加店名，
都可能引入子集里没有的字 —— 那些字会静悄悄回落到系统字体，
在 iOS 上尤其明显（系统根本没有对应的字体，样式直接崩掉）。

这个脚本就是拿来兜住这件事的，改完文案跑一次：

    python scripts/check-font-coverage.py

有缺字会列出来并以非零状态退出。补救办法是重跑 subset-cn-font.py。
"""
import glob
import io
import os
import re
import sys

from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

COMMENT_PATTERNS = [
    re.compile(r"<!--.*?-->", re.S),
    re.compile(r"/\*.*?\*/", re.S),
    re.compile(r"(?m)^\s*//.*$"),
]


def page_chars(path):
    text = io.open(path, encoding="utf-8").read()
    for pat in COMMENT_PATTERNS:
        text = pat.sub(" ", text)
    return {c for c in text if "一" <= c <= "鿿"}


def font_chars(path):
    cov = set()
    for table in TTFont(path)["cmap"].tables:
        cov |= {chr(code) for code in table.cmap}
    return cov


def main():
    pages = [os.path.join(HERE, "what-to-eat.html")]
    fonts = sorted(glob.glob(os.path.join(HERE, "fonts", "*.woff2")))
    if not fonts:
        print("fonts/ 下没有字体，跳过")
        return 0

    used = set()
    for p in pages:
        used |= page_chars(p)

    bad = False
    for f in fonts:
        missing = sorted(used - font_chars(f))
        name = os.path.basename(f)
        if missing:
            bad = True
            print("%s 缺 %d 字: %s" % (name, len(missing), "".join(missing)))
        else:
            print("%s 覆盖全部 %d 字" % (name, len(used)))

    if bad:
        print("\n重跑 scripts/subset-cn-font.py 补齐这些字。")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
