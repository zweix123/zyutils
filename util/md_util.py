import re, functools
from typing import Callable


def process_images(content: str, func: Callable[[str], str]) -> str:
    """处理内容为Markdown的字符串中的图片链接, 返回处理过的字符串

    Args:
        content (str): 处理内容为Markdown的字符串
        func (Callable[[str], str]): 处理图片链接的函数, 该函数接受图片链接字符串, 返回一个字符串

    Returns:
        str: _description_
    """

    def modify(match):
        # 下面是黑盒魔法
        tar = match.group()
        pre, mid, suf = str(), str(), str()
        if tar[-1] == ")":
            pre = tar[: tar.index("(") + 1]
            mid = tar[tar.index("(") + 1 : -1]
            suf = tar[-1]
        else:
            mid = re.search(r'src="([^"]*)"', tar).group(1)
            pre, suf = tar.split(mid)

        link = mid
        # 黑盒魔法结束, link即为一个图片链接
        return pre + func(link) + suf  # 这里不能修改

    patten = r"!\[.*?\]\((.*?)\)|<img.*?src=[\'\"](.*?)[\'\"].*?>"
    return re.sub(patten, modify, content)


def get_image_link(content: str) -> list[str]:
    # 优雅! 函数式编程太优雅了!
    return functools.reduce(
        lambda x, y: x + y,
        [
            list(filter(str.strip, re.findall(pattern, content)))
            for pattern in [r"!\[.*?\]\((.*?)\)", r"<img.*?src=[\'\"](.*?)[\'\"].*?>"]
        ],
    )


def get_not_image_link(content: str) -> list[str]:
    return [
        link[1]
        for link in re.findall(r"\[(.*?)\]\((.*?)\)", content)
        if not link[1].endswith(
            (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp")
        )  # 一方面, 这里可能不全, 另一方面, 有的图片链接并不以后缀名区分, 所以这个函数是有bug的
    ]
