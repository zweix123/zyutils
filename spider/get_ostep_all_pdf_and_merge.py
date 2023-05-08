homepage = "https://pages.cs.wisc.edu/~remzi/OSTEP/"
homepage_tmpfilepath = "page.html"  # 后续会变化
tmpfilepath = ".tmp"
result_filepath = "ostep.pdf"


import os
import shutil
import PyPDF2
import requests
from typing import List
from bs4 import BeautifulSoup, Tag


def end():
    if os.path.exists(tmpfilepath):
        shutil.rmtree(tmpfilepath)


def pre():
    if os.path.exists(result_filepath) is True:
        end()
        exit()
    global tmpfilepath, homepage_tmpfilepath

    if not os.path.exists(tmpfilepath):
        os.mkdir(tmpfilepath)

    homepage_tmpfilepath = os.path.join(tmpfilepath, homepage_tmpfilepath)


pre()
pdf_file_path_s: List[str] = list()


def get_html_code() -> str:
    if os.path.exists(homepage_tmpfilepath) is True:
        with open(homepage_tmpfilepath, "r") as f:
            return f.read()
    else:
        response = requests.get(homepage)
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
        global pdf_file_path_s
        num = num + 1
        if (tag := cell.find("a")) is not None:
            url: str = homepage + tag["href"]
            filepath = os.path.join(".", tmpfilepath, str(num) + url.split("/")[-1])
            pdf_file_path_s.append(filepath)
            if os.path.exists(filepath) is False:
                print(f"下载{filepath}")
                response = requests.get(url)
                with open(filepath, "wb") as f:
                    f.write(response.content)

    return load


loader = g_load()

for row in new_table:
    for cell in row:
        loader(cell)

print("下载完毕")
# 下载完毕

pdf_output = PyPDF2.PdfWriter()
for pdf in pdf_file_path_s:
    print("处理:{}".format(pdf), end=" ")
    pdf_input = PyPDF2.PdfReader(open(pdf, "rb"))
    print("共{}页".format(len(pdf_input.pages)))
    for page in pdf_input.pages:
        pdf_output.add_page(page)
pdf_output.write(open(result_filepath, "wb"))


#

end()
