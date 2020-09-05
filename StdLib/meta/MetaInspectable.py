from abc import ABC, abstractmethod, abstractproperty
from typing import Tuple, Dict, Any

from foundation.wrapper.FlatWrapper import FlatWrapper
from generic.Generics_ import T


class MetaInspectable(ABC, FlatWrapper[T]):
    """
    Kelas dasar yg dapat digunakan sbg unit inspeksi yg dicek oleh semua metaclass yg ada di library ini.
    """

    name: str = None
    """
    Berisi nama attribut yg berisi nilai [bool: boolean] yg akan di-inspeksi oleh metaclass pada library ini.
    Properti ini bersifat abstract jadi harus di-implement pada subclass.
    """

    bool: bool = False
    """Berisi valaue boolean yg akan di-inspeksi oleh metaclass pada library ini."""

    @abstractmethod
    def isImplementationValid(
        this, inspectedCls: Any, supers: Tuple[type],
        inspectedMember: Dict[str, Any]  # , meta: MetaInspectable
    ) -> bool: pass


def createMetaInspectableFrom(obj, name: str = "") -> MetaInspectable[T]:
    """
    Membuat MetaInspectable yg berasal dari sebuah [obj] dg nama [name].
    :param obj: Objek yg dijadikan sebagai MetaInspectable.
    :param name: Nama yg diberikan pada MetaInspecstable.
    :return: MetaInspecstable.
    """
    inspectable = MetaInspectable(obj)
    inspectable.name = name.strip() or obj.__str__()
    return inspectable


def createMetaInspectable(name: str) -> MetaInspectable[T]:
    """
    Membuat MetaInspectable simpel tanpa objek yg di-wrap dg nama [name].
    :param name: Nama yg diberikan pada MetaInspecstable.
    :return: MetaInspecstable.
    """
    return createMetaInspectableFrom(None, name)



"""
class A:
    def ab(self): print("halo A")

    def __str__(self) -> str: return f"Kelas A {self.__hash__()}"


ls = A()
aMet = createMetaInspectableFrom(ls)

#print(f"aMet.content = {aMet.content}")
#print(aMet.plu)
aMet.ab()


print(aMet)
print(aMet.content)
#"""