import time
import requests
import platform
from threading import Thread
from asyncio import (
    get_running_loop,
    new_event_loop,
    set_event_loop,
    run_coroutine_threadsafe,
    all_tasks,
    AbstractEventLoop,
)
from aiohttp import ClientSession, ClientResponse
from dataclasses import dataclass
from typing import Any, Union, Optional, Literal, Callable, Coroutine

if platform.system() == "Windows":
    from asyncio import set_event_loop_policy, WindowsSelectorEventLoopPolicy  # type: ignore

    set_event_loop_policy(WindowsSelectorEventLoopPolicy())

from fake_useragent import UserAgent


@dataclass
class Request:
    def __init__(
        self,
        method: Literal["GET", "POST"],
        url: str,
        params: Optional[dict] = None,
        data: Optional[dict] = None,
        headers: Optional[dict] = None,
        callback: Optional[Callable[["Response", Any], None]] = None,
        extra: Any = None,  # 回调函数使用
        response: Optional["Response"] = None,
    ) -> None:
        self.method: Literal["GET", "POST"] = method
        self.url: str = url
        self.params: Optional[dict] = params
        self.data: Optional[dict] = data
        self.headers: Optional[dict] = headers
        self.callback: Optional[Callable[["Response", Any], None]] = callback
        self.extra = extra
        self.response: Optional["Response"] = response

    def __str__(self) -> str:
        return "{} {} is {}\nparams {}\nheaders{}".format(
            self.method,
            self.url,
            self.response.status if self.response is not None else "terminal",
            self.params,
            self.headers,
        )


@dataclass
class Response:
    def __init__(self, status: int, headers, data: Any) -> None:
        self.status: int = status
        self.headers: str = headers
        self.data: str | dict | bytes = data


class Rail(object):
    def __init__(self: "Rail"):
        self.session: ClientSession = None  # type: ignore
        self.loop: AbstractEventLoop = None  # type: ignore

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

    async def close(self):
        await self.session.close()

    def start(self, session_number: int = 3) -> None:
        try:
            self.loop = get_running_loop()
        except RuntimeError:
            self.loop = new_event_loop()
        Rail.start_event_loop(self.loop)

    def stop(self) -> None:
        if self.session is not None:
            coro: Coroutine = self.close()
            fut = run_coroutine_threadsafe(coro, self.loop)
            fut.result()

        if self.loop and self.loop.is_running():
            self.loop.stop()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def join(self) -> None:
        while len(all_tasks(loop=self.loop)) != 0:
            time.sleep(1)

    def add_request(self, request: Request) -> Request:
        coro: Coroutine = self._process_request(request)
        run_coroutine_threadsafe(coro, self.loop)
        return request

    def request(self, request: Request) -> Response:
        coro: Coroutine = self._get_response(request)
        fut = run_coroutine_threadsafe(coro, self.loop)
        return fut.result()

    @staticmethod
    async def _parse_response(response: ClientResponse) -> Union[dict, str, bytes]:
        content_type = response.headers.get("Content-Type", "")
        if "application/json" in content_type:
            return await response.json()
        elif "text" in content_type:
            return await response.text()
        else:
            return await response.read()

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
        data = await Rail._parse_response(cr)

        request.response = Response(status, headers=headers, data=data)
        return request.response

    async def _process_request(self, request: Request) -> None:
        try:
            response: Response = await self._get_response(request)
            status: int = response.status
            if status // 100 == 2:
                if request.callback is not None:
                    request.callback(response, request.extra)
                else:
                    raise Exception("无回调函数")
            else:
                raise Exception("请求异常, 无法回调")
        except Exception as e:
            raise e


class RailGun(Rail):
    def __init__(self):
        super().__init__()

    def start(self, session_number: int = 3) -> None:
        super().start(session_number)

    def stop(self) -> None:
        super().stop()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def join(self) -> None:
        super().join()

    def fire(self, method: Literal["GET", "POST"], url: str) -> Response:
        request = Request(method, url)
        return self.request(request)


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


"""
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
"""
