import os
import pdfplumber  # need ImageMagick, Ghostscript, can install through scoop in win


def pdf_to_imgs(pdfpath: str, distpath: str = os.path.join(".", "images")) -> None:
    """将一个pdf文件分割成一张张图片

    Args:
        pdfpath (str): pdf文件路径
        distpath (str, optional): 切割并转换好的照片保存路径. Defaults to os.path.join(".", "images").
    """
    if os.path.exists(distpath) is False:
        os.mkdir(distpath)

    pdf = pdfplumber.open(pdfpath)
    for i, page in enumerate(pdf.pages):
        # print(page.page_number, page.width, page.height)

        # print(page.extract_text())
        # print(page.extract_table())
        img = page.to_image()
        img.save(os.path.join(distpath, str(i) + ".jpg"))

    pdf.close()
