"""
收集在acwing上的总总做题数
请一定要完成`A + B`, 我按这个判断header对不对的, 早发现早治疗
找到题库页面, 打开F12, 打开Network选项卡, 刷新页面, Filter problem, 右键, Copy, as CURL, 然后装贴到`https://curlconverter.com/`, 将生成的cookies和headers替换下面代码
代码主要是网页解析
"""
import __init__
import requests
from bs4 import BeautifulSoup, Tag
from rich.progress import track

cookies = {
    "csrftoken": "tp2ImAOP20umc3rJLIfpzCvqC3FrplDEyyynDis22so5zC6oh1v8J9phZjwbvdvc",
    "sessionid": "qdzcz3u0n4g4r4p7v1e8vpkvtz9ww2t7",
}

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    # 'Cookie': 'csrftoken=tp2ImAOP20umc3rJLIfpzCvqC3FrplDEyyynDis22so5zC6oh1v8J9phZjwbvdvc; sessionid=qdzcz3u0n4g4r4p7v1e8vpkvtz9ww2t7',
    "Pragma": "no-cache",
    "Referer": "https://www.acwing.com/",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "sec-ch-ua": '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
}


def get_page_acwing_problem(index: int):
    global cookies, headers

    url = "https://www.acwing.com/problem/" + str(index)
    resp = requests.get(url, cookies=cookies, headers=headers)
    return resp.text


def get_tag_from_page(page: str, tag: str, attrs: dict) -> Tag:
    return BeautifulSoup(page, "html.parser").find(tag, attrs=attrs)


def get_tags_from_page(page: str, tag: str, attrs: dict) -> list[Tag]:
    return BeautifulSoup(page, "html.parser").find_all(tag, attrs=attrs)


if __name__ == "__main__":
    maxn: int = int(get_tags_from_page(get_page_acwing_problem(10086), "a", {"name": "page_turning"})[:-1][-1].get_text())  # fmt: skip
    num: int = 0
    for i in track(range(1, int(maxn) + 1)):
        page = get_page_acwing_problem(i)
        bs = BeautifulSoup(page, "html.parser")
        if (table := bs.find("table", attrs={"class": "table table-striped table-responsive"})) is None:  # fmt: skip
            break
        tar = table.find("tbody")
        table = tar.find_all("tr")

        for ele in table:
            if ele.find("td").find("span") is not None:
                num = num + 1

        if i == 1 and num == 0:
            raise Exception("出锅啦, 我怀疑你的cookie和header不对")

    print("共做完", num, "个题目")
