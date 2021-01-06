from abc import ABC, abstractmethod
from typing import Generic, Iterator as Itr, Iterable, Callable

from reflex.Reflex import isGenerator, isIterator
from val.generic import T_out


class Iterator(Generic[T_out], ABC, Itr[T_out], Iterable[T_out]):
    """
    Kelas abstrak semua iterator pada library ini.
    """

    @abstractmethod
    def next(this) -> T_out: pass

    @abstractmethod
    def hasNext(this) -> bool: pass

    def __next__(this) -> T_out:
        return this.next()

    def __iter__(this) -> "Iterator[T_out]":
        return this


class IteratorImpl(Iterator[T_out]):
    nextFun: Callable[[int], T_out] = None  # Diganti nilainya dg fungsi.
    hasNextFun: Callable[[T_out, int], bool] = None  # Diganti nilainya dg fungsi.
    _prevNext: T_out = None  # Item yg diambil dari fungsi [next] pada iterasi sblumya.
    _prevIndex: int = 0  # Indeks pada iterasi sblumnya.

    def __init__(this, nextFun: Callable[[int], T_out], hasNextFun: Callable[[T_out, int], bool]) -> None:
        super().__init__()
        this.nextFun = nextFun
        this.hasNextFun = hasNextFun

    @property
    def prevNext(this) -> T_out: return this._prevNext
    @property
    def prevIndex(this) -> T_out: return this._prevIndex

    def next(this) -> T_out:
        if not this.hasNext():
            raise StopIteration()
        this._prevNext = this.nextFun(this.prevIndex)
        this._prevIndex += 1
        # print(f"Iterator next() this.nextFun= {this.nextFun} this._prevNext = {this._prevNext}")
        return this.prevNext

    def hasNext(this) -> bool:
        return this.hasNextFun(this.prevNext, this.prevIndex)


def iteratorOf(*args: T_out) -> Iterator[T_out]:
    range_ = range(0, len(args))
    nextFun = lambda index: args[index]
    hasNextFun = lambda prevNext, index: index in range_

    if isGenerator(args) or isIterator(args):
        next = {"n": None}

        def hasNextFun_():
            try:
                next["n"] = args.__next__()
                return True
            except StopIteration: return False

        nextFun = lambda index: next["n"]
        hasNextFun = hasNextFun_

    return IteratorImpl(
        nextFun,
        hasNextFun,
    )
