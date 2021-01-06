from abc import abstractmethod
from typing import Generic, Callable

from collection.iterator.Iterator import Iterator, IteratorImpl
from reflex.Reflex import isGenerator, isIterator
from val.generic import T_out, In


class MappingIterator(Generic[In, T_out], Iterator[T_out]):
    """
    Kelas abstrak semua iterator pada library ini.
    """

    @abstractmethod
    def map(this, next: In) -> T_out: pass

    @abstractmethod
    def nextInput(this) -> In: pass

    def next(this) -> T_out: return this.map(this.nextInput())

    @abstractmethod
    def hasNext(this) -> bool: pass

    def __next__(this) -> T_out:
        return this.next()

    def __iter__(this) -> "MappingIterator[T_out]":
        return this


class MappingIteratorImpl(IteratorImpl[T_out], MappingIterator[In, T_out]):
    _prevNextInput: In = None  # Item yg diambil dari fungsi [next] pada iterasi sblumya.

    def __init__(
        this,
        nextInputFun: Callable[[int], In],
        mappingFun: Callable[[In], T_out],
        hasNextFun: Callable[[T_out, int], bool]
    ) -> None:
        super().__init__(
            lambda i: mappingFun(nextInputFun(i)),
            hasNextFun
        )
        this.nextInputFun = nextInputFun
        this.mappingFun = mappingFun

    @property
    def prevNextInput(this) -> In: return this._prevNextInput

    def map(this, next: In) -> T_out: return this.mappingFun(next)

    def nextInput(this) -> In:
        if not this.hasNext():
            raise StopIteration()
        this._prevNextInput = this.mappingFun(this.nextInputFun(this.prevIndex))
        this._prevIndex += 1
        # print(f"Iterator next() this.nextFun= {this.nextFun} this._prevNext = {this._prevNext}")
        return this.prevNextInput

    def next(this) -> T_out: return this.map(this.nextInput())


def mappingIteratorOf(*args: In, mappingFun: Callable[[In], T_out]) -> MappingIterator[In, T_out]:
    range_ = range(0, len(args))
    nextInputFun = lambda index: args[index]
    hasNextFun = lambda prevNext, index: index in range_

    if isGenerator(args) or isIterator(args):
        nextInput = {"n": None}

        def hasNextFun_():
            try:
                nextInput["n"] = args.__next__()
                return True
            except StopIteration: return False

        nextInputFun = lambda index: nextInput["n"]
        hasNextFun = hasNextFun_

    return MappingIteratorImpl(
        nextInputFun,
        mappingFun,
        hasNextFun,
    )
