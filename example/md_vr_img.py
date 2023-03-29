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

import file_util

#

import os, re
from tqdm import tqdm


def process(filepath):
    _, filename = os.path.split(filepath)  # 获得文件名

    # 使用正则表达式获得项目名到文件名之间的路径
    _, midpath, _ = re.findall(
        "(?<=({}))(.*?)(?=({}))".format(re.escape(DIRNAME), re.escape(filename)),
        filepath,
    )[0]

    # 将路径转换成对应模式的中间路径
    if MODE == "note":
        t_list = midpath.split(os.sep)
        while "" in t_list:
            t_list.remove("")
        if len(t_list) != 0:
            midpath = "/".join(t_list) + "/"
        else:  # 特判类似README这样的
            midpath = str()
    elif MODE == "blog":
        midpath = os.path.basename(filename).split(".")[0] + "/"
    elif MODE == "OSS":
        midpath = "/"

    context = file_util.read(filepath)

    def modify(match):
        tar = match.group()

        pre, mid, suf = str(), str(), str()  # 链接图片的代码, pre和suf是其他部分, mid是路径部分
        if tar[-1] == ")":
            pre = tar[: tar.index("(") + 1]
            mid = tar[tar.index("(") + 1 : -1]
            suf = tar[-1]
        else:
            pre = tar[: tar.index('"') + 1]
            tar = tar[tar.index('"') + 1 :]  # 转换一下, 不是要使用
            mid = tar[: tar.index('"')]
            suf = tar[tar.index('"') :]

        _, photoname = os.path.split(mid)
        res = pre + (URLP + midpath + photoname) + suf

        # print("modified: ", res, photoname)
        return res

    # 匹配所有图片链接并修改
    patten = r"!\[.*?\]\((.*?)\)|<img.*?src=[\'\"](.*?)[\'\"].*?>"
    context = re.sub(patten, modify, context)

    file_util.write(filepath, context)  # 写回


def transfer():
    filenames = file_util.get_files_under_folder(DIRPATH, "md")
    for filename in tqdm(filenames):
        process(filename)


transfer()
