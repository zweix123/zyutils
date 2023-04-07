from typing import Optional
from rich import print, inspect


def print_table(data: list[list[str]] = list(), title: Optional[str] = None):
    # 以表格的形式打印一个矩形列表, 默认第一行是表头
    from rich.console import Console
    from rich.table import Table

    table = Table(title=title)
    assert len(data) > 0

    for head in data[0]:
        table.add_column(head)
    for row in data[1:]:
        table.add_row(*row)

    console = Console()
    console.print(table)
    print(f"Table has {len(data[1:])} columns.")
