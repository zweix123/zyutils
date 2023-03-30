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

import util.file_util as file_util, util.str_util as str_util, util.md_util as md_util

#

from tqdm import tqdm
from prettytable import PrettyTable

import asyncio
import aiohttp
from tqdm.asyncio import tqdm


class UrlChecker:
    def __init__(self, urlpairs: list[(str, str)]) -> None:
        self.urlpairs = urlpairs
        self.invalid_urlpairs = list()

    def __call__(self) -> list[str]:
        asyncio.run(self.check_urlpairs())
        return self.invalid_urlpairs

    async def check_urlpair(self, pair, session, pbar):
        timeout = aiohttp.ClientTimeout(total=5)
        try:
            async with session.get(pair[1], timeout=timeout) as response:
                pbar.update(1)
                if response.status == 200:
                    pass
                else:
                    self.invalid_urlpairs.append(pair)
        except:
            self.invalid_urlpairs.append(pair)

    async def check_urlpairs(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299",
            "Referer": "https://www.example.com",
            "Accept-Language": "en-US,en;q=0.9",
        }
        async with aiohttp.ClientSession(headers=headers) as session:
            tasks = []
            n = len(self.urlpairs)
            with tqdm(total=n) as pbar:
                for i in range(n):
                    task = asyncio.create_task(
                        self.check_urlpair(self.urlpairs[i], session, pbar)
                    )
                    tasks.append(task)
                for coroutine in asyncio.as_completed(tasks):
                    await coroutine


def not_should_filtered(s: str):
    if s.startswith("#") is True:
        return False
    return True


def check():
    targets = list()
    print("提取链接:")
    for filepath in tqdm(file_util.get_files_under_folder(DIRPATH, "md")):
        temp = md_util.get_not_image_link(file_util.read(filepath))
        temp = [sam for sam in temp if str_util.is_url(sam)]
        # temp = [sam for sam in temp if not_should_filtered(sam)]
        targets += list(zip([filepath] * len(temp), temp))

    # print(targets)
    invalid_urlpairs = list()

    print("检测链接:")
    urlchecker = UrlChecker(targets)
    invalid_urlpairs += urlchecker()

    ans = invalid_urlpairs

    if len(ans) != 0:
        table = PrettyTable()
        table.field_names = ["文件", "链接"]
        for sam in ans:
            table.add_row([sam[0][len(DIRPATH) :], sam[1]])
        print(table)
    else:
        print("没有失效图床链接")


check()
