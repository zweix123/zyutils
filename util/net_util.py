import asyncio
import aiohttp
import requests
from fake_useragent import UserAgent
from rich.progress import Progress
from typing import Any, Tuple


def get_resp(url):  # 爬虫
    # ua池
    user_anent = UserAgent().random  # ua池
    headers = {"User-Agent": user_anent}

    # ip池

    # 开始爬取
    resp = requests.get(url=url, headers=headers)
    resp.encoding = resp.apparent_encoding  # 设置编码

    return resp


def down(url: str, filepath: str):
    result = get_resp(url)
    with open(filepath, "wb") as f:
        f.write(result.content)


class Event:
    def __init__(self, url: str, data: Any) -> None:
        self.url = url
        self.is_valid = True
        self.data = data

    def __str__(self) -> str:
        return self.url + ", " + str(self.data)


class URLChecker:
    def __init__(self, data: list[Event]) -> None:
        self.data = data

    def __call__(self) -> list[Event]:
        asyncio.run(self.check_urls())

        return self.data

    async def check_url(
        self, index: int, session: aiohttp.ClientSession, progress, task_id
    ):
        try:
            async with session.get(self.data[index].url) as response:
                if response.status == 200:
                    self.data[index].is_valid = True
                else:
                    self.data[index].is_valid = False
            progress.update(task_id, advance=1)
        except:
            self.data[index].is_valid = False
            progress.update(task_id, advance=1)

    async def check_urls(self):
        async with aiohttp.ClientSession(
            headers={"User-Agent": UserAgent().random}
        ) as session:
            with Progress() as progress:
                task_id = progress.add_task("Check URLs...", total := len(self.data))
                for i in range(total):
                    await self.check_url(
                        i, session, progress, task_id
                    ) | progress.update(task_id, advance=1)


def check_url_link_path_pairs_return_invalid(
    urls: list[str], paths: list[str]
) -> Tuple[list[str], list[str]]:
    assert len(urls) == len(paths), "提供的urls和paths应该成对"
    pairs: list[Event] = list()
    for url, path in zip(urls, paths):
        pairs.append(Event(url, path))

    inter = URLChecker(pairs)()

    return ([event.url for event in inter], [event.data for event in inter])
