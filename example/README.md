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
```

### 命令行程序的设计

+ 项目根目录一个入口程序：检查配置，进入命令行cli
+ 在cli检查检查参数并分配权限：
     ```python
     import argparse

     from .command import stats, image, link, table
     # 这个子命令的命令组织部分，下面把管理子命令的权利放权给他们

     parser = argparse.ArgumentParser()
     subparsers = parser.add_subparsers()

     stats.init(subparsers.add_parser("stats", help="项目信息统计"))
     image.init(subparsers.add_parser("image", help="维护项目图床"))
     table.init(subparsers.add_parser("table", help="维护项目目录"))
     link.init(subparsers.add_parser("link", help="维护项目链接"))


     def exec():
          # try:
          #     args = parser.parse_args()
          # except:
          #     parser.print_help()
          #     exit(1)
          args = parser.parse_args()
          if not vars(args):
               parser.print_help()
          else:
               args.func(args)

     ```

+ command中即使这个子命令：
     + 简单的
          ```python
          import src.command.stats as stats
          # 这里引入的是对应命令实现功能的部分


          subparsers = None


          def init(subparsers_):
               global subparsers
               subparsers = subparsers_

               subparsers.set_defaults(func=exec)

               pass


          def exec(args):
               stats.cnt()    
          ```
     + 复杂的：
          ```python
          import src.command.image as image
          # 和上面一样, 引入的是对应命令实现功能的部分

          subparsers = None


          def init(subparsers_):
               global subparsers
               subparsers = subparsers_

               subparsers.set_defaults(func=exec)

               mutually_exclusive_group = subparsers.add_mutually_exclusive_group()
               mutually_exclusive_group.add_argument(
                    "-t", "--transfer", action="store_true", help="使用图床前缀按照模式替换图床链接"
               )
               mutually_exclusive_group.add_argument(
                    "--check", action="store_true", help="检测项目中的失效图床链接"
               )
               mutually_exclusive_group.add_argument(
                    "--clean", action="store_true", help="检测图传中的图床链接, 删除未链接图片，要求图片在本地"
               )


          def exec(args):
               # if [arg for arg in vars(args) if type(arg) == type(True)].count(True) != 1:
               #     subparsers.parse_args(["-h"])
               #     exit()

               if args.transfer is True:
                    image.transfer()
               elif args.check is True:
                    image.check()
               elif args.clean is True:
                    image.clean()
               else:
                    subparsers.parse_args(["-h"])
          ```

+ 关于功能实现的部分，他们在`src/command/`下，每个子命令的各个部分放在一个目录下（的各个文件下），如果各个引入就很麻烦（引入各个文件？引入各个文件中的对应函数？那样不好管理），可以在每个子命令的目录的`__init__.py`各样做（以image为例）
     ```python
     from .transfer import transfer
     from .check import check 
     from .clean import clean

     __all__ = [transfer, check, clean]
     ```

     因为万物皆对象嘛，把核心入口的函数放在这个目录下，然后引入这个目录，就可以想引入一个命令空间一个样这个核心的命令了。