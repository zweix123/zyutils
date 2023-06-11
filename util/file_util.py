import os, json, csv, chardet, shutil, uuid
from typing import Optional, Any, Literal


def get_filepaths_under_dir(
    folerpath: str, suffix_name: Optional[str] = None
) -> list[str]:
    """返回目录folderpath下后缀名为suffix_name的所有文件的绝对路径列表"""
    return sorted(
        [
            os.path.abspath(os.path.join(dirpath, filename))
            for dirpath, dirnames, filenames in os.walk(folerpath)
            for filename in filenames
            if suffix_name is None or str(filename).endswith("." + suffix_name)
        ],
        key=lambda filepath: int(".".join(os.path.basename(filepath).split(".")[:-1])),
    )


def get_file_encode(filepath: str) -> Optional[str]:
    """检测文件编码格式, 效率较低"""
    res: Optional[str] = str()
    with open(filepath, "rb") as f:
        res = chardet.detect(f.read())["encoding"]
    return res


def read(filepath: str, type: Literal["type", "json", "csv"] = "type") -> Any:
    # 读取文本文件内容
    if not os.path.exists(filepath):
        raise Exception("The path {} is not exists".format(filepath))

    if type == "type":
        with open(filepath, "r", encoding=get_file_encode(filepath)) as f:
            return f.read()
    elif type == "json":
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    elif type == "csv":
        with open(filepath, "r", encoding="utf-8", newline="") as f:
            return list(csv.reader(f))
    else:
        raise Exception("The type '{}' is not exists".format(type))


def write(filepath: str, data: Any) -> None:
    # 向文件(覆)写内容(性能极低), 通过类型区分写入文件类型
    if isinstance(data, str) or isinstance(data, dict):
        with open(
            file=filepath,
            mode="w",
            encoding=get_file_encode(filepath)
            if os.path.exists(filepath) is True
            else None,
        ) as f:
            if isinstance(data, str):
                f.write(data)
            elif isinstance(data, dict):
                f.write(json.dumps(data))
    elif isinstance(data, list):
        with open(filepath, "w", encoding="utf-8", newline="") as f:
            csv.writer(f).writerows(data)
    else:
        raise TypeError("Unsupported data type")


def mkdir(folder_path):  # 加一个预检防止覆盖
    if os.path.exists(folder_path) is False:
        os.mkdir(folder_path)


def get_abspath(basefile: str, filepath: str) -> str:  # 从绝对路径变化成相对路径且符合当前的操作系统
    return os.path.normpath(os.path.join(os.path.dirname(basefile), filepath))


def get_image_to_target(link: str, from_filepath: str, target_foldpath: str) -> str:
    import util.str_util as str_util, util.net_util as net_util

    # 对于from_filepath(请使用其绝对地址)中的图床链接link, 它可能是url、绝对地址或相对地址, 我们会get它然后重命名并放到target_foldpath下, 并返回重命名后的名字
    # 这里对图片类型的判断是通过link的后缀名, 有些图片的url的末尾不是类型名, 就会有bug
    name = uuid.uuid4().hex + "." + link.split(".")[-1]
    if str_util.is_path(link) and not os.path.isabs(link):
        link = get_abspath(from_filepath, link)
    if str_util.is_url(link):
        net_util.down(link, os.path.join(target_foldpath, name))
    else:
        if os.path.exists(link) is False:
            print("该路径不存在: ", link)
            return name
        shutil.copyfile(link, os.path.join(target_foldpath, name))

    return name
