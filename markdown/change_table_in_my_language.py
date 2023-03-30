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

import re
from tqdm import tqdm


def clear(filepath):
    content = file_util.read(filepath)
    pattern = re.compile(
        r"<!-- toc\.first -->\n(.*?\n)*?.*?\n<!-- toc\.second -->", re.S
    )
    content = re.sub(pattern, "[TOC]", content)
    file_util.write(filepath, content)


def get_menu(filename):
    content = file_util.read(filename)

    pattern = r"^(#{1,6})\s+(.+)$"
    matches = re.findall(pattern, content, re.MULTILINE)

    minn = 6 + 1

    headers = []
    for match in matches:
        level = len(match[0])
        text = match[1]
        headers.append([level, text])
        if level < minn:
            minn = level

    for i in range(len(headers)):
        headers[i][0] -= minn - 1

    content = ""
    for level, text in headers:
        text_converted = text.replace(" ", "-")
        row = "    " * (level - 1) + "-   [" + text + "](#" + text_converted + ")\n"

        content += row

    return content


def create(filepath):
    content = file_util.read(filepath)
    table = "<!-- toc.first -->\n{}<!-- toc.second -->\n".format(get_menu(filepath))
    table = table.replace("\\s", "\\\s")  # 特判如果标题中出现`\s`
    content = re.sub(r"^\[TOC\]\n", table, content, flags=re.MULTILINE)

    file_util.write(filepath, content)


def process(filepath):
    clear(filepath)
    create(filepath)


def table():
    files = file_util.get_files_under_folder(DIRPATH, "md")
    for file in tqdm(files):
        process(file)


table()
