import re
from typing import Callable


def process_images(content: str, func: Callable[[str], str]) -> str:
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
