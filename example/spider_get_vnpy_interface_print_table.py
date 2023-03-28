import sys
from os.path import abspath, dirname

sys.path.append(abspath(dirname(dirname(__file__))))

##

import net_util

resp = net_util.get_resp("https://www.vnpy.com/docs/cn/gateway.html")

##

text = resp.text

from bs4 import BeautifulSoup
import re

soup = BeautifulSoup(text, "html.parser")
root = soup.find("div", attrs={"class": "section", "id": "id8"})
targets = root.find_all("div", attrs={"class": "section"})
res = list()
for target in targets:
    if re.match("id.?", target["id"]) is not None:
        continue
    name = target.find("h3").text[:-1]

    system = [t.text for t in target.find("div").find("li").find_all("li")]
    sorted(system)

    res.append((name, system))

res

##

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

table

##

import show_util

show_util.print_table(table)
