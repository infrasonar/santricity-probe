from typing import Optional


def to_int(val: Optional[str]) -> int:
    try:
        return int(val)
    except TypeError:
        return


def to_float(val: Optional[str]) -> float:
    try:
        return float(val)
    except TypeError:
        return
