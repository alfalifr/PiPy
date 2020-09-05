from abc import ABC, abstractmethod
from typing import Generic, Iterable

from generic.Generics_ import T_out


class NestedSequence(Generic[T_out], ABC, Iterable[T_out]):
    """
    Kelas dasar untuk semua sequence pada library ini.
    """

    @abstractmethod
    def __iter__(this) -> Iterator[T_out]: pass