"""
《Build Your Own Redis with C/C++》是一个全开源的书籍, 可以线上阅读, 但是online的形式不容易做笔记, 我希望有PDF版本的  
我的思路是, 收集每个章节的内容, 然后拼接到一个网页中, 这样就能在一个页面查看所有章节的了, 然后再用safari将其导出成pdf

值得一提的是
+ 取出不必要的Tag
+ 对于章节末尾的代码的链接, 为了让导出的pdf里仍然能使用链接, 将href转换成对应tag的string
"""

import __init__
from util.net_util import RailGun
from bs4 import BeautifulSoup, Tag

with RailGun() as railgun:
    base_url = "https://build-your-own.org/redis/"
    content_url = "https://build-your-own.org/redis/#table-of-contents"

    content_page = railgun.fire("GET", content_url).data  # get content html

    bs: Tag = BeautifulSoup(content_page, "html.parser")
    # parser content page to get links
    links = [
        base_url + li_page.get("href")
        for ol_page in bs.find("div", attrs={"class": "body"}).find_all("ol")[:2]
        for li_page in ol_page.find_all("a")
    ]

    # loop links and get need part and aapend to sum
    sum_page = Tag(name="body")
    for i, chapter_url in enumerate(links):
        print(chapter_url)
        chapter_page = railgun.fire("GET", chapter_url).data
        bs = BeautifulSoup(chapter_page, "html.parser")
        body_tag = bs.find("div", attrs={"class": "body"})

        del body_tag["class"]

        blockquote = body_tag.find("blockquote")
        if blockquote is not None:
            ref_base_url = "https://build-your-own.org"
            for a_tag in blockquote.find_all("a"):
                a_tag["class"] = "uri"
                # 获取原始的 href 属性值
                href = a_tag["href"]

                # 拼接新的 href 属性值
                new_href = ref_base_url + href

                # 更新 href 属性
                a_tag["href"] = new_href

                a_tag.string = a_tag["href"]

        sum_page.append(body_tag)

# unified delete thing not need
for codecrafters_tag in sum_page.find_all("div", attrs={"class": "codecrafters"}):
    codecrafters_tag.extract()

# insert origin page
bs = BeautifulSoup(content_page, "html.parser")
bs.find("div", attrs={"class": "body"}).replace_with(sum_page)


for tag in bs.find_all("div", attrs={"class": "prev-toc-next"}):
    tag.extract()

# write
with open("BuildYourOwnRediswithCandCPP2.html", "w") as f:
    f.write(str(bs))
