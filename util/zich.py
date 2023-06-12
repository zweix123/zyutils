import builtins
from typing import Any, Set, List, Optional
from inspect import ismethod, isfunction


class Stainer:
    def __init__(self) -> None:
        pass

    def __call__(self, s: str) -> str:
        return s


class Entry:
    def __init__(self, k: Any, v: Any, sep: str) -> None:
        # if dict: k is dict key, v is dict value, sep is ' : '
        # if custom: k is attr name, v is attr value, sep is " = "
        # if ...: k is None, v is None, sep is not key
        self.k = k
        self.v = v
        self.sep = sep


class Zish:
    _print = print

    LIMIT = 4  # 对于非字符串可序列化的元素的个数限制
    MAXN = 80  # 对于可str化的单行长度限制
    TAB = "  "
    BANS: Set[Any] = set()  # 特判不会处理的custom class

    def __init__(self) -> None:
        self.stainer = Stainer()

        self.cur_dep = 0
        self.config = [Zish.gen_config()]

    @staticmethod
    def gen_config(indent: bool = True, comma: bool = True, end="\n") -> dict:
        return {"indent": indent, "comma": comma, "end": end}

    def print(
        self,
        s: str,
        indent: Optional[bool] = None,  # 是否缩进, None则遵循当前层次全局配置
        comma: Optional[bool] = None,  # 是否输出逗号, None则遵循当前层次全局配置
        end: Optional[str] = None,  # print函数的end参数, None则遵循当前层次全局配置
    ) -> None:
        if indent is None:
            indent = self.config[-1]["indent"]
        if comma is None:
            comma = self.config[-1]["comma"]
        if end is None:
            end = self.config[-1]["end"]

        lines = s.splitlines()
        if len(lines) > 0:
            if indent:
                lines[0] = self.cur_dep * Zish.TAB + lines[0]
            for i in range(1, len(lines)):
                lines[i] = (self.cur_dep + 1) * Zish.TAB + lines[i]
        s = "\n".join(lines)

        Zish._print(
            "{}{}{}".format(
                "",  # self.cur_dep * Zish.TAB if indent is True else "",
                self.stainer(s),
                "," if comma is True and self.cur_dep != 0 else "",
            ),
            end=end,
        )

    @staticmethod
    def check_builtin(inst: Any) -> bool:  # check if inst is built-in thing
        return (
            inst is None  # 特判None
            or isinstance(inst, type(...))  # 特判...
            # Warning, Exception, Error, built-in type
            or type(inst).__name__ in dir(builtins)
            # built-in function
            or hasattr(inst, "__name__") and hasattr(builtins, inst.__name__)  # fmt: skip
        )

    def __call__(self, *insts: Any, depth: int = 0) -> Any:
        # 转递归为迭代
        if len(insts) == 1:
            inst = insts[0]
        else:  # 0 or > 1
            for inst in insts:
                self(inst, depth=depth)
            return

        last_dep = self.cur_dep
        self.cur_dep = depth

        if Zish.check_builtin(inst):
            self.handle_builtin(inst)
        else:
            self.handle_custom(inst)

        self.cur_dep = last_dep

    @staticmethod
    def check_single(inst: Any) -> bool:
        # need check_builtin(inst) -> True
        return type(inst) not in (list, tuple, set, dict)

    def handle_builtin(self, inst: Any) -> None:
        if Zish.check_single(inst):
            self.handle_single(inst)
        else:
            self.handle_multi(inst)

    def handle_single(self, inst: Any) -> None:
        self.print(self.gen_single(inst))

    def gen_single(self, inst: Any) -> str:
        if isinstance(inst, type(...)):
            return "..."
        elif isinstance(inst, str):
            if len(inst) <= Zish.MAXN:
                return f"'{inst}'"
            if len(inst) > Zish.MAXN:
                return f"str('{inst[:Zish.MAXN]}...' len={len(inst)})"
        elif isinstance(inst, (bytes, bytearray)):
            if len(str(inst)) <= Zish.MAXN:
                return str(inst)
            else:
                handle = hex  # int 10; bin 2; oct 8, hex 16
                res = f"{type(inst).__name__}(["
                for byte in inst[: int(Zish.MAXN // 4 - 2)]:
                    res += handle(byte) + " "
                res += f"... {handle(inst[-1])}] len={len(inst)})"
                return res
        return str(inst)

    def handle_custom(self, inst: Any) -> None:
        assert type(inst) not in Zish.BANS, f"{type(inst)} not yet developed."
        if False:  # 占位
            pass
        elif hasattr(type(inst), "__str__") and type(inst).__str__ is not object.__str__:  # fmt: skip

            self.print(f"{type(inst).__name__}(\n{inst.__str__()}", end="\n")
            self.print(")")
        elif hasattr(type(inst), "__repr__") and type(inst).__repr__ is not object.__repr__:  # fmt: skip
            self.print(f"{type(inst).__name__}(\n{inst.__repr__()}", end="\n")
            self.print(")")
        else:
            self.handle_multi(inst)

    def handle_multi(self, inst: Any) -> None:
        if isinstance(inst, Entry):
            self.handle_entry(inst)
        elif isinstance(inst, (list, set, tuple)):
            self.handle_seq(inst)
        else:
            self.handle_com(inst)

    def handle_entry(self, inst: Entry) -> None:
        if inst.k is None and inst.v is None:
            self.print(self.gen_single(...))
            return

        if Zish.check_builtin(inst.k) and Zish.check_single(inst.k):
            self.print(self.gen_single(inst.k), comma=False, end="")
            self.print(inst.sep, indent=False, comma=False, end="")
        else:
            self.config.append(Zish.gen_config(True, False, ""))
            self(inst.k, depth=self.cur_dep)
            self.config.pop()
            self.print(inst.sep, indent=False, comma=False, end="")

        self.config.append(Zish.gen_config(False, True, end="\n"))
        self(inst.v, depth=self.cur_dep)
        self.config.pop()

    def handle_seq(self, inst: Any) -> None:
        symbol = {"list": ["[", "]"], "tuple": ["(", ")"], "set": ["{", "}"]}[type(inst).__name__]  # fmt: skip
        if all(Zish.check_builtin(ele) and Zish.check_single(ele) for ele in inst):
            if len(str(inst)) <= Zish.MAXN:
                self.print(str(inst))
            else:
                ele_str_list: List[str] = list()
                for ele in inst:
                    ele_str = self.gen_single(ele)
                    if len(", ".join([ele_str for ele_str in ele_str_list])) > Zish.MAXN:  # fmt: skip
                        break
                    ele_str_list.append(ele_str)
                if len(ele_str_list) > Zish.LIMIT:
                    ele_str_list.append(self.gen_single(...))
                    self.print(symbol[0]+ ", ".join([ele_str for ele_str in ele_str_list])+ symbol[1])  # fmt: skip
                else:
                    self.print(symbol[0], comma=False, end="\n")
                    self.config.append(Zish.gen_config(True, True))
                    zp(*list(inst)[:3], depth=self.cur_dep + 1)  # 这里转换成list是因为set不能索引访问
                    self.config.pop()
                    self.print(symbol[1], indent=True, comma=True)
        else:
            content = list(inst)
            if len(content) > Zish.LIMIT:
                content[Zish.LIMIT :] = [...]
            self.print(symbol[0], comma=False, end="\n")
            self.config.append(Zish.gen_config(True, True))
            zp(*content, depth=self.cur_dep + 1)  # 这里转换成list是因为set不能索引访问
            self.config.pop()
            self.print(symbol[1], indent=True, comma=True)

    def handle_com(self, inst: Any) -> None:
        entries: List[Entry] = list()
        if isinstance(inst, dict):
            for k, v in inst.items():
                entries.append(Entry(k, v, " : "))
                if len(entries) >= Zish.LIMIT:
                    break
            if len(inst.items()) > Zish.LIMIT:
                entries.append(Entry(None, None, "..."))
            self.print("{", comma=False, end="\n")
            self.config.append(Zish.gen_config(True, True))
            self(*entries, depth=self.cur_dep + 1)
            self.config.pop()
            self.print("}", indent=True)
        else:  # real custom
            for attr in dir(inst):
                value = getattr(inst, attr)
                if attr.startswith("__") or ismethod(value) or isfunction(value):
                    continue
                entries.append(Entry(attr, value, " = "))

            self.print(f"<{type(inst).__name__}")
            self.config.append(Zish.gen_config(True, True))
            self(*entries, depth=self.cur_dep + 1)
            self.config.pop()
            self.print(">")


zp = Zish()

if __name__ == "__main__":
    from enum import Enum, auto
    from decimal import Decimal

    zp()
    zp(None)
    zp(...)
    zp(True)
    zp(False)
    zp(42)
    zp(3.1415)
    zp(Decimal("3.1415"))
    zp(Decimal(3.1415))
    zp("hello world")
    zp(
        "hello Alice, Bob, Charlie, Dave, Eve, Frank, Grace, Heidi, Ivan, John, Karen, Lily, Mike, Nancy, Oscar, Peter, Quentin, Rachel, Sarah, Tom, Uma, Veronica, Wendy, Xander, Yolanda, Zachary"
    )
    zp(b"hello world")
    zp(
        b"hello Alice, Bob, Charlie, Dave, Eve, Frank, Grace, Heidi, Ivan, John, Karen, Lily, Mike, Nancy, Oscar, Peter, Quentin, Rachel, Sarah, Tom, Uma, Veronica, Wendy, Xander, Yolanda, Zachary"
    )
    zp(bytearray(b"hello world"))
    zp(
        bytearray(
            b"hello Alice, Bob, Charlie, Dave, Eve, Frank, Grace, Heidi, Ivan, John, Karen, Lily, Mike, Nancy, Oscar, Peter, Quentin, Rachel, Sarah, Tom, Uma, Veronica, Wendy, Xander, Yolanda, Zachary"
        )
    )
    zp([1, 2, 3])
    zp((1, 2, 3))
    zp({1, 2, 3})
    zp(list(range(100)))
    zp(list([str(i) * i for i in range(1, 100)]))
    zp(list([str(i) * i for i in range(100, 0, -1)]))
    zp(
        [
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6],
        ]
    )
    zp({1: "1", 2: "2", 3: "3"})
    zp({"1": 1, "2": 2, "3": 3})

    class Time(Enum):
        SECOND = 1
        MINUTE = 60 * SECOND
        HOUR = 60 * MINUTE

    zp(Time.HOUR)

    class DogType(Enum):
        A = auto()
        B = auto()
        C = auto()

    zp(
        {
            DogType.A: [1, "2", 3],
            DogType.B: ["1", 2, "3"],
            DogType.C: {DogType.A: [1, "2", 3], DogType.B: ["1", 2, "3"]},
            "hello world": {
                DogType.A: [1, "2", 3],
                DogType.B: ["1", 2, "3"],
            },
        }
    )

    class T:
        a = None
        b = ...
        c = True
        d = False
        e = 42
        f = 3.1415
        g = Decimal("3.1415")
        h = Decimal(3.1415)
        i = "hello world"
        j = "hello Alice, Bob, Charlie, Dave, Eve, Frank, Grace, Heidi, Ivan, John, Karen, Lily, Mike, Nancy, Oscar, Peter, Quentin, Rachel, Sarah, Tom, Uma, Veronica, Wendy, Xander, Yolanda, Zachary"
        k = b"hello world"
        l = b"hello Alice, Bob, Charlie, Dave, Eve, Frank, Grace, Heidi, Ivan, John, Karen, Lily, Mike, Nancy, Oscar, Peter, Quentin, Rachel, Sarah, Tom, Uma, Veronica, Wendy, Xander, Yolanda, Zachary"
        m = bytearray(b"hello world")
        n = bytearray(
            b"hello Alice, Bob, Charlie, Dave, Eve, Frank, Grace, Heidi, Ivan, John, Karen, Lily, Mike, Nancy, Oscar, Peter, Quentin, Rachel, Sarah, Tom, Uma, Veronica, Wendy, Xander, Yolanda, Zachary"
        )
        o = [1, 2, 3]
        p = (1, 2, 3)
        q = {1, 2, 3}
        r = list(range(100))
        s = list([str(i) * i for i in range(1, 100)])
        t = list([str(i) * i for i in range(100, 0, -1)])
        u = [
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6],
        ]

        v = {1: "1", 2: "2", 3: "3"}
        w = {"1": 1, "2": 2, "3": 3}
        x = Time.HOUR
        y = {
            DogType.A: [1, "2", 3],
            DogType.B: ["1", 2, "3"],
            DogType.C: {DogType.A: [1, "2", 3], DogType.B: ["1", 2, "3"]},
            "hello world": {
                DogType.A: [1, "2", 3],
                DogType.B: ["1", 2, "3"],
            },
        }

    zp(T())

    class Join:
        def __init__(self, a, b, c) -> None:
            self.a = a
            self.b = b
            self.c = c

        def __repr__(self) -> str:
            return f"""{self.a}
{self.b}
{self.c}"""

    j = Join(1, 2, 3)

    zp(j)
    zp([j, j, j])
