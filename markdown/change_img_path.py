from settings import *

import os, re
from rich.progress import track
from util import file_util, md_util


def process(filepath):
    # 从文件路径中获得项目名到文件名之间的路径
    _, midpath, _ = re.findall(
        "(?<=({}))(.*?)(?=({}))".format(
            re.escape(DIRNAME), re.escape(os.path.basename(filepath))
        ),
        filepath,
    )[0]

    # 将上面的中间路径转换成对应模式的中间路径
    if MODE == "note":
        t_list = midpath.split(os.sep)
        while "" in t_list:
            t_list.remove("")
        if len(t_list) != 0:
            midpath = "/".join(t_list) + "/"
        else:  # 特判类似README这样的
            midpath = str()
    elif MODE == "blog":
        midpath = os.path.basename(filepath).split(".")[0] + "/"
    elif MODE == "OSS":
        midpath = "/"

    def in_func(link):
        return URLP + midpath + os.path.basename(link)

    content = file_util.read(filepath)
    content = md_util.process_images(content, in_func)
    file_util.write(filepath, content)


def solve():
    fs = file_util.get_files_under_folder(DIRPATH, "md")
    for filepath in track(fs):
        process(filepath)


if __name__ == "__main__":
    solve()
