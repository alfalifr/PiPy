import inspect
from abc import ABC, abstractmethod
from typing import Tuple, Dict, Any, Iterable, List

from exception.IllegalStateExc import IllegalStateExc
from exception.MetaInspectionExc import MetaInspectionExc
from meta.MetaConst import MetaConst
from meta.MetaInspectable import MetaInspectable, createMetaInspectable
from reflex import _Reflex


class MetaInspector(type):
    def __new__(mcls, name: str, supers: Tuple[type], namespace: Dict[str, Any], immediateSubclasses: List[type] = []):
        cls = super().__new__(mcls, name, supers, namespace)
        return cls

    def __init__(cls, name: str, supers: Tuple[type], namespace: Dict[str, Any], immediateSubclasses: List[type] = []):  # **metas: MetaInspectable):
        super().__init__(name, supers, namespace)
        print(f"MetaInspector this= {cls} supers= {supers} this.__subclasses__()= {cls.__subclasses__()} immediateSubclasses= {immediateSubclasses}")

        superList = list(supers)

        for member in namespace.values():
            print(f"MetaInspector member= {member}")
            try: nestedMembers = member.__dict__
            except AttributeError: continue

            for nestedMemberName in nestedMembers:  # Iterasi terhadap dict akan dilakukan pada key-nya.
                nestedMember = nestedMembers[nestedMemberName]
                if isinstance(nestedMember, MetaInspectable):
                    setattr(cls, MetaConst.CLASS_INSPECTABLE_MARK, True)
                    nestedMemberDict = {member.__name__: nestedMember}
                    if not nestedMember.isImplementationValid(cls, superList, immediateSubclasses, nestedMemberDict):
                        msg = nestedMember.implementationErrorMsg().strip() \
                              or f"""Terjadi kesalahan pada kelas: "{name}" implementasi member: "{nestedMember}" dg meta: "{nestedMember.__class__}"."""
                        msg += f"\n   {_Reflex.getLineInfo(nestedMember.errorImplemetedMember())}"
                        raise MetaInspectionExc(msg)
                    break

        superclassTree = _Reflex.superclassesTree(cls, False)
        if len(superclassTree) > 0:
            for sup in superclassTree:
                print(f"MetaInspector cls not in sup.__subclasses__()= {cls not in sup.__subclasses__()}")
                print(f"MetaInspector cls= {cls}")
                print(f"MetaInspector sup.__subclasses__()= {sup.__subclasses__()}")
                try:
                    if sup.__dict__[MetaConst.CLASS_INSPECTABLE_MARK]:
                        print(f"sup.__dict__= {sup.__dict__}")
                        MetaInspector(sup.__name__, sup.__bases__, dict(sup.__dict__), [cls])
                except KeyError: pass



"""
    @abstractmethod
    def _isMetaImplementationValid(
        thisInspectedCls: str, supers: Tuple[type],
        inspectedMember: Dict[str, Any], meta: MetaInspectable
    ) -> bool: pass
"""

"""
def inspectClassMeta(*metas: MetaInspectable):
    def inner(cls):
        if not isinstance(cls, type):
            raise TypeError(f"Anotasi @inspectClassMeta hanya untuk kelas, elemen aktual yg di-anotasi: \"{cls}\"")

        namespace = cls.__dict__
        for meta in metas:
            for member in namespace.values():
                print(f"inspectClassMeta() member= {member}")
                try: nestedMembers = member.__dict__
                except AttributeError: continue
                for nestedMemberName in nestedMembers:  # Iterasi terhadap dict akan dilakukan pada key-nya.
                    try:
                        if meta.name == nestedMemberName:
                            nestedMember = {nestedMemberName : nestedMembers[nestedMemberName]}
                            if not (isinstance(meta, type) and meta.isImplementationValid(member, cls, cls.mro(), nestedMember)) \
                                    (isinstance(meta, MetaInspectable) and meta.isImplementationValid(cls, cls.mro(), cls.__subclasses__(), nestedMember)):
                                raise MetaInspectionExc(f" ""Terjadi kesalahan pada kelas: "{cls.__name__}" implementasi member: "{nestedMember}" dg meta: "{meta}" " "")
                            break
                    except AttributeError: raise TypeError("meta harus MetaInspectable.")
        return cls

    if len(metas) == 1:
        meta = metas[0]
        if not ((isinstance(meta, type) and issubclass(meta, MetaInspectable))
                or isinstance(meta, MetaInspectable)):
            print(f"inspectClassMeta() isinstance(meta, type)= {isinstance(meta, type)}")
            print(f"inspectClassMeta() meta= {meta}")
            print(f"inspectClassMeta() issubclass(meta, MetaInspectable)= {issubclass(meta, MetaInspectable)}")
            print(f"inspectClassMeta() isinstance(meta, type) and issubclass(meta, MetaInspectable)= {isinstance(meta, type) and issubclass(meta, MetaInspectable)}")
            print(f"inspectClassMeta() isinstance(meta, MetaInspectable)= {isinstance(meta, MetaInspectable)}")
            raise TypeError(f"Argumen inspectClassMeta() harus bertipe MetaInspectable, argumen aktual = {meta}")

    return inner
"""