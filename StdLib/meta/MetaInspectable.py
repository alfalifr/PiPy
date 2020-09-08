from abc import ABC, abstractmethod
from typing import Dict, Any, List

from exception.MetaInspectionExc import MetaInspectionExc
from foundation.wrapper.FlatWrapper import FlatWrapper
from generic.Generics_ import T
from meta import Meta
from reflex import _Reflex


class MetaInspectable(ABC, FlatWrapper[T]):
    """
    Kelas dasar yg dapat digunakan sbg unit inspeksi yg dicek oleh semua metaclass yg ada di library ini.
    """

    #TODO blum bisa untuk anotasi yg menerima param tambahan.
    def __init__(this, content: T = None, **kwargs):
        """
        :param content: adalah fungsi atau kelas yg ditandai dg anotasi ini.
          Param ini adalah param yg diberikan oleh interpreter yaitu dg menambahkan param tambahan pada akhir decorator.
          Contoh:
            @decorator
            def fun():
              ...
            Hasil terjemahan kode di atas menjadi fun = decorator(fun)
            @decorator(a, b)
            def fun():
              ...
            Hasil terjemahan kode di atas menjadi fun = decorator(a,b)(fun)
          Sebaiknya, jika ingin menambahkan argumen, gunakan keyword.
        :param kwargs: param untuk menambahkan argumen tambahan pada kelas ini saat digunakan sbg decorator.
        """
        print(f"""MetaInspectable __init__ content = {content} this= {this}""")
        if not _Reflex.isAnnotatedUnit(content) and content is not None:
            raise TypeError(f"""MetaInspectable: "{this}" digunakan untuk membungkus sesuatu selain kelas dan fungsi.""")

        super().__init__(content)
        print(f"MetaInspectable.__init__() this = {this} isinstance(this, MetaInspectable)= {isinstance(this, MetaInspectable)}")
        if content is not None:
            #setattr(content, Meta.INSPECTABLE_PROP_NAME, this)
            this._injectThisMeta(content)
            this.injectData(content, **kwargs)
        else:
            #kwargs[Meta.INSPECTABLE_PROP_NAME] = this
            setattr(this, Meta.META_KWARGS_NAME, kwargs)

    name: str = None
    """
    Berisi nama attribut yg berisi nilai [bool: boolean] yg akan di-inspeksi oleh metaclass pada library ini.
    Properti ini bersifat abstract jadi harus di-implement pada subclass.
    """

    bool: bool = False
    """Berisi valaue boolean yg akan di-inspeksi oleh metaclass pada library ini."""

    def injectData(this, content: T, **kwargs):
        for key in kwargs:
            setattr(content, key, kwargs[key])

    def _injectThisMeta(this, content: T):
        print(f"_injectThisMeta mulai this= {this} content= {content}")
        try:
            metaList = content.__dict__[Meta.INSPECTABLE_PROP_NAME]
            print(f"_injectThisMeta metaList= {metaList} this= {this} try berhasil")
            if not isinstance(metaList, list):
                if metaList:
                    metaList = [metaList]
                else: metaList = []
            print(f"_injectThisMeta metaList= {metaList} this= {this} try berhasil 2")
        except KeyError as e:
            print(f"_injectThisMeta e= {e}")
            metaList = []

        metaList.append(this)
        print(f"_injectThisMeta metaList= {metaList} content= {content}")
        setattr(content, Meta.INSPECTABLE_PROP_NAME, metaList)
        print(f"_injectThisMeta metaList= {metaList} content.__dict__[Meta.INSPECTABLE_PROP_NAME]= {content.__dict__[Meta.INSPECTABLE_PROP_NAME]}")

    @abstractmethod
    def isImplementationValid(
        this, inspectedCls: type,
        supers: List[type], immediateSubclasses: List[type], # //Gak berguna karena metaclass dipanggil sebelum subclass di-deklarasikan.
        inspectedUnit: Dict[str, Any]  # , meta: MetaInspectable
    ) -> bool:
        """
        :param inspectedCls: Kelas tempat :param inspectedUnit menempel.
        :param supers: superclass dari :param inspectedCls.
        :param immediateSubclasses: subclass dari :param inspectedCls.
        :param inspectedUnit: Unit yg di-inpeksi, dapat berupa kelas maupun fungsi.
          Jika brupa kelas, maka nilainya sama dg :param inspectedCls.
        :return:
        """
        pass

    def implementationErrorMsg(this) -> str:
        return ""

    def errorImplemetedMember(this):
        return this.content

    def __call__(this, inspectedUnit = None):
        print(f"MetaInspectable this.content= {this.content} inspectedUnit= {inspectedUnit}")
        if this.content is not None:
            res = this.content
        elif inspectedUnit is not None:
            if not _Reflex.isAnnotatedUnit(inspectedUnit):
                raise TypeError(f"""MetaInspectable: "{this}" digunakan untuk membungkus sesuatu selain kelas dan fungsi.""")
            this.injectData(inspectedUnit, **this.__dict__[Meta.META_KWARGS_NAME])
            this._injectThisMeta(inspectedUnit)
            this.content = inspectedUnit
            res = inspectedUnit
        else:
            raise TypeError(f"""MetaInspectable: "{this}" digunakan untuk membungkus sesuatu selain kelas dan fungsi.""")

        """
        if len(this.__class__.__subclasses__()) == 0:
            if _Reflex.isFunction(res) and this.__dict__[Meta.INSPECTABLE_META_TARGET_PROP_NAME] != 2:  # Target.FUNCTION:
                raise MetaInspectionExc(f" ""Meta: "{this}" tidak ditujukan untuk target fungsi, current target: "{res}"." "")
            elif _Reflex.isType(res) and this.__dict__[Meta.INSPECTABLE_META_TARGET_PROP_NAME] != 1:  # Target.CLASS:
                raise MetaInspectionExc(f" ""Meta: "{this}" tidak ditujukan untuk target kelas, current target: "{res}"." "")
        """
        return res

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