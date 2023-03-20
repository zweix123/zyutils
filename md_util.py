import re, functools


def process_images(content, func):
    """处理Markdown类型字符串中的图片链接, 返回处理过图片链接部分的Markdown字符串

    Args:
        content (_type_): Markdown类型字符串
        func (_type_): 处理图片链接的函数, 该函数接受图片链接, 返回一个有关图片链接的新串
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
        # 黑盒魔法结束
        return pre + func(link) + suf

    patten = r"!\[.*?\]\((.*?)\)|<img.*?src=[\'\"](.*?)[\'\"].*?>"
    return re.sub(patten, modify, content)


def get_image_link(content):
    # 优雅! 太优雅了!
    return functools.reduce(
        lambda x, y: x + y,
        [
            list(filter(str.strip, re.findall(pattern, content)))
            for pattern in [r"!\[.*?\]\((.*?)\)", r"<img.*?src=[\'\"](.*?)[\'\"].*?>"]
        ],
    )


def get_not_image_link(content):
    return [
        link[1]
        for link in re.findall(r"\[(.*?)\]\((.*?)\)", content)
        if not link[1].endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"))
    ]

    # return list(filter(str.strip, re.findall(r"\[(.*?)\]\((.*?)\)", content)))


# from markdown import markdown
# from markdown import Extension
# from markdown.blockprocessors import BlockProcessor
# import xml.etree.ElementTree as etree


# def md_to_html(md: str) -> str:
#     class BoxBlockProcessor(BlockProcessor):
#         first = True

#         def run(self, parent, blocks):
#             if self.first:
#                 self.first = False
#                 e = etree.SubElement(parent, "div")
#                 self.parser.parseBlocks(e, blocks)
#                 for _ in range(0, len(blocks)):
#                     blocks.pop(0)
#                 return True
#             return False

#     class BoxExtension(Extension):
#         def extendMarkdown(self, md):
#             md.parser.blockprocessors.register(BoxBlockProcessor(md.parser), "box", 175)

#     extensions = [
#         BoxExtension(),
#         "meta",
#         "fenced_code",
#         "codehilite",
#         # "extra",
#         "attr_list",
#         "tables",
#         # "toc",
#     ]
#     return markdown(md, extensions=extensions)
