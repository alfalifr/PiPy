from abc import ABC, abstractmethod
from typing import Dict, Any, List

from collection._CollectionFun import isEmpty
from foundation.wrapper.FlatWrapper import FlatWrapper
from log.logs import prind
from text.text import contentStr
from val.generic import T
from meta import Meta
from reflex import Reflex


class Annotation(ABC, FlatWrapper[T]):
    """
    Kelas dasar yg dapat digunakan sbg unit inspeksi yg dicek oleh semua metaclass yg ada di library ini.
    Kelas ini dapat digunakan sebagai anotasi yang akan dicek oleh `MetaInspector`.
    """

    def __init__(this, content: T = None, **kwargs):
        """
        *Pastikan semua turunan dari kelas ini memanggil `super().__init__`*

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
        prind(f"""MetaInspectable __init__ content = {content} this= {this}""")
        if not Reflex.isAnnotatedUnit(content) and content is not None:
            raise TypeError(f"""MetaInspectable: "{this}" digunakan untuk membungkus sesuatu selain kelas dan fungsi.""")

        super().__init__(content)
        #prind(f"MetaInspectable.__init__() this = {this} isinstance(this, MetaInspectable)= {isinstance(this, Annotation)}")
        if content is not None and kwargs.__len__() == 0:  # kwargs harus kosong, karena anggapannya param [content] hanya boleh di-pass oleh interpreter.
            #%src{meta_kind}
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

    bool_: bool = False
    """Berisi valaue boolean yg akan di-inspeksi oleh metaclass pada library ini."""

    def injectData(this, content: T, **kwargs):
        for key in kwargs:
            setattr(content, key, kwargs[key])

    def _injectThisMeta(this, content: T):
        prind(f"_injectThisMeta mulai this= {this} content= {content}")
        this._checkTarget(content)
        try:
            metaList = content.__dict__[Meta.INSPECTABLE_PROP_NAME]
            prind(f"_injectThisMeta metaList= {metaList} this= {this} try berhasil")
            if not isinstance(metaList, list):
                if metaList:
                    metaList = [metaList]  # Jika `metaList` tidak None atau sebagainya, maka simpan di list.
                else: metaList = []  # Jika None atau sebagainya, maka buat list kosong.
            prind(f"_injectThisMeta metaList= {metaList} this= {this} try berhasil 2")
        except KeyError as e:
            prind(f"_injectThisMeta e= {e}")
            metaList = []

        metaList.append(this)
        prind(f"_injectThisMeta metaList= {metaList} content= {content}")
        setattr(content, Meta.INSPECTABLE_PROP_NAME, metaList)
        prind(f"_injectThisMeta metaList= {metaList} content.__dict__[Meta.INSPECTABLE_PROP_NAME]= {content.__dict__[Meta.INSPECTABLE_PROP_NAME]}")

    @property
    def targets(this) -> List["Target._Enum"]:
        try: return this.__dict__[Meta.META_TARGETS_NAME]
        except KeyError: return []

    def _checkTarget(this, content: T):
        """
        Mengecek apakah content sesuai `Target` (Target.CLASS, Target.FUNCTION, Target.META,) dari `this` Annotation.
        :param content: objek yang di-anotasi.
        :return:
        """
        if this.__class__.__name__ == "Target": return  # Gak usah dicek kalo `this` adalah anotasi `Target`.
        try:
            targets = this.targets  # content.__dict__[Meta.META_TARGETS_NAME]
            prind(f"Annotation._checkTarget() cls= {this.__class__.__name__} target= {contentStr(targets)} targets.__class__.__name__ = {targets.__class__.__name__}")
            bool_ = isEmpty(targets)
            if targets is not None:
                for target in targets:
                    if target.checkFun(content):
                        bool_ = True
                        break
            if not bool_:
                raise TypeError(f"Param `obj` ({content}) bkn merupakan salah satu dari {contentStr(targets)}")
        except KeyError: pass

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

    def __call__(this, inspectedUnit=None, *args, **kwargs):
        """
        Fungsi ini berguna saat anotasi `MetaInspectable` diberi parameter tambahan.
        Contoh:
            @decorator(a, b)
            def fun():
              ...
            Hasil terjemahan kode di atas menjadi fun = decorator(a,b)(fun)
        Maka tentunya, interpreter Python memanggil fungsi `__call__` dengan parameter `inspectedUnit`.
        :param inspectedUnit:
        :return:
        """
        prind(f"MetaInspectable this.content= {this.content} inspectedUnit= {inspectedUnit}")
        if this.content is not None:
            content = this.content
            res = content(*args, **kwargs) if isinstance(content, type) or Reflex.isFunction(content) \
                else content
            #prind(f"MetaInspectable __call__ res={res} this.content= {this.content} this.content is not None => MASUK")
        elif inspectedUnit is not None:
            if not Reflex.isAnnotatedUnit(inspectedUnit):
                raise TypeError(f"""MetaInspectable: "{this}" digunakan untuk membungkus sesuatu selain {this.targets}.""")
            this.injectData(inspectedUnit, **this.__dict__[Meta.META_KWARGS_NAME])
            this._injectThisMeta(inspectedUnit)
            this.content = inspectedUnit
            res = inspectedUnit
            #prind(f"MetaInspectable __call__ res={res} this.content= {this.content} this.content is not None => GAK MASUK")
        else:
            raise TypeError(f"""Annotation: "{this.__class__.__name__}" digunakan untuk membungkus sesuatu selain {this.targets}.""")

        prind(f"MetaInspectable __call__ res={res} inspectedUnit= {inspectedUnit}")  # this.content={this.content}
        """
        if len(this.__class__.__subclasses__()) == 0:
            if _Reflex.isFunction(res) and this.__dict__[Meta.INSPECTABLE_META_TARGET_PROP_NAME] != 2:  # Target.FUNCTION:
                raise MetaInspectionExc(f" ""Meta: "{this}" tidak ditujukan untuk target fungsi, current target: "{res}"." "")
            elif _Reflex.isType(res) and this.__dict__[Meta.INSPECTABLE_META_TARGET_PROP_NAME] != 1:  # Target.CLASS:
                raise MetaInspectionExc(f" ""Meta: "{this}" tidak ditujukan untuk target kelas, current target: "{res}"." "")
        """
        return res

#    def cob(this): prind(f"MetaInspectable.cob()")


def createMetaInspectableFrom(obj: T, name: str = "") -> Annotation[T]:
    """
    Membuat MetaInspectable yg berasal dari sebuah [obj] dg nama [name].
    :param obj: Objek yg dijadikan sebagai MetaInspectable.
    :param name: Nama yg diberikan pada MetaInspecstable.
    :return: MetaInspecstable.
    """
    inspectable = Annotation(obj)
    inspectable.name = name.strip() or obj.__str__()
    return inspectable


def createMetaInspectable(name: str) -> Annotation[T]:
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