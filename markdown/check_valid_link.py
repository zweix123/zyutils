from settings import *

from rich.progress import track
from util import str_util, file_util, md_util, net_util, rich_util


def solve():
    urls, paths = list(), list()
    for filepath in track(
        file_util.get_files_under_folder(DIRPATH, "md"), description="提取链接..."
    ):
        temp = md_util.get_not_image_link(file_util.read(filepath))
        temp = [sam for sam in temp if str_util.is_url(sam)]
        urls += temp
        paths += [filepath] * len(temp)

    table = list()
    table.append(["链接", "文件"])
    for url, path in net_util.check_url_link_path_pairs_return_invalid(urls, paths):
        table.append([url, path])

    rich_util.print_table(table)


if __name__ == "__main__":
    solve()
