from abc import abstractmethod
from typing import Callable

from collection.iterator.Iterator import Iterator, IteratorImpl
from val.generic import T_out


class SkippingIterator(Iterator[T_out]):
    """
    Kelas Iterator yg dapat di-skip.
    """

    @abstractmethod
    def skip(this, next: T_out) -> bool:
        """
        Fungsi yg melewatkan (skip) `next` jika return `true`
        :param next: next dari fungsi `next` yg akan di-emit.
        :return: `true` maka `next` di-skip.
        """
        pass


class SkippingIteratorImpl(SkippingIterator[T_out], IteratorImpl[T_out]):
    skipFun: Callable[[T_out], bool] = None  # Diganti nilainya dg fungsi.
    reverseSkipFunResult: bool = False
    _status = -1  # -1 untuk belum diketahui, -2 sedang berjalan, 0 selesai, 1 emit next.

    def __init__(
        this,
        nextFun: (lambda index: T_out),
        hasNextFun: (lambda prevNext, index: bool),
        skipFun: (lambda next_: bool)
    ) -> None:
        super().__init__(nextFun, hasNextFun)
        this.skiptFun = skipFun

    def _calculateStatus(this):
        if this._status != -1 or not this.hasNext():
            this._status = 0
            return
        this._status = 1
        while this.hasNext():
            super().next()
            # print(f"SkipItr calculate() next= {this.prevNext} src= ${this.prevNext} skip = {this.skip(this.prevNext)}")
            if not this.skip(this.prevNext):
                this._status = 1
                return
        this._status = 0

    def next(this) -> T_out:
        if this._status == -1:
            this._calculateStatus()
        if this._status == 1:
            # super().next()
            # print(f"SkipItr next() status == 1 this.prevNext= {this.prevNext}")
            this._status = -1
            return this.prevNext
        else: raise StopIteration()

    def skip(this, next: T_out) -> bool:
        if not this.reverseSkipFunResult:
            return this.skiptFun(next)
        else:
            return not this.skiptFun(next)


def skippingIteratorOf(
        *varargs,
        skipFun: Callable[[T_out], bool] = lambda it: True,
        reverseFunResult: bool = False
) -> SkippingIterator[T_out]:
    # print(f"skippingIteratorOf() skipFun= ${inspect.getsource(skipFun)}")
    itr = SkippingIteratorImpl(
        lambda index: varargs[index],
        lambda prevNext, index: index in range(0, len(varargs)),
        skipFun,
    )
    itr.reverseSkipFunResult = reverseFunResult
    return itr
