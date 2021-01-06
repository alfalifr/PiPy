import sys
from typing import Iterable as PyIterable, Any, Callable, Optional, Iterator as PyIterator

from collection.iterator.Iterator import Iterator
from exception.NoSuchElementExc import NoSuchElementExc
from log.logs import prind
from stdop.operable.Operable import Operable
from val.generic import T_out
from val.type import IterableLike


class Iterable(Operable[T_out], PyIterable[T_out]):
    """
    Kelas yg berisi sekumpulan data yg mirip dg Iterable dg fungsi tambahan.
    """

    #breakItr = False

    def __init__(this, origin: IterableLike = [], **kwargs):
        #prind(f"isinstance(content, Iterable)={isinstance(origin, Iterable)} isinstance(content, PyIterator)={isinstance(origin, PyIterator)} **kwargs={kwargs}")
        if not (isinstance(origin, PyIterable) or isinstance(origin, PyIterator)):
            raise TypeError(f"""content: {origin} harus Iterable.""")
        iterable = origin if isinstance(origin, Iterable) else [e for e in origin]

        super().__init__(iterable, **kwargs)

    def filter(this, op: Callable[[T_out], bool]) -> "Iterable[T_out]":
        return Iterable([e for e in this.content if op(e)])

    def forEach(this, op: Callable[[T_out], object], start: int = 0, end: int = None):
        #this.breakItr = False
        i = 0
        range_ = range(start, end or this.size if hasattr(this, 'size') else sys.maxsize)
        #prind(f"range_={range_} end or this.size if hasattr(this, 'size') else sys.maxsize={ end or this.size if hasattr(this, 'size') else sys.maxsize} this.itr={this.itr}")
        for e in this.itr:
            #prind(f"Iterable.forEach() for e={e} i={i} i in range_={i in range_}")
            if i in range_:
                op(e)
            i += 1

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
        """
        list = []
        this.breakItr = False
        for e in this.content:
            if this.breakItr: break
            list.append(e)
        return list.__iter__()
        """
        return this.__iter__()

    """
    def __iter__(this) -> Iterator[T_out]:
        return this.itr
    """


def iterableOf(
    *varargs: T_out,
    src: Iterable[T_out] = None,
    itrBuilder: Callable[[], Iterator[T_out]] = None
) -> Iterable[T_out]:
    itr = itrBuilder() if itrBuilder else src.__iter__()

