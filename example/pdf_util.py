import PyPDF2


def select_pdf(pdf: str, select_str: str = "", outputpath: str = None) -> None:
    """切分pdf文件, 具体的, 通过选择表达式选择想要的PDF页面
    选择表达式:
        1: 选择第一页
        1 | 2 | 5: 选择第一页、第二页和第五页
        1-3 | 5: 选择第一页、第二页、第三页和第五页

    Args:
        pdf (str): pdf文件路径
        select_str (str, optional): 选择表达式. Defaults to "".
        outputpath (str, optional): 输出剪切好的pdf的文件路径. Defaults to None.

    Raises:
        Exception: _description_
        Exception: _description_
    """
    # 解析select表达式
    sections = list(map(str.strip, select_str.split("|")))
    target_list = list()
    for section in sections:
        if section == "":
            continue
        if "-" in section:
            start, end = map(int, section.split("-"))
            target_list += list(range(start, end + 1))
        else:
            target = int(section)
            target_list.append(target)
    if len(target_list) == 0:
        raise Exception("没有选择页码")
    pro_pdf = PyPDF2.PdfReader(open(pdf, "rb"))
    length = len(pro_pdf.pages)
    if all(1 <= index <= length for index in target_list) is False:
        raise Exception("页面的选择超过PDF文件页数")
    res_pdf = PyPDF2.PdfWriter()
    for index in target_list:
        res_pdf.add_page(pro_pdf.pages[index])
    if outputpath is None:
        outputpath = "".join(pdf.split(".")[:-1]) + "_selected.pdf"
    res_pdf.write(open(outputpath, "wb"))


def merge_pdfs(pdfs: list[str], outputpath: str = "Result.pdf"):
    """合并多个pdf文件

    Args:
        pdfs (list[str]): 各个pdf文件路径列表
        outputpath (_type_): 合并后的pdf文件的保存路径(包括路径和文件名)
    """
    pdf_output = PyPDF2.PdfWriter()
    for pdf in pdfs:
        print("处理:{}".format(pdf), end=" ")
        pdf_input = PyPDF2.PdfReader(open(pdf, "rb"))
        print("共{}页".format(len(pdf_input.pages)))
        for page in pdf_input.pages:
            pdf_output.add_page(page)
    pdf_output.write(open(outputpath, "wb"))


import os, pdfplumber  # scoop ImageMagick, Ghostscript


def pdf_to_imgs(pdfpath: str, distpath: str = os.path.join(".", "imgs")) -> None:
    """将一个pdf文件分割成一张张图片

    Args:
        pdfpath (str): pdf文件路径
        distpath (str, optional): 切割并转换好的照片保存路径. Defaults to os.path.join(".", "imgs").
    """
    if os.path.exists(distpath) is False:
        os.mkdir(distpath)

    pdf = pdfplumber.open(pdfpath)
    for i, page in enumerate(pdf.pages):
        print(i)
        # print(page.page_number, page.width, page.height)
        # print(page.extract_text())
        # print(page.extract_table())
        img = page.to_image()
        img.save(os.path.join(distpath, str(i) + ".jpg"))

    pdf.close()
