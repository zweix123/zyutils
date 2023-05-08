import time, datetime


def milliseconds_to_natural_time(milliseconds: int) -> datetime.datetime:
    # 计算对应的秒数和微秒数
    seconds, microseconds = divmod(milliseconds, 1000)

    # 转换为 datetime 对象
    reference_time = datetime.datetime.utcfromtimestamp(0)
    natural_time = reference_time + datetime.timedelta(seconds=seconds, microseconds=microseconds)  # fmt: skip

    return natural_time


def natural_time_to_milliseconds(natural_time: datetime.datetime) -> int:
    # 计算自然时间和参考时间点之间的时间差
    reference_time = datetime.datetime.utcfromtimestamp(0)
    time_delta = natural_time - reference_time

    # 将时间差转换为总毫秒数
    milliseconds = (time_delta.days * 86400000) + (time_delta.seconds * 1000) + (time_delta.microseconds / 1000)  # fmt: skip

    return int(milliseconds)


def get_now_time() -> datetime.datetime:
    return datetime.datetime.now()


def get_now_timestamp() -> int:
    return int(time.time() * 1000)
