from typing import Any
from prettytable import PrettyTable


def print_table(content: list[list[Any]]):
    table = PrettyTable()
    table.field_names = content[0]
    for row in content[1:]:
        table.add_row(row)
    print(table)
