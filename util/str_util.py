import os, re


# 判断一个字符串是否为URL
def is_url(s: str) -> bool:
    url_regex = re.compile(
        r"^(?:http|ftp)s?://"  # http:// or https:// or ftp:// or ftps://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
        r"localhost|"  # localhost...
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )
    return re.match(url_regex, s) is not None


# 判断一个字符串是否为路径
def is_path(s: str) -> bool:
    return os.path.isdir(s) or os.path.isfile(s)


def str_class(s: str) -> str:
    if is_url(s):
        return "URL"
    elif is_path(s):
        return "PATH"
    else:
        return "None"
