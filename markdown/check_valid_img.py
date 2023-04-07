from settings import *

import os
from rich.progress import track
from util import net_util, file_util, md_util, str_util, rich_util


def check():
    url_events: list[net_util.Event] = list()
    path_pairs: list(tuple(str, str)) = list()

    for filepath in track(
        file_util.get_filepaths_under_folder(DIRPATH, "md"), description="提取图片链接"
    ):
        for link in md_util.get_image_link(file_util.read(filepath)):
            if str_util.is_url(link):
                url_events.append(net_util.Event(url=link, data=filepath))
            else:
                path_pairs.append((link, filepath))

    ans: list(tuple(str, str)) = list()

    if len(url_events) != 0:
        ans += [(event.url, event.data) for event in net_util.URLChecker(url_events)()]

    if len(path_pairs) != 0:
        for pathpair in track(path_pairs, description="Check Path: "):
            img_file_path = os.path.normpath(
                os.path.join(
                    os.path.abspath(
                        os.path.join(DIRNAME, os.path.dirname(pathpair[0]))
                    ),
                    pathpair[1],
                )
            )
            if os.path.exists(img_file_path) is False:
                ans.append(pathpair)

    if len(ans) != 0:
        table = list()
        table.append(["链接", "文件"])
        for sam in ans:
            table.append(list(sam))
        rich_util.print_table(table)
    else:
        print("没有失效图床链接")


if __name__ == "__main__":
    check()
