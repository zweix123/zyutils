import __init__
from util.net_util import RailGun
from bs4 import BeautifulSoup, Tag

with RailGun() as railgun:
    root_url = "https://build-your-own.org/redis/"  # root url
    content_page_url = (
        "https://build-your-own.org/redis/#table-of-contents"  # content url
    )

    content_page = railgun.fire("GET", content_page_url).data  # spider

    bs: Tag = BeautifulSoup(content_page, "html.parser")
    links = [
        root_url + li_page.get("href")
        for ol_page in bs.find("div", attrs={"class": "body"}).find_all("ol")[:2]
        for li_page in ol_page.find_all("a")
    ]
    # links is all chapter url

    sum_page = Tag(name="body")
    for chapter_url in links:
        print(chapter_url)
        chapter_page = railgun.fire("GET", chapter_url).data
        bs = BeautifulSoup(chapter_page, "html.parser")
        sum_page.append(bs.find("div", attrs={"class": "body"}))

    # 删除每个文章尾多余的东西
    for codecrafters_tag in sum_page.find_all("div", attrs={"class": "codecrafters"}):
        codecrafters_tag.extract()

    bs = BeautifulSoup(content_page, "html.parser")
    bs.find("div", attrs={"class": "body"}).replace_with(sum_page)

    with open("BuildYourOwnRediswithCandCPP2.html", "w") as f:
        f.write(bs.prettify())
