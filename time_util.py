import time, datetime


def get_timestamp(year, month, date, hour, minute, second):
    return int(
        time.mktime(
            datetime.datetime(year, month, date, hour, minute, second).timetuple()
        )
    )
