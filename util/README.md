自用封装库

```
.
├── __init__.py
├── file_util.py  # 文件处理和IO相关
├── md_util.py    # markdown文件处理相关
├── misc_util.py  # 杂项(目前只有一个从枚举名字符串到枚举类型的反射函数)
├── net_util.py   # 网络相关
├── rich_util.py  # 对rich封装的关于输出相关的函数
├── str_util.py   # 字符串处理相关
├── time_util.py  # 时间相关
└── zich.py       # 这里借用高天的对objprint的Description
                  # A library that can print Python objects in human readable format
```

## RailGun

并发超高且接口简单的Restful客户端, 具体文档有时间再写

## zich

一般不轻易造轮子, 目前我知道的可以实现object print有rich和objprint, 既然我选择造轮子说明前两者有不能满足要求的地方.

rich很美观, 但是不能"轻松"的递归打印  
objprint, 可以递归打印, 但是对于很大的列表也是全盘打印, 可以指定"每层"打印个数, 但是这个限制是全局的, 即比如限制三个, 列表是打印只三个元素, 但是类属性也只打印三个

所以我也自己写了一个, 主体仍然是模仿objprint的行为