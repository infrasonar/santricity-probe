from typing import Optional


def to_int(val: Optional[str]) -> Optional[int]:
    try:
        return int(val)  # type: ignore
    except TypeError:
        return


def to_float(val: Optional[str]) -> Optional[float]:
    try:
        return float(val)  # type: ignore
    except TypeError:
        return
