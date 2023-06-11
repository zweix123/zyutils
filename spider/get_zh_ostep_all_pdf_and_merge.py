import __init__
import os, re, shutil
import PyPDF2
from rich.progress import track
from util import net_util
from typing import Any

tmp_filename = ".tmp"
result_filename = "ostep.pdf"
raw_text = """| [Preface](http://ostep.org/Chinese/preface.pdf) | 3 [Dialogue](http://ostep.org/Chinese/03.pdf) | 12 [Dialogue](http://ostep.org/Chinese/12.pdf) | 25 [Dialogue](http://ostep.org/Chinese/25.pdf) | 35 [Dialogue](http://ostep.org/Chinese/35.pdf) | [Dialogue](http://ostep.org/Chinese/fla.pdf) | 
| [TOC](http://ostep.org/Chinese/toc.pdf) | 4 [Processes](http://ostep.org/Chinese/04.pdf) | 13 [Address Spaces](http://ostep.org/Chinese/13.pdf) | 26 [Concurrency and Threads](http://ostep.org/Chinese/26.pdf) | 36 [I/O Devices](http://ostep.org/Chinese/36.pdf) | [Virtual Machines](http://ostep.org/Chinese/flb.pdf) | 
| 1 [Dialogue](http://ostep.org/Chinese/01.pdf) | 5 [Process API](http://ostep.org/Chinese/05.pdf) | 14 [Memory API](http://ostep.org/Chinese/14.pdf) | 27 [Thread API](http://ostep.org/Chinese/27.pdf) | 37 [Hard Disk Drives](http://ostep.org/Chinese/37.pdf) | [Dialogue](http://ostep.org/Chinese/flc.pdf) | 
| 2 [Introduction](http://ostep.org/Chinese/02.pdf) | 6 [Direct Execution](http://ostep.org/Chinese/06.pdf) | 15 [Address Translation](http://ostep.org/Chinese/15.pdf) | 28 [Locks](http://ostep.org/Chinese/28.pdf) | 38 [Redundant Disk Arrays (RAID)](http://ostep.org/Chinese/38.pdf) | | 
|  | 7 [CPU Scheduling](http://ostep.org/Chinese/07.pdf) | 16 [Segmentation](http://ostep.org/Chinese/16.pdf) | 29 [Locked Data Structures](http://ostep.org/Chinese/29.pdf) | 39 [Files and Directories](http://ostep.org/Chinese/39.pdf) | [Dialogue](http://ostep.org/Chinese/fld.pdf) | 
|  | 8 [Multi-level Feedback](http://ostep.org/Chinese/08.pdf) | 17 [Free Space Management](http://ostep.org/Chinese/17.pdf) | 30 [Condition Variables](http://ostep.org/Chinese/30.pdf) | 40 [File System Implementation](http://ostep.org/Chinese/40.pdf) | [Lab Tutorial](http://ostep.org/Chinese/fle.pdf) | 
|  | 9 [Lottery Scheduling](http://ostep.org/Chinese/09.pdf) | 18 [Introduction to Paging](http://ostep.org/Chinese/18.pdf) | 31 [Semaphores](http://ostep.org/Chinese/31.pdf) | 41 [Fast File System (FFS)](http://ostep.org/Chinese/41.pdf) | [Systems Labs](http://ostep.org/Chinese/flf.pdf) | 
|  | 10 [Multi-CPU Scheduling](http://ostep.org/Chinese/10.pdf) | 19 [Translation Lookaside Buffers](http://ostep.org/Chinese/19.pdf) | 32 [Concurrency Bugs](http://ostep.org/Chinese/32.pdf) | 42 [FSCK and Journaling](http://ostep.org/Chinese/42.pdf) | [xv6 Labs](http://ostep.org/Chinese/flg.pdf) | 
|  | 11 [Summary](http://ostep.org/Chinese/11.pdf) | 20 [Advanced Page Tables](http://ostep.org/Chinese/20.pdf) | 33 [Event-based Concurrency](http://ostep.org/Chinese/33.pdf) | 43 [Log-Structured File System (LFS)](http://ostep.org/Chinese/43.pdf) |  | 
|  |  | 21 [Swapping: Mechanisms](http://ostep.org/Chinese/21.pdf) | 34 [Summary](http://ostep.org/Chinese/34.pdf) | 44 [Data Integrity and Protection](http://ostep.org/Chinese/44.pdf) |  | 
|  |  | 22 [Swapping: Policies](http://ostep.org/Chinese/22.pdf) |  | 45 [Summary](http://ostep.org/Chinese/45.pdf) |  | 
|  |  | 23 [Complete VM Systems](http://ostep.org/Chinese/23.pdf) |  | 46 [Dialogue](http://ostep.org/Chinese/46.pdf) |  | 
|  |  | 24 [Summary](http://ostep.org/Chinese/24.pdf) |  | 47 [Distributed Systems](http://ostep.org/Chinese/47.pdf) |  | 
|  |  |  |  | 48 [Network File System (NFS)](http://ostep.org/Chinese/48.pdf) |  | 
|  |  |  |  | 49 [Andrew File System (AFS)](http://ostep.org/Chinese/49.pdf) |  | 
|  |  |  |  | 50 [Summary](http://ostep.org/Chinese/50.pdf) |  | """

if os.path.exists(result_filename) is True:
    if os.path.exists(tmp_filename) is True:
        shutil.rmtree(tmp_filename)
        exit()

if not os.path.exists(tmp_filename):
    os.mkdir(tmp_filename)

tmp_table: list[list[str]] = [[] for _ in range(6)]
for line in raw_text.split("\n"):
    for i, cell in enumerate(line.strip()[1:-1].split("|")):
        tmp_table[i].append(cell)


def pick(text: str):
    text = text.strip()
    assert text != ""
    match = re.search(r"https?://[\w./-]+", text)
    assert match is not None
    return match.group(0)


tasks = [pick(cell.strip()) for col in tmp_table for cell in col if cell.strip() != ""]
pdf_tasks = []


def load(response: net_util.Response, extra: Any) -> None:
    filepath = os.path.join(tmp_filename, str(extra) + ".pdf")
    global pdf_tasks
    pdf_tasks.append(filepath)
    print(f"{filepath}下载完毕")
    with open(filepath, "wb") as f:
        assert isinstance(response.data, bytes)
        f.write(response.data)


with net_util.Rail() as rail:
    print("开始下载")
    for i, task in enumerate(tasks):
        print(task)
        filepath = os.path.join(tmp_filename, str(i) + ".pdf")
        pdf_tasks.append(filepath)
        if os.path.exists(filepath) is True:  # 不重复下载
            print(f"{filepath}已经下载")
            continue
        request = net_util.Request("GET", task, callback=load, extra=i)
        rail.add_request(request)
    print("等待下载")
    rail.join()


pdf_output = PyPDF2.PdfWriter()
for pdf in track(pdf_tasks, description="合成中..."):
    print("处理:{}".format(pdf), end=" ")
    pdf_input = PyPDF2.PdfReader(open(pdf, "rb"))
    print("共{}页".format(len(pdf_input.pages)))
    for page in pdf_input.pages:
        pdf_output.add_page(page)
pdf_output.write(open(result_filename, "wb"))

shutil.rmtree(tmp_filename)
