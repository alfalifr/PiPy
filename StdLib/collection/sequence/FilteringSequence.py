from abc import abstractmethod
from typing import Iterable

from collection.iterator.SkippingIterator import SkippingIterator, skippingIteratorOf
from collection.sequence.Sequence import Sequence, SequenceImpl
from val.generic import T_out

"""
class FilteringSequence(Sequence[T_out]):
    "" "
    Kelas sequence yg dapat mem-filter iterator-nya.
    "" "

    @abstractmethod
    def __iter__(this) -> SkippingIterator[T_out]:
        pass


class FilteringSequenceImpl(FilteringSequence[T_out], SequenceImpl[T_out]):

    def __new__(cls, content: Iterable[T_out], skipFun: (lambda next_: bool)):
        return super().__new__(cls, content)

    def __init__(this, content: Iterable[T_out], filteringFun: (lambda next_: bool)) -> None:
        super().__init__()
        this._filteringFun = filteringFun

    def __iter__(this) -> SkippingIterator[T_out]:
        return skippingIteratorOf(*this.content, skipFun = this._filteringFun, reverseFunResult = True)


def filterSequenceOf(*varargs, filteringFun: (lambda next_: bool) = lambda it: True) -> FilteringSequence[T_out]:
    return FilteringSequenceImpl(varargs, filteringFun)
"""