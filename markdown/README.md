每个脚本前有配置信息，要按要求填好，不然会报错（虽然我assert了）


下面是`md-admin`中配置文件内容
```python
DIRPATH = r"/home/netease/Documents/CS-notes"  # 要处理的Markdown项目根目录的绝对路径
URLP = "https://cdn.jsdelivr.net/gh/zweix123/CS-notes@master/resource"  # 项目使用图床的URL前缀
MODE = "note"  # 模式有["note", "blog", "OSS"], 具体解释见下
"""
关于常量MODE, 指的是图床下的文件结构, 我们以这样的项目结构（括号中即为目录引用的图片）来解释不同模式的区别   
.
|--os
|  |--file(file1.jpg, file2.jpg)
|  `--coroutine(coroutine1.jpg, coroutine.jpg)
|--DS
   |---consensus    
   |     |------PacificA()
   |     |------Raft(leader.jpg, copyset.jpg)
   `--storage
         |-----GFS(gfs.jpg)
         `-----Ceph(ceph.png)
1. note: 对于每个文章内的图片, 该文章相对项目根目录的相对路径和图片相对图床的相对路径是一致的.比如  
.
|--os
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

import os

if DIRPATH[-1] != os.sep:
    DIRPATH += os.sep

if URLP[-1] != "/":
    URLP += "/"

DIRNAME = DIRPATH.split(os.sep)[-2]

IMGPATHPRE = URLP.split(os.sep)[-2]


def check_cnt():
    if DIRPATH is None or DIRPATH == "":
        print("请填写项目所在文件路径")
        return False
    if os.path.exists(DIRPATH) is False:
        print("项目目录不存在")
        return False
    return True


def check_perl():
    if check_cnt() is False:
        return False
    if URLP is None or URLP == "":
        print("请填写图床前缀")
        return False
    if MODE not in ["note", "blog", "OSS"]:
        print("请查看图床路径前缀是否填写或填写是否正确")
        return False
    return True


def check():
    return check_cnt() and check_perl()

if check() is False:
     exit(0)
```