from typing import Iterable, Any, Generic, Type
import inspect

from foundation.wrapper.FlatWrapper import FlatWrapper
from generic.Generics_ import T


class Operable(Generic[T], FlatWrapper[T]):
    """
    Kelas dasar pada library yg dapat melakukan operasi scope standar.
    """

    def also(this, op: (lambda it: Operable)):
        """
        Fungsi untuk melakukan operasi chaining sebelum mengembalikan referensi object `this`.
        :param op: lambda untuk operasi `also`
        :return: object `this`.
        """
        op(this)
        return this

    def let(this, op: (lambda it: object)) -> object:
        """
        Fungsi untuk melakukan operasi chaining yg mengubah object `this` menjadi apapun itu pada :param op.
        :param op: lambda untuk operasi `let`
        :return: object apapun itu yg di-return :param op.
        """
        return op(this)


def toOperable(any) -> Operable[T]:
    return Operable(any)
