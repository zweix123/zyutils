import re
from urllib.parse import urlparse


# 分辨URL和路径: 判断一个字符串是否为URL
def is_url(string):
    try:
        string = str(string)
    except:
        raise TypeError("expected string or bytes-like object")
    url_regex = re.compile(
        r"^(?:http|ftp)s?://"  # http:// or https:// or ftp:// or ftps://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
        r"localhost|"  # localhost...
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )
    return re.match(url_regex, string) is not None


# 分辨URL和路径: 判断一个字符串是否为路径
def is_path(string):
    result = urlparse(string)
    return not all([result.scheme, result.netloc])
