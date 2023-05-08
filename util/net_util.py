import platform
import requests
from fake_useragent import UserAgent
from threading import Thread
from asyncio import (
    run as asyncio_run,
    get_running_loop,
    new_event_loop,
    set_event_loop,
    run_coroutine_threadsafe,
    AbstractEventLoop,
)
from aiohttp import ClientSession, ClientResponse
from rich.progress import Progress
from typing import Any, Tuple, Callable, Optional, Union, Literal, Coroutine

if platform.system() == "Windows":
    # from asyncio import set_event_loop_policy, WindowsSelectorEventLoopPolicy
    # set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    pass


class Request:
    def __init__(
        self,
        method: Literal["GET", "POST"],
        url: str,
        params: Optional[dict] = None,
        data: Optional[dict] = None,
        headers: Optional[dict] = None,
        callback: Optional[Callable[["Response"], None]] = None,
        response: Optional["Response"] = None,
    ) -> None:
        self.method: Literal["GET", "POST"] = method
        self.url: str = url
        self.params: Optional[dict] = params
        self.data: Optional[dict] = data
        self.headers: Optional[dict] = headers
        self.callback: Optional[Callable[["Response"], None]] = callback
        self.response: Optional["Response"] = response

        if self.headers is None:
            user_anent = UserAgent().random
            headers = {"User-Agent": user_anent}


class Response:
    def __init__(self, status: int, headers, data: Any) -> None:
        self.status: int = status
        self.headers: str = headers
        self.data = data


class Rail(object):
    def __init__(self):
        self.session: ClientSession = None
        self.loop: AbstractEventLoop = None

    @staticmethod
    def start_event_loop(loop: AbstractEventLoop) -> None:
        if not loop.is_running():
            thread = Thread(target=Rail.run_event_loop, args=(loop,))
            thread.daemon = True
            thread.start()

    @staticmethod
    def run_event_loop(loop: AbstractEventLoop) -> None:
        set_event_loop(loop)
        loop.run_forever()

    def start(self, session_number: int = 3) -> None:
        try:
            self.loop = get_running_loop()
        except RuntimeError:
            self.loop = new_event_loop()
        Rail.start_event_loop(self.loop)

    def stop(self) -> None:
        if self.loop and self.loop.is_running():
            self.loop.stop()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def join(self) -> None:
        pass

    def add_request(
        self,
        method: Literal["GET", "POST"],
        url: str,
        params: Optional[dict] = None,
        data: Optional[dict] = None,
        headers: Optional[dict] = None,
        callback: Optional[Callable[["Response"], None]] = None,
    ) -> Request:
        request: Request = Request(method, url, params, data, headers, callback)
        coro: Coroutine = self._process_request(request)
        run_coroutine_threadsafe(coro, self.loop)
        return request

    def request(
        self,
        method: Literal["GET", "POST"],
        url: str,
        params: Optional[dict] = None,
        data: Optional[dict] = None,
        headers: Optional[dict] = None,
    ) -> Response:
        request: Request = Request(method, url, params, data, headers)
        coro: Coroutine = self._get_response(request)
        fut = run_coroutine_threadsafe(coro, self.loop)
        return fut.result()

    async def _get_response(self, request: Request) -> Response:
        if not self.session:
            self.session = ClientSession(trust_env=True)

        cr: ClientResponse = await self.session.request(
            request.method,
            request.url,
            headers=request.headers,
            params=request.params,
            data=request.data,
        )

        status = cr.status
        headers = cr.headers
        data = None
        if "application/json" in cr.headers.get("Content-Type", ""):
            data = await cr.json()
        else:
            data = await cr.text()

        request.response = Response(status, headers=headers, data=data)

        return request.response

    async def _process_request(self, request: Request) -> None:
        try:
            response: Response = await self._get_response(request)
            status: int = response.status

            if status // 100 == 2:
                if request.callback is not None:
                    request.callback(response)
                else:
                    raise Exception("无回调函数")
            else:
                raise Exception("请求失败")
        except Exception as e:
            raise e


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
        asyncio_run(self.check_urls())

        return self.data

    async def check_url(self, index: int, session: ClientSession, progress, task_id):
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
        async with ClientSession(headers={"User-Agent": UserAgent().random}) as session:
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
