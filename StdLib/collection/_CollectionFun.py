from collections import Sized
from typing import Optional, Iterable, Callable

from val.generic import T


def size(obj: Iterable) -> int:
    if isinstance(obj, Sized):
        return len(obj)
    i = 0
    for e in obj:
        i += 1
    return i


def isEmpty(obj: Iterable) -> bool:
    return size(obj) == 0


def find(itr: Iterable[T], predicate: Callable[[T], bool]) -> Optional[T]:
    for e in itr:
        if predicate(e):
            return e
    return None