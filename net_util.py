import asyncio
import aiohttp
from tqdm.asyncio import tqdm


class UrlFilter:
    def __init__(self, urls: list[str]) -> None:
        self.urls = urls
        self.valid_urls = list()
        self.invalid_urls = list()

    def __call__(self) -> list[str]:
        asyncio.run(self.check_urls())
        return self.valid_urls, self.invalid_urls

    async def check_url(self, url, session, pbar):
        try:
            async with session.get(url) as response:
                pbar.update(1)
                if response.status == 200:
                    self.valid_urls.append(url)
                else:
                    self.invalid_urls.append(url)
        except:
            self.invalid_urls.append(url)

    async def check_urls(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299"
        }
        async with aiohttp.ClientSession(headers=headers) as session:
            tasks = []
            n = len(self.urls)
            with tqdm(total=n) as pbar:
                for i in range(n):
                    task = asyncio.create_task(
                        self.check_url(self.urls[i], session, pbar)
                    )
                    tasks.append(task)
                for coroutine in asyncio.as_completed(tasks):
                    await coroutine


import requests
from fake_useragent import UserAgent


def get_resp(url):  # 爬虫
    # ua池
    user_anent = UserAgent().random  # ua池
    headers = {"User-Agent": user_anent}

    # ip池

    # 开始爬取
    resp = requests.get(url=url, headers=headers)
    resp.encoding = resp.apparent_encoding  # 设置编码

    return resp
