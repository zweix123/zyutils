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

import util.file_util as file_util, util.md_util as md_util

#

import os


import shutil, urllib
from tqdm import tqdm


def clean():
    inter = list()
    print("提取所有图片链接")
    for filepath in tqdm(file_util.get_files_under_folder(DIRPATH, "md")):
        inter += md_util.get_image_link(file_util.read(filepath))

    valid_imgs_path = [
        os.path.join(IMGPATHPRE, img_link[len(URLP) :])
        for img_link in inter
        if img_link.startswith(URLP)  # 相当于只处理图床管理的图片
    ]

    valid_imgs_path = list(map(urllib.parse.unquote, valid_imgs_path))

    imgs_path = map(
        lambda path: path[len(DIRPATH) :],
        file_util.get_files_under_folder(os.path.join(DIRPATH, IMGPATHPRE)),
    )

    trash_can = os.path.join(DIRPATH, "trash_can")
    file_util.mkdir(trash_can)

    for img_path in imgs_path:
        if img_path not in valid_imgs_path:
            tar = os.path.join(DIRPATH, img_path)
            shutil.move(tar, trash_can)


clean()
