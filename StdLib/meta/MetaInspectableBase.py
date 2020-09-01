from abc import ABC, abstractmethod, abstractproperty

from foundation.wrapper.FlatWrapper import FlatWrapper
from generic.Generics_ import T


class MetaInspectableBase(FlatWrapper[T]):
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


def createMetaInspectableFrom(obj, name: str = "") -> MetaInspectableBase[T]:
    inspectable = MetaInspectableBase(obj)
    inspectable.name = name.strip() or obj.__str__()
    return inspectable



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