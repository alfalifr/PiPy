from typing import Generic, Callable

from foundation.wrapper.FlatWrapper import FlatWrapper
from val.generic import T, R


class Operable(Generic[T], FlatWrapper[T]):
    """
    Kelas dasar pada library yg dapat melakukan operasi scope standar.
    """

    def also(this, op: Callable[[T], T]) -> T:
        """
        Fungsi untuk melakukan operasi chaining sebelum mengembalikan referensi object `this`.
        :param op: lambda untuk operasi `also`
        :return: object `this`.
        """
        op(this)
        return this

    def let(this, op: Callable[[T], R]) -> R:  #Generic[R]
        """
        Fungsi untuk melakukan operasi chaining yg mengubah object `this` menjadi apapun itu pada :param op.
        :param op: lambda untuk operasi `let`
        :return: object apapun itu yg di-return :param op.
        """
        return op(this)


def toOperable(any) -> Operable[T]:
    return Operable(any)
