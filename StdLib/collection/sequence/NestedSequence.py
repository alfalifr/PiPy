from abc import ABC, abstractmethod
from typing import Generic, Iterable

from collection.iterator.NestedIterator import NestedIterator
from val.generic import In, Out


class NestedSequence(Generic[In, Out], ABC, Iterable[Out]):
    """
    Kelas dasar untuk semua sequence pada library ini.
    """

    @abstractmethod
    def __iter__(this) -> NestedIterator[In, Out]: pass