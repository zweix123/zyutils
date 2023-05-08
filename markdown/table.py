from settings import *

import re
from rich.progress import track
from util import file_util


def clear(filepath):
    content = file_util.read(filepath)
    pattern = re.compile(r"<!-- toc\.first -->\n(.*?\n)*?.*?\n<!-- toc\.second -->", re.S)  # fmt: skip
    content = re.sub(pattern, "[TOC]", content)
    file_util.write(filepath, content)


def get_menu(filename):
    content = file_util.read(filename)

    pattern = r"^(#{1,6})\s+(.+)$"
    matches = re.findall(pattern, content, re.MULTILINE)

    minn = 6 + 1

    headers = [[len(match[0]), match[1]] for match in matches]
    minn = min([level for level, _ in headers])

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
    for file in track(files):
        process(file)


if __name__ == "__main__":
    table()
