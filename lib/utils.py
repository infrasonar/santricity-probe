from typing import Optional


def to_int(val: Optional[str]) -> Optional[int]:
    try:
        assert val is not None
        return int(val)
    except TypeError:
        return


def to_float(val: Optional[str]) -> Optional[float]:
    try:
        assert val is not None
        return float(val)
    except TypeError:
        return
