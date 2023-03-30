"""
请一定要完成`A + B`, 我按这个判断header对不对的, 早发现早治疗
找到题库页面, 打开F12的network, 刷新页面找到problem的信息, 右键它找到copy
cookie和header用这个网址生成`https://curlconverter.com/`
代码主要是网页解析
"""
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

cookies = {
    "csrftoken": "2eDR1yFE7RA1VQhJ90eoipCLuqQClaErtrgY0JKyjIb1308mMSt6rDBLnMtAthOA",
    "sessionid": "x2soy6vlka5kd85i54fakc3ytmjetn6g",
    "file_305565_readed": '""',
}

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    # 'Cookie': 'csrftoken=2eDR1yFE7RA1VQhJ90eoipCLuqQClaErtrgY0JKyjIb1308mMSt6rDBLnMtAthOA; sessionid=x2soy6vlka5kd85i54fakc3ytmjetn6g; file_305565_readed=""',
    "Referer": "https://www.acwing.com/about/",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "sec-ch-ua": '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
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
    bs = BeautifulSoup(page, "html.parser")
    res = bs.find(tag, attrs=attrs)
    return res


def get_eles_from_page(page, tag, attrs):
    bs = BeautifulSoup(page, "html.parser")
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

    bs = BeautifulSoup(page, "html.parser")
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