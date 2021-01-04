from abc import ABC, abstractmethod
from typing import Generic, Iterable

from collection.iterator.Iterator import iteratorOf, Iterator
from val.generic import T_out


class Sequence(Generic[T_out], ABC, Iterable[T_out]):
    """
    Kelas dasar untuk semua sequence pada library ini.
    """

    @abstractmethod
    def __iter__(this) -> Iterator[T_out]: pass


class SequenceImpl(Sequence[T_out]):
    def __new__(cls, content: Iterable[T_out]):
        if not isinstance(content, Iterable):
            raise TypeError("""content: %s harus Iterable.""" % content)
        inst = super().__new__(cls)
        inst.content = content
        return inst

    def __iter__(this) -> Iterator[T_out]:
        return iteratorOf(*this.content)


def simpleSequenceOf(*vararg) -> Sequence[T_out]:
    return SequenceImpl(vararg)
