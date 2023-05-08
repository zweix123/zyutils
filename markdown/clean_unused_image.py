from settings import *

import os, shutil
from rich.progress import track
from urllib.parse import unquote
from util import file_util, md_util


def clean():
    inter = list()

    for filepath in track(
        file_util.get_files_under_folder(DIRPATH, "md"), description="提取所有图片链接"
    ):
        inter += md_util.get_image_link(file_util.read(filepath))

    valid_imgs_path = [
        os.path.join(IMGPATHPRE, img_link[len(URLP) :])
        for img_link in inter
        if img_link.startswith(URLP)  # 相当于只处理图床管理的图片
    ]

    valid_imgs_path = list(map(unquote, valid_imgs_path))

    imgs_path = map(
        lambda path: path[len(DIRPATH) :],
        file_util.get_files_under_folder(os.path.join(DIRPATH, IMGPATHPRE)),
    )

    trash_can = os.path.join(DIRPATH, "trash_can")
    file_util.mkdir(trash_can)

    flag = False

    for img_path in imgs_path:
        if img_path not in valid_imgs_path:
            tar = os.path.join(DIRPATH, img_path)
            shutil.move(tar, trash_can)
            flag = True

    if flag is False:
        os.removedirs(trash_can)


if __name__ == "__main__":
    clean()
