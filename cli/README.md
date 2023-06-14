我们以实现一个Markdown项目管理工具为例讲解一个命令行工具项目的架构

+ 需求分析
     >我们显然可以对每一个功能都写一个脚本来实现，但是那样实现的项目是很不容易扩展的

     我们的设计是把命令分成命令、参数和标记，而命令分成根命令和子命令

     比如`python main.py image -c`这里`python main.py`就是根命令（根命令只有一个），`image`是一个子命令，表示后面的参数是用来管理这个项目中的图片相关的，`-c`就是一个标记，表示check检测图床  
     + 子命令可以嵌套，比如`python main.py image check --top=XXX`，这里到`image`表示是图床相关，`check`表示是检测相关，最后一个参数指出去哪个目录下检测（当然这样的设计在目前的这个项目中是没必要的）
     + 区分参数和标记。

     + 这样的设计还有一个好处，可以让`--help`更方便的展现
          ```bash
          python main.py --help      # 展示这个命令都有哪些子命令
          python main.py image --help  # 展示这个子命令都有哪些参数和标记
          ```

项目目录如下：
```
> tree          
.
├── main.py
└── src
    ├── cli
    │   ├── cli.py
    │   ├── command
    │   │   ├── image.py
    │   │   ├── __init__.py
    │   │   └── stats.py
    │   └── __init__.py
    └── command
        ├── image
        │   ├── check.py
        │   ├── clean.py
        │   ├── __init__.py
        │   └── transfer.py
        ├── __init__.py
        └── stats
            └── __init__.py
```


+ `main.py`即为项目入口, 在这里有两个任务
     + 检查配置文件
     + 进入命令代码`cli`

+ 在`src/cli/cli.py`中检查参数并“分发子命令权限”
     ```python
     import argparse

     from .command import stats, image
     
     parser = argparse.ArgumentParser()
     subparsers = parser.add_subparsers()

     stats.init(subparsers.add_parser("stats", help="项目信息统计"))
     image.init(subparsers.add_parser("image", help="维护项目图床"))

     def exec():
          args = parser.parse_args()
          if not vars(args):
               parser.print_help()
          else:
               args.func(args)
     ```

+ 在目录`src/cli/command`下即为这个子命令下参数或标记的配置
     >这里体现这样设计的好处之一就是根命令不用在乎子命令是如何实现的

     + 不需要标记或参数的，比如这里的`stats`，统计作用
          ```python
          import src.command.stats as stats

          subparsers = None

          def init(subparsers_):
               global subparsers
               subparsers = subparsers_

               subparsers.set_defaults(func=exec)

          def exec(args):
               stats.cnt()    
          ```

     + 需要标记且标记互斥的，比如这里的`image`，要么转移图床、要么检查图床、要么从图床中去掉不使用的图片
          ```python
          import src.command.image as image

          subparsers = None

          def init(subparsers_):
               global subparsers
               subparsers = subparsers_

               subparsers.set_defaults(func=exec)

               mutually_exclusive_group = subparsers.add_mutually_exclusive_group()
               mutually_exclusive_group.add_argument("-t", "--transfer", action="store_true", help="使用图床前缀按照模式替换图床链接")
               mutually_exclusive_group.add_argument("--check", action="store_true", help="检测项目中的失效图床链接")
               mutually_exclusive_group.add_argument("--clean", action="store_true", help="检测图传中的图床链接, 删除未链接图片，要求图片在本地")

          def exec(args):
               if args.transfer is True:
                    image.transfer()
               elif args.check is True:
                    image.check()
               elif args.clean is True:
                    image.clean()
               else:
                    subparsers.parse_args(["-h"])
          ```

+ 而在`src/command/`目录下则是对应功能的实现，这里有个小trick：说到底，每个命令的实现都是一个脚本，一般都是以函数的形式组织的，在这个目录下，每个命令功能的实现是一个文件，那么用户难道要一个一个把每个文件都导入嘛？导入后怎么管理呢？可以在每个命令下的`__init__.py`文件中import一下，比如image这个命令`src/command/image/__init__.py`
     ```python
     from .transfer import transfer
     from .check import check 
     from .clean import clean

     __all__ = [transfer, check, clean]
     ```
     这样依赖，外界只需要import这个目录`image`，就可以通过`image.xxx`的方式使用各个函数了，这里image不是类对象，而是一个module，也算是python万物皆对象的trick吧。
