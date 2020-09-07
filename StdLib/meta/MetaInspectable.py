from abc import ABC, abstractmethod, abstractproperty
from typing import Tuple, Dict, Any, List

from foundation.wrapper.FlatWrapper import FlatWrapper
from generic.Generics_ import T
from meta.MetaConst import MetaConst


class MetaInspectable(ABC, FlatWrapper[T]):
    """
    Kelas dasar yg dapat digunakan sbg unit inspeksi yg dicek oleh semua metaclass yg ada di library ini.
    """
    #TODO blum bisa untuk anotasi yg menerima param tambahan.
    def __init__(this, content: T):
        super().__init__(content)
        setattr(content, MetaConst.INSPECTABLE_PROP_NAME, this)
        this.injectData(content)
        print(f"MetaInspectable.__init__() this = {this} isinstance(this, MetaInspectable)= {isinstance(this, MetaInspectable)}")

    name: str = None
    """
    Berisi nama attribut yg berisi nilai [bool: boolean] yg akan di-inspeksi oleh metaclass pada library ini.
    Properti ini bersifat abstract jadi harus di-implement pada subclass.
    """

    bool: bool = False
    """Berisi valaue boolean yg akan di-inspeksi oleh metaclass pada library ini."""

    def injectData(this, content: T): pass

    @abstractmethod
    def isImplementationValid(
        this, inspectedCls: Any,
        supers: List[type], immediateSubclasses: List[type], # //Gak berguna karena metaclass dipanggil sebelum subclass di-deklarasikan.
        inspectedMember: Dict[str, Any]  # , meta: MetaInspectable
    ) -> bool: pass

    def implementationErrorMsg(this) -> str:
        return ""

    def errorImplemetedMember(this):
        return this.content

#    def cob(this): print(f"MetaInspectable.cob()")


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