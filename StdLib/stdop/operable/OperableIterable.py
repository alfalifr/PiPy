import sys
from typing import Iterable, Any, Callable, Optional

from collection.iterator.Iterator import Iterator
from exception.NoSuchElementExc import NoSuchElementExc
from foundation.wrapper.FlatWrapper import FlatWrapper
from val.generic import T_out


class OperableIterable(FlatWrapper[T_out], Iterable[T_out]):
    """
    Kelas yg berisi sekumpulan data yg mirip dg Iterable dg fungsi tambahan.
    """

    breakItr = False

    def __new__(cls, content: T_out) -> Any:
        if not isinstance(content, Iterable):
            raise TypeError(f"""content: {content} harus Iterable.""")
        inst = super().__new__(cls, content)
        return inst

    def filter(this, op: Callable[[T_out], bool]) -> "OperableIterable[T_out]":
        return OperableIterable([e for e in this.content if op(e)])

    def forEach(this, op: Callable[[T_out], object], start: int = 0, end: int = None):
        this.breakItr = False
        i = 0
        range_ = range(start, end or sys.maxsize)
        for e in this.itr:
            if i in range_:
                op(e)

    @property
    def first(this) -> T_out:
        for e in this:
            return e  # Hanya mengembalikan 1 member
        raise NoSuchElementExc("Element kosong.")

    @property
    def firstOrNull(this) -> Optional[T_out]:
        try: return this.first
        except NoSuchElementExc: return None

    @property
    def last(this) -> T_out:
        if this.isEmpty:
            raise NoSuchElementExc("Elemen kosong.")
        outerE = None
        for e in this:
            outerE = e
        return outerE

    @property
    def lastOrNull(this) -> Optional[T_out]:
        try: return this.last
        except NoSuchElementExc: return None

    """
    @property
    def firstOrNull(this):
        try: return this.last
        except NoSuchElementExc: return None
    """
    @property
    def isEmpty(this) -> bool:
        try:
            this.first
            return False
        except NoSuchElementExc: return True

    @property
    def itr(this) -> Iterator[T_out]:
        # print(f"itr itr() cls= {type(this)} this.content= {this.content}")
        list = []
        this.breakItr = False
        for e in this.content:
            if this.breakItr: break
            list.append(e)
        return list.__iter__()

    def __iter__(this) -> Iterator[T_out]:
        return this.itr
