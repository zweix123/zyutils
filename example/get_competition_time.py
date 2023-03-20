import os
import time
import requests
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup as bs


class SpiderByRequests:
    def __init__(self):
        # ua池
        user_anent = UserAgent(path=os.path.join(
            os.getcwd(), "fake_useragent_0.1.11.json")).random  # ua池
        self.headers = {"User-Agent": user_anent}
        # ip池

    def __call__(self, url):
        resp = requests.get(url=url, headers=self.headers)
        resp.encoding = resp.apparent_encoding  # 设置编码
        return resp


class SpiderBySelenium:
    def __init__(self):
        options = Options()
        options.add_argument('--headless')  # 设置chrome浏览器无界面模式
        self.driver = webdriver.Chrome(executable_path=os.path.join(
            os.getcwd(), "chromedriver.exe"), chrome_options=options)
        self.TIME = 5  # 等待页面加载时间
        # 【Selenium】关闭INFO:CONSOLE提示: https://blog.csdn.net/Spade_/article/details/105903246

    def __call__(self, url):
        self.driver.get(url)
        time.sleep(self.TIME)
        return self.driver.page_source

    def __del__(self):
        self.driver.quit()


class Game:
    def __init__(self, sponsor: str, start_time, duration: int) -> None:
        self.sponsor = sponsor
        self.start_time = start_time
        self.duration = duration

    def __str__(self) -> str:
        return ""


def get_luogu():
    # 洛谷: https://www.luogu.com.cn/contest/list
    html = SpiderBySelenium()("https://www.luogu.com.cn/contest/list")
    # with open("page.html", 'w', encoding="utf-8") as f:
    #     f.write(html)
    bench = bs(html, "lxml")
    games = bench.find_all(name="div", attrs={"class": "row"})
    for game in games:
        status = game.find("span", attrs={"class": "status"}).get_text().strip()
        if status == "未开始":
            name = game.find("a", attrs={"class": "name color-default"}).get_text().strip()
            time_and_duration = game.find("span", attrs={"class": "time"}).get_text().strip()
            print(name, time_and_duration)
            pass
        
        
        break
    
    pass


if __name__ == '__main__':
    get_luogu()
    pass


# taskkill /im chrome.exe /F
# taskkill /im chromedriver.exe /F


"""
牛客: https://ac.nowcoder.com/acm/contest/vip-index
codeforces: https://codeforces.com/contests
AtCoder: https://atcoder.jp/contests/
acwing: https://www.acwing.com/activity/1/competition/
力扣: https://leetcode.cn/contest/
"""
