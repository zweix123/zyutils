import re
from typing import Callable


def process_images(content: str, func: Callable[[str], str]) -> str:
    """提取一份Markdown格式的文本中的所有图片链接, 通过提供的处理函数进行转换并嵌入回原文本中  
       可用于切换图床

    Args:
        content (str): Mardown文本
        func (Callable[[str], str]): 处理每个图片链接的函数, 返回转换后的图片

    Returns:
        str: 返回处理好(修改图片链接)的Markdown文本
    """
    pattern = r"!\[.*?\]\((.*?)\)|<img.*?src=[\'\"](.*?)[\'\"].*?>"

    def modify(match):
        link = match.group(1) or match.group(2)
        return str(func(link)).join(match.group().split(link))

    return re.sub(pattern, modify, content)


def get_image_link(content: str) -> list[str]:
    patterns = [r"!\[.*?\]\((.*?)\)", r"<img.*?src=[\'\"](.*?)[\'\"].*?>"]
    flags = re.IGNORECASE | re.DOTALL
    links = [re.findall(pattern, content, flags=flags) for pattern in patterns]
    return [link for link_list in links for link in link_list if link.strip()]


def get_not_image_link(content: str) -> list[str]:
    pattern = r"\[(.*?)\]\((.*?)\)"
    flags = re.IGNORECASE | re.DOTALL
    extensions = (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp")
    links = (link.group(2) for link in re.finditer(pattern, content, flags=flags))
    return [link for link in links if not link.endswith(extensions)]
