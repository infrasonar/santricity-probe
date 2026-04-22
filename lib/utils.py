def to_int(val: str | None) -> int | None:
    try:
        assert val is not None
        return int(val)
    except TypeError:
        return


def to_float(val: str | None) -> float | None:
    try:
        assert val is not None
        return float(val)
    except TypeError:
        return
