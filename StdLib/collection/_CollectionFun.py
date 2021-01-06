from collections import Iterable, Sized


def size(obj: Iterable) -> int:
    if isinstance(obj, Sized):
        return len(obj)
    i = 0
    for e in obj:
        i += 1
    return i


def isEmpty(obj: Iterable) -> bool:
    return size(obj) == 0
