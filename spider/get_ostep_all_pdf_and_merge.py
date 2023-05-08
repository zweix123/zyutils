homepage_url = "https://pages.cs.wisc.edu/~remzi/OSTEP/"
result_filename = "ostep.pdf"


import __init__

import os
import shutil
import PyPDF2
from typing import List
from bs4 import BeautifulSoup, Tag
from rich.progress import track
from util import net_util


tmpfilepath = ".zmp"
homepage_tmpfilepath = "page.html"  # 后续会变化


def pre_code():
    if os.path.exists(result_filename) is True:
        suf_code()
        exit()
    global tmpfilepath, homepage_tmpfilepath
    if not os.path.exists(tmpfilepath):
        os.mkdir(tmpfilepath)
    homepage_tmpfilepath = os.path.join(tmpfilepath, homepage_tmpfilepath)


def suf_code():
    if os.path.exists(tmpfilepath):
        shutil.rmtree(tmpfilepath)


pre_code()
tmp_pdf_file_path_s: List[str] = list()


def get_html_code() -> str:
    if os.path.exists(homepage_tmpfilepath) is True:
        with open(homepage_tmpfilepath, "r") as f:
            return f.read()
    else:
        response = net_util.get_resp(homepage_url)
        with open(homepage_tmpfilepath, "wb") as f:
            f.write(response.content)
        return response.text


html_code = get_html_code()
bs = BeautifulSoup(html_code, "html.parser")

main = bs.find("body").find("center").find("table").find_all("tr")[6].find("center")
table: Tag = main.find("table")

new_table: List[List[Tag]] = [[] for _ in range(6)]

for row in table.find_all("tr"):
    for i, col in enumerate(row.find_all(["td", "th"])):
        new_table[i].append(col)


def g_load():
    num = 0

    def load(cell: Tag):
        nonlocal num
        global tmp_pdf_file_path_s
        num = num + 1
        if (tag := cell.find("a")) is not None:
            url: str = homepage_url + tag["href"]
            filepath = os.path.join(".", tmpfilepath, str(num) + url.split("/")[-1])
            tmp_pdf_file_path_s.append(filepath)
            if os.path.exists(filepath) is False:
                print(f"下载{filepath}")
                response = net_util.get_resp(url)
                with open(filepath, "wb") as f:
                    f.write(response.content)

    return load


loader = g_load()

tasks = [cell for row in new_table for cell in row]
for task in track(tasks, description="正在下载..."):
    loader(task)

#

pdf_output = PyPDF2.PdfWriter()
for pdf in track(tmp_pdf_file_path_s, description="正在合成..."):
    print("处理:{}".format(pdf), end=" ")
    pdf_input = PyPDF2.PdfReader(open(pdf, "rb"))
    print("共{}页".format(len(pdf_input.pages)))
    for page in pdf_input.pages:
        pdf_output.add_page(page)
pdf_output.write(open(result_filename, "wb"))

#

suf_code()
