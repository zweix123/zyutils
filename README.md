以个人需求优先的场景下, Python很方便, 但国内目前对Python的岗位需求不大, 只能图一乐.

我个人使用Python主要在以下几个方面

+ 自动化脚本：[jyyslide-md](https://github.com/zweix123/jyyslide-md)、博客管理工具、爬虫
+ 量化交易系统：中低频交易，摸索中
+ Web应用：

其中

+ 对于爬虫我严格遵循《中华人民共和国网络安全法》、《互联网信息服务管理办法》以及Robots协议
+ 关于Web应用我用Django框架写了一个Web游戏的Demo，但是后续没有计划继续开发，估计永远Private了
+ 关于博客管理工具，我借鉴了实习中一个由Go开发的命令行工具的架构，确实开发成了一个命令行项目，但是后续发现项目太小了没有必要，但架构本身挺有意思的，所以我将功能拆分成了一个个小脚本，把框架设计写成文档

除此之外

在开发项目的过程中总结了些封装库, 目前比较得意的有
+ 并发超高且接口简单的Restful客户端：[代码](./util/net_util.py#L168) | [文档](./util/README.md#railgun)
+ 借鉴[`rich`](https://github.com/Textualize/rich/tree/master)和[`objprint`](https://github.com/gaogaotiantian/objprint)用来以human readable format打印实例属性的库：[代码](./util/zich.py) | [文档](./util/README.md#zich)

### 项目结构

下面各个子目录下有README对应其下目录结构
```
.
├── cli      # 上面提到的命令行项目的框架设计
├── crawler  # 爬虫
├── md       # 博客管理相关脚本
├── misc     # 杂项, 一些计算相关代码和一个pdf转图片的脚本
└── util     # 自用封装库
```

代码分布在我的各个阶段, 所以代码风格各异, 也未必是成熟的实现.