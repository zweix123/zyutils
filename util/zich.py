import builtins
from enum import Enum
from decimal import Decimal
from inspect import ismethod, isfunction
from typing import Any, Set
from rich import print


MAX_LEN: int = 50
# a number from ancient, the len of screen
# the var is limit symbol itself,
# not include the len of pre and suf
BAN_TYPE: Set = set()


def zp(*insts: Any, prefix: str = "", suffix: list = [""]) -> None:
    """zweix object print
    以最利于人读的方式输出Python类对象的数据

    对于自定义类对象, 全面展示
        对于实现了__str__或者__repr__魔术方法的自定义类型, 优先展示用户定义
    对于内置类型, 识别大小, 适当展示
    > 对于内置类型中的自定义类型, 当前版本选择不展示

    对于部分非内置类型(库内类型), 部分特判
    特判名单: decimal.Decimal, enum.Enum

    Args:
        *insts (Any, optional): 可变参数, 用户放入任意类型任意数量的变量, 打印
        prefix (str, optional): 内部使用, 用户不必关心. Defaults to "".
        suffix (list, optional): 内部使用, 用户不必关心. Defaults to [""].

        suffix: 为实现诸如序列元素、字典元素和类成员值的输出末尾符号,
                当前的输出末尾是由上一个调用确定的, 而每个调用不知道后面还会有什么,
                所有采用list(语义上其实是链表), 每个递归节点只使用列表末尾,
                不用添加\\n, 默认
                已经其他亿点细节
    """

    if True:  # handle parameters, current level handle var `inst`
        # 这里的if不是为了语义, 而是为了划分代码块
        if len(insts) > 1:
            for inst in insts:
                zp(inst, prefix=prefix, suffix=suffix)
            return
        elif len(insts) == 1:
            inst = insts[0]
        else:
            return

    # handle printer
    def get_printer():
        def printer(*arg, **kwargs):
            # if len(prefix) > 0 and prefix[-1] not in set("([{:"):
            #     print(prefix, end="")
            # # for '('、'[' and '{', current node is container first element
            # # for ':', current node is dict value or class member value
            # # both of the above don't print prefix
            # 不用整这个花活了, 只有全是space的prefix才输出
            if all(c.isspace() for c in prefix):
                print(prefix, end="")

            wait_suffix = suffix[-1]
            # set `end` defualt parameter
            if "end" not in kwargs:
                kwargs["end"] = "\n"
            elif "\n" not in kwargs["end"]:
                wait_suffix = ""
            else:
                assert False, "未决"
            kwargs["end"] = wait_suffix + kwargs["end"]
            # 这里有精妙的设计, 想一下,
            # 如果用户没有设置end, 说明就像使用默认的换行, 要开新的一行了, 肯定要添加后缀, 同时我们这里也设置的换行,
            # 如果用户添加了end, 还有两个情况,
            # 那就是用户添加了回车, 就是想修饰下, 说明要换行了, 也应该添加后缀,
            # 但是用户的修饰和当前节点的后缀的优先级是什么?还没有决定,
            # 最后的情况, 就是用户使用end参数是为了避免回车, 说明当前行后面还会有东西, 就不添加后缀
            # 这也意味着, 如果当前调用在递归时要注意当前的prefix是否是全空白的
            print(*arg, **kwargs)

        return printer

    _print = get_printer()
    name = type(inst).__name__  # 常用量

    # special judge None
    if inst is None:
        _print("None")
    # special judge ...
    # elif type(inst) is Ellipsis:
    elif type(inst) == type(...):
        _print("...")
    elif name in dir(builtins):  # handle buildin type
        if inst is True or inst is False:  # True and False
            _print(inst)  # 直接输出
        elif isinstance(inst, (int, float)):  # int and float
            _print(f"{name}({inst})")  # direct print
        elif isinstance(inst, (str)):  # str len, check len
            inst_str = inst
            if len(inst) > MAX_LEN:
                inst_str = inst[: MAX_LEN - 3] + "..."
            _print(f"{name}('{inst_str}' len={len(inst)})")  # print content and len
        elif isinstance(inst, (bytes, bytearray)):  # bytes and bytearray
            zp_inst = inst
            if len(inst) * 4 > MAX_LEN:  # 一个字节和一个空格打印占四位
                zp_inst = inst[: int(MAX_LEN // 4)]
            _print("{}[{}]".format(name, " ".join("{:03d}".format(b) for b in zp_inst)))
        elif isinstance(inst, (list, tuple, set)):  # sequence: list, tuple, set
            # handle long
            if len(str(inst)) < MAX_LEN:
                _print(f"{name}{inst}")
                return
            # type name and bracket
            SYMBOL = {
                "list": ["[", "]"],
                "tuple": ["(", ")"],
                "set": ["{", "}"],
            }
            left, right = SYMBOL[name]

            try:
                head, *body, tail = inst
            except ValueError:
                if isinstance(inst, set):  # set不能通过索引访问, 转换成list
                    assert len(inst) == 1
                    inst = list(inst.pop())
                head, body, tail = inst[0], None, None
            # two situation
            # + head and tail is element and body is sequence, empty or else
            # + head is element and body and tail is None
            _print(name + left, end="")
            if body is None and tail is None:  # situation one
                zp(head, prefix=prefix + name + left, suffix=suffix + [right])
                return
            # situation two
            assert body is not None and tail is not None
            zp(head, prefix=prefix + name + left, suffix=suffix + [","])
            if len(body) > 3:
                body[2:] = [...]
            zp(*body, prefix=len(prefix + name + left) * " ", suffix=suffix + [","])
            zp(tail, prefix=len(prefix + name + left) * " ", suffix=suffix)
            _print(len(prefix + name) * " " + right)
        elif isinstance(inst, dict):
            _print(inst)
        elif isinstance(inst, type):  # include 类名
            _print(inst)
        else:
            assert False, f"该内建类型{type(inst)}未开发"
    else:  # custom type
        if isinstance(inst, Decimal):  # special judge decimal.Decimal
            # maybe have accuracy problem
            _print(f"{name}({inst})")
        elif issubclass(type(inst), Enum):  # special judge enum.Enum
            _print(repr(inst))
        elif isinstance(inst, tuple(BAN_TYPE)):
            assert False, f"该类型{type(inst)}可能来自库自定义类型, 可选择直接输出"
            _print(inst)
        else:  # real custom type
            left, right = tuple("()")
            max_len = max(
                len(attr)
                for attr in dir(inst)
                if not attr.startswith("__") and not ismethod(getattr(inst, attr))
            )
            for attr in dir(inst):
                value = getattr(inst, attr)
                if attr.startswith("__") or ismethod(value) or isfunction(value):
                    # 过滤,       魔术方法,            方法   和            静态方法
                    continue
                # currnt_text = name + left + attr + (max_len - len(attr)) * " " + ":"
                currnt_text = name + left + attr + ":"
                _print(currnt_text, end="")
                zp(value, prefix=prefix + currnt_text, suffix=suffix + [","])
                name = len(name) * " "
                left = len(left) * " "
                prefix = len(prefix) * " "

            _print(right)


zp(True)
zp(False)
zp(None)
zp(...)
zp(1)
zp(1.23)
zp(Decimal(1.23))
zp("str")
zp(
    "strstrstrstrstrstrstrstrstrstr\
strstrstrstrstrstrstrstrstrstr\
strstrstrstrstrstrstrstrstrstr"
)
zp(bytearray([0x23, 0x0, 0x0, 0x0, 0x0]))
zp(bytes(bytearray([0x23, 0x0, 0x0, 0x0, 0x0])))
zp((1, 2, 3))
zp([1, 2, 3])
zp({1, 2, 3})
zp([1])
zp([1, 2])
zp([1, 2, 3])
zp([1, 2, 3, 4])
long_list = [
    "1234567890123456789901234567891",
    "1234567890123456789901234567892",
    "1234567890123456789901234567893",
    "1234567890123456789901234567894",
    "1234567890123456789901234567895",
    "1234567890123456789901234567896",
    "1234567890123456789901234567897",
    "1234567890123456789901234567897",
]
zp(list(long_list))
zp(tuple(long_list))
zp(set(long_list))
zp(["12345678901234567890123456789012345678901234567890123456789012345678901234567890"])

from enum import Enum


class TIME(Enum):
    SECOND = 1
    MINTUE = 60 * SECOND
    HOUR = 60 * MINTUE


zp(TIME.SECOND)


class Market:
    num_ele = 1
    str_ele = "123"
    list_ele = [1, 2, 3, 4, 5]
    enum_ele = TIME.HOUR
    long_list = [
        "1234567890123456789901234567891",
        "1234567890123456789901234567892",
        "1234567890123456789901234567893",
        "1234567890123456789901234567894",
        "1234567890123456789901234567895",
        "1234567890123456789901234567896",
        "1234567890123456789901234567897",
        "1234567890123456789901234567897",
    ]


zp(Market)
zp(Market())
