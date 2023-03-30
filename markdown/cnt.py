DIRPATH = r"/home/netease/Documents/CS-notes"  # 要处理的Markdown项目根目录的绝对路径
URLP = "https://cdn.jsdelivr.net/gh/zweix123/CS-notes@master/resource"  # 项目使用图床的URL前缀
MODE = "note"  # 模式有["note", "blog", "OSS"], 具体解释见下


import os

if DIRPATH[-1] != os.sep:
    DIRPATH += os.sep

if URLP[-1] != "/":
    URLP += "/"

DIRNAME = DIRPATH.split(os.sep)[-2]

IMGPATHPRE = URLP.split(os.sep)[-2]


def check_cnt():
    if DIRPATH is None or DIRPATH == "":
        print("请填写项目所在文件路径")
        return False
    if os.path.exists(DIRPATH) is False:
        print("项目目录不存在")
        return False
    return True


def check_perl():
    if check_cnt() is False:
        return False
    if URLP is None or URLP == "":
        print("请填写图床前缀")
        return False
    if MODE not in ["note", "blog", "OSS"]:
        print("请查看图床路径前缀是否填写或填写是否正确")
        return False
    return True


def check():
    return check_cnt() and check_perl()


check()

#

import sys
from os.path import abspath, dirname

sys.path.append(abspath(dirname(dirname(__file__))))

#

import util.file_util as file_util

#

import string
from tqdm import tqdm


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
    filenames = file_util.get_files_under_folder(DIRPATH, "md")

    count_en, count_zh, count_dg, count_pu = 0, 0, 0, 0

    for file in tqdm(filenames):
        with open(file, encoding=file_util.get_file_code(file)) as f:
            for line in f:
                t = count_content(line)
                count_en += t[0]
                count_zh += t[1]
                count_dg += t[2]
                count_pu += t[3]

    print("总共{}篇文章".format(len(filenames)))
    print("英文:", f"{int(count_en):,d}")
    print("中文:", f"{int(count_zh):,d}")
    print("数字:", f"{int(count_dg):,d}")
    print("标点:", f"{int(count_pu):,d}")
    print(
        "汇总:",
        f"{int(count_zh + count_en // 6 + count_dg // 32):,d}",
        "(使用算法认为每6个字母是单词、每32个数字是一个字)",
    )


cnt()
