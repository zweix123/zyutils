DIRPATH = r"/home/netease/Documents/CS-notes/"  # Markdown项目根目录绝对路径
URL = "https://cdn.jsdelivr.net/gh/zweix123/CS-notes@master/resource/"  # 项目使用图床的URL前缀
IMGPATHPRE = "resource"  # 图片所在目录
MODE = "note"  # 模式有["note", "blog", "OSS"], 具体解释见README
ZYUTILS = r"/home/netease/Projects/zyutils/"  # zyutils的绝对路径


try:
    import sys

    sys.path.append(ZYUTILS)
    import util.file_util as file_util, util.md_util as md_util
except ImportError as ierr:
    print("zyutils的绝对路径不正确")
    exit(0)


import os, shutil
from rich.progress import track
from urllib.parse import unquote


def check_config():
    assert os.path.exists(DIRPATH) is True, "Markdwon项目路径不存在"
    assert DIRPATH[-1] == os.sep, "Markdwon项目路径不以" + os.sep + "结尾"
    assert URL[-1] == "/", "图床URL前缀没有以'/'结尾"
    assert IMGPATHPRE in URL, IMGPATHPRE + "可能有错误"


def clean():
    check_config()

    inter = list()

    for filepath in track(
        file_util.get_files_under_folder(DIRPATH, "md"), description="提取所有图片链接"
    ):
        inter += md_util.get_image_link(file_util.read(filepath))

    valid_imgs_path = [
        os.path.join(IMGPATHPRE, img_link[len(URL) :])
        for img_link in inter
        if img_link.startswith(URL)  # 相当于只处理图床管理的图片
    ]

    valid_imgs_path = list(map(unquote, valid_imgs_path))

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


if __name__ == "__main__":
    clean()
