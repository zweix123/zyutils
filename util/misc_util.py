from enum import Enum
from typing import Type, Optional


def find_enum(s: str, enum_class: Type[Enum]) -> Optional[Enum]:
    for enum in enum_class:
        if enum.name == s:
            return enum
    raise Exception("该枚举类没有这样的枚举")
    return None
