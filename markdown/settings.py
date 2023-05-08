import os, sys

ZYTUILS = r"/home/netease/Projects/zyutils"  # zyutils项目的根目录的绝对路径

DIRPATH = r"/home/netease/Documents/CS-notes"  # 要处理的Markdown项目根目录的绝对路径
URLP = "https://cdn.jsdelivr.net/gh/zweix123/CS-notes@master/resource"  # 项目使用图床的URL前缀
MODE = "note"  # 模式有["note", "blog", "OSS"], 具体解释见下

"""
关于常量MODE, 指的是图床下的文件结构,  
我们以这样的项目结构（括号中即为目录引用的图片）来解释不同模式的区别   
.
|--OS
|  |--file(file1.jpg, file2.jpg)
|  `--coroutine(coroutine1.jpg, coroutine.jpg)
`--DS
   |---consensus    
   |     |------PacificA()
   |     `------Raft(leader.jpg, copyset.jpg)
   `---storage
         |-----GFS(gfs.jpg)
         `-----Ceph(ceph.png)
1. note: 对于每个文章内的图片, 该文章相对项目根目录的相对路径和图片相对图床的相对路径是一致的.比如  
.
|--OS
|  |---file1.jpg
|  |---file2.jpg
|  |---coroutine1.jpg
|  |---coroutine.jpg
|--DS
    |---consensus
    |       |------leader.jpg
    |       |------copyset.jpg
    |---storage
            |---gfs.jpg
            |---ceph.png
2. blog: 所有图片以所属的文章为单位平铺在图床下  
.
|---file
|    |----file1.jpg
|    `----file2.jpg
|---coroutine
|      |------coroutine1.jpg
|      `------coroutine2.jpg
|---PacificA
|---Raft
|    |---leader.jpg
|    `---copyset.jpg
|---GFS
|    `---gfs.jpg
`---Ceph
     `---ceph.png
3. OSS: 所有图片都平铺在图床下  
.
|--file1.jpg
|--file2.jpg
|--coroutine1.jpg
|--coroutine2.jpg
|--leader.jpg
|--copyset.jpg
|--gfs.jpg
`--ceph.png
"""

assert DIRPATH is not None and DIRPATH.strip() != "", "未填写Markdown项目所在文件路径"
assert os.path.exists(DIRPATH), "Markdown项目目录不存在"
assert URLP is not None and URLP.strip() != "", "未填写图床前缀"
assert MODE in ["note", "blog", "OSS"], "未正确选择图床文件类型"

DIRPATH += os.sep if DIRPATH[-1] != os.sep else ""
URLP += "/" if URLP[-1] != "/" else ""
DIRNAME = DIRPATH.split(os.sep)[-2]  # 拿到Markdown项目根目录目录名
IMGPATHPRE = URLP.split("/")[-2]  # 拿到图床根目录目录名

sys.path.append(ZYTUILS)

del os, sys
