"""
请一定要完成`A + B`, 我按这个判断header对不对的, 早发现早治疗
cookie和header用这个网址生成`https://curlconverter.com/`
代码主要是网页解析
"""
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

cookies = {
    "csrftoken": "RyW98KUri9J4Dbw1RFInBdg1nC0P4QOQWLLaaZXcMwQCAln72ChucBNIxe1J0UOC",
    "sessionid": "j5dywqvx71hs1kudz0pdvcw7eeunkxuz",
}

headers = {
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="8"',
    "sec-ch-ua-mobile": "?0",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 SLBrowser/8.0.0.12022 SLBChan/11",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Referer": "https://www.acwing.com/",
    "Accept-Language": "zh-CN,zh;q=0.9",
    # 'Cookie': 'csrftoken=RyW98KUri9J4Dbw1RFInBdg1nC0P4QOQWLLaaZXcMwQCAln72ChucBNIxe1J0UOC; sessionid=j5dywqvx71hs1kudz0pdvcw7eeunkxuz',
}


def get_page_acwing_problem(index: int, save=False):
    global cookies, headers

    url = "https://www.acwing.com/problem/" + str(index)
    resp = requests.get(url, cookies=cookies, headers=headers)
    # resp = requests.get(url, headers=headers)
    if save is True:
        with open("page.html", "wb") as f:
            f.write(resp.content)
    return resp.text


def get_ele_from_page(page, tag, attrs):
    bs = BeautifulSoup(page, "lxml")
    res = bs.find(tag, attrs=attrs)
    return res


def get_eles_from_page(page, tag, attrs):
    bs = BeautifulSoup(page, "lxml")
    res = bs.find_all(tag, attrs=attrs)
    return res


maxn = get_eles_from_page(
    get_page_acwing_problem("10086"), "a", {"name": "page_turning"}
)[:-1][
    -1
].get_text()  # str

ans = 0

for i in tqdm(range(1, int(maxn) + 1), desc="Processing"):
    page = get_page_acwing_problem(i)

    bs = BeautifulSoup(page, "lxml")
    tmp = bs.find("table", attrs={"class": "table table-striped table-responsive"})
    if tmp is None:
        break
    tar = tmp.find("tbody")
    table = tar.find_all("tr")

    for ele in table:
        if ele.find("td").find("span") is not None:
            ans = ans + 1

    if i == 1 and ans == 0:
        raise Exception("出锅啦, 我怀疑你的cookie和header不对")

print(ans)
