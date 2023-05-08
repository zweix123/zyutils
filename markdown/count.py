from settings import *

import string
from rich.progress import track
from util import file_util


def count_content(content):
    # English, Chinese, Digit, Punctuation
    cnt_en, cnt_zh, cnt_dg, cnt_pu = [0] * 4

    for c in content:
        if c in string.ascii_letters:  # 英文
            cnt_en += 1
        elif c.isalpha():  # 中文, isalpha()会得到英文和中文, 但是英文已经在上面的if筛选了
            cnt_zh += 1
        elif c.isdigit():  # 数字
            cnt_dg += 1
        elif c.isspace():  # 空格
            pass
        else:  # 标点符号
            cnt_pu += 1

    return cnt_en, cnt_zh, cnt_dg, cnt_pu


def count():
    filenames = file_util.get_filepaths_under_dir(DIRPATH, "md")

    count_en, count_zh, count_dg, count_pu = 0, 0, 0, 0

    for file in track(filenames):
        with open(file, encoding=file_util.get_file_encode(file)) as f:
            for line in f:
                t = count_content(line)
                count_en += t[0]
                count_zh += t[1]
                count_dg += t[2]
                count_pu += t[3]

    print(f"总共{len(filenames)}篇文章")
    print(f"字母:{int(count_en):,d}个")
    print(f"汉字:{int(count_zh):,d}字")
    print(f"数字:{int(count_dg):,d}位")
    print(f"标点:{int(count_pu):,d}个")
    print(f"总共大约:{int(count_zh + count_en//6 + count_dg//32):,d}字")  # fmt: skip


if __name__ == "__main__":
    count()
