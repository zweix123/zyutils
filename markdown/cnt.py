DIRPATH = r"/home/netease/Documents/CS-notes/"  # Markdown项目根目录绝对路径
ZYUTILS = r"/home/netease/Projects/zyutils/"  # zyutils的绝对路径


try:
    import sys

    sys.path.append(ZYUTILS)
    import util.file_util as file_util, util.md_util as md_util
except ImportError as ierr:
    print("zyutils的绝对路径不正确")
    exit(0)


import os, sys, string
from rich.progress import track


def check_config():
    assert os.path.exists(DIRPATH) is True, "Markdwon项目路径不存在"
    assert DIRPATH[-1] == os.sep, "Markdwon项目路径不以" + os.sep + "结尾"


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


def cnt():
    check_config()

    filenames = file_util.get_files_under_folder(DIRPATH, "md")

    count_en, count_zh, count_dg, count_pu = 0, 0, 0, 0

    for file in track(filenames):
        with open(file, encoding=file_util.get_file_code(file)) as f:
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
    cnt()
