"""
vnpy官网展示了它对不同交易所在不同系统上的支持, 但是这些是写在各个网关下的, 我想汇总成表格进行比对
"""

import __init__
import re
from bs4 import BeautifulSoup
from util import net_util, rich_util


resp = net_util.get_resp("https://www.vnpy.com/docs/cn/gateway.html")
soup = BeautifulSoup(resp.text, "html.parser")
root = soup.find("div", attrs={"class": "section", "id": "id8"})
targets = root.find_all("div", attrs={"class": "section"})
res = list()
for target in targets:
    if re.match("id.?", target["id"]) is not None:
        continue
    name = target.find("h3").text[:-1]

    systems = [t.text for t in target.find("div").find("li").find_all("li")]
    sorted(systems)

    res.append((name, systems))

inter_data = res

table = list()
table.append(["NAME", "Windows", "Ubuntu", "Mac"])

for name, systems in inter_data:
    mp = dict()
    for system in ["Windows", "Ubuntu", "Mac"]:
        if system in systems:
            mp[system] = "\u2713"
        else:
            mp[system] = ""

    table.append([name] + [v for k, v in mp.items()])

rich_util.print_table(table)
