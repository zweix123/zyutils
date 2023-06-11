import time, datetime
from dateutil import parser
from typing import Optional


def str2datetime(date_string: str) -> datetime.datetime:
    return parser.parse(date_string)


def milliseconds2naturaltime(milliseconds: int) -> datetime.datetime:
    # 计算对应的秒数和微秒数
    seconds, microseconds = divmod(milliseconds, 1000)

    # 转换为 datetime 对象
    reference_time = datetime.datetime.utcfromtimestamp(0)
    natural_time = reference_time + datetime.timedelta(seconds=seconds, microseconds=microseconds)  # fmt: skip

    return natural_time


def naturaltime2milliseconds(natural_time: str | datetime.datetime) -> int:
    if isinstance(natural_time, str):
        natural_time = parser.parse(natural_time)

    # 计算自然时间和参考时间点之间的时间差
    reference_time = datetime.datetime.utcfromtimestamp(0)
    time_delta = natural_time - reference_time

    # 将时间差转换为总毫秒数
    milliseconds = (time_delta.days * 86400000) + (time_delta.seconds * 1000) + (time_delta.microseconds / 1000)  # fmt: skip

    return int(milliseconds)


def get_now_time(
    format_str: Optional[str] = "%Y-%m-%d %H:%M:%S",
) -> datetime.datetime | str:
    if not format_str:
        return datetime.datetime.now()
    else:
        return datetime.datetime.now().strftime(format_str)


def get_now_timestamp() -> int:
    return int(time.time() * 1000)
