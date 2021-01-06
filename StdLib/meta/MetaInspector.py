import inspect
from abc import ABC, abstractmethod
from typing import Tuple, Dict, Any, Iterable, List

from exception.IllegalStateExc import IllegalStateExc
from exception.MetaInspectionExc import MetaInspectionExc
from meta import Meta
from meta.Annotation import Annotation
from reflex import Reflex


class MetaInspector(type):
    """
    Kelas yang dapat mengecek `MetaInspectable`. Kelas ini digunakan sebagai metaclass oleh kelas
    yang memiliki anotasi berupa turunan `MetaInspectable`.
    """
    def __new__(mcls, name: str, supers: Tuple[type], namespace: Dict[str, Any], immediateSubclasses: List[type] = []):
        cls = super().__new__(mcls, name, supers, namespace)
        return cls

    def __init__(cls, name: str, supers: Tuple[type], namespace: Dict[str, Any], immediateSubclasses: List[type] = []):  # **metas: MetaInspectable):
        super().__init__(name, supers, namespace)
        print(f"MetaInspector this= {cls} supers= {supers} this.__subclasses__()= {cls.__subclasses__()} immediateSubclasses= {immediateSubclasses}")

        superList = list(supers)

        def inspectMember(inspectable: Annotation):
            inspectedMember = inspectable.content
            print(f"MetaInspector.init.inspectMember() inspectedMember= {inspectedMember}")
            nestedMemberDict = {inspectedMember.__name__: inspectedMember}
            if not inspectable.isImplementationValid(cls, superList, immediateSubclasses, nestedMemberDict):
                msg = inspectable.implementationErrorMsg().strip() \
                      or f"""Terjadi kesalahan pada kelas: "{name}" implementasi member: "{inspectedMember}" dg meta: "{inspectedMember.__class__}"."""
                msg += f"\n   {Reflex.lineInfo(inspectable.errorImplemetedMember())}"
                raise MetaInspectionExc(msg)

        # Pengecekan untuk @Target(Target.FUNCTION)
        # Pengecekan untuk @Target(Target.FUNCTION)
        # 1. Pengecekan `MetaInspectable` pada `this`, yaitu mencari member yang memiliki namespace `Meta.INSPECTABLE_PROP_NAME`.
        for memberName in namespace:
            member = namespace[memberName]
            print(f"MetaInspector member= {member} memberName= {memberName}")
            try: print(f"MetaInspector member= {member} memberName= {memberName} dict= {member.__dict__}")
            except: pass
            if memberName == Meta.INSPECTABLE_PROP_NAME:
                if not isinstance(member, list): continue
                isMemberAnnotated = False
                for inspectable in member:
                    if not isinstance(inspectable, Annotation): continue
                    print(f"MetaInspector cls= {cls} member= {member} Meta.INSPECTABLE_PROP_NAME= {Meta.INSPECTABLE_PROP_NAME}")
                    isMemberAnnotated = True
                    inspectMember(inspectable)
                if isMemberAnnotated:
                    setattr(cls, Meta.CLASS_INSPECTABLE_MARK, True)
                    print(cls.__dict__[Meta.CLASS_INSPECTABLE_MARK])
                continue

            # 2. Pengecekan `MetaInspectable` pada nested member.
            #  Jika tidak ditemukan member dengan namespace selain `Meta.INSPECTABLE_PROP_NAME`,
            #  maka inspect membernya. Contohnya seperti member dengan tipe fungsi atau property,
            #  maka yang dicek adalah member dari fungsi atau property, atau `nested member`.
            try: nestedMembers = member.__dict__
            except AttributeError: continue

            for nestedMemberName in nestedMembers:  # Iterasi terhadap dict akan dilakukan pada key-nya.
                nestedMember = nestedMembers[nestedMemberName]
                print(f"MetaInspector nestedMemberName= {nestedMemberName} nestedMember= {nestedMember} isinstance(nestedMember, MetaInspectable)= {isinstance(nestedMember, Annotation)}")

                #print(f"MetaInspector nestedMember= {nestedMember} inspectables= {inspectables} isinstance(nestedMember, MetaInspectable)= {isinstance(nestedMember, MetaInspectable)}")
                if not isinstance(nestedMember, list): continue
                isMemberAnnotated = False
                for inspectable in nestedMember:
                    if not isinstance(inspectable, Annotation): continue
                    print(f"MetaInspector inspectable = {inspectable} this = {cls}")
                    print(f"MetaInspector inspectable.content= {inspectable.content}")
                    print(f"MetaInspector _Reflex.isType(inspectable.content)= {Reflex.isType(inspectable.content)}")
                    print(f"MetaInspector _Reflex.isFunction(inspectable.content)= {Reflex.isFunction(inspectable.content)}")
                    isMemberAnnotated = True
                    inspectMember(inspectable)
                if isMemberAnnotated:
                    setattr(cls, Meta.CLASS_INSPECTABLE_MARK, True)
                break

        superclassTree = Reflex.superclassesTree(cls, False)

        # 3. Cek `MetaInspectable` pada superclassTree.
        print(f"MetaInspector fullName= {Reflex.fullName(cls)} superclassTree= {superclassTree} dict= {cls.__dict__}")
        if len(superclassTree) > 0:
            for sup in superclassTree:
                print(f"MetaInspector sup= {sup} qualname= {sup.__qualname__}")
                print(f"MetaInspector sup.__subclasses__()= {sup.__subclasses__()}")
                print(f"sup.__dict__= {sup.__dict__}")
                print(f"MetaInspector cls not in sup.__subclasses__()= {cls not in sup.__subclasses__()}")
                print(f"MetaInspector cls= {cls}")
                try:
                    if sup.__dict__[Meta.CLASS_INSPECTABLE_MARK]:
                        MetaInspector(sup.__name__, sup.__bases__, dict(sup.__dict__), [cls])
                except KeyError as e:
                    print(f"MetaInspector sup= {sup} lagi error e= {e} sup.__dict__= {sup.__dict__}")
                    if Reflex.getInspectable(sup):
                        print(f"MetaInspector sup= {sup} lagi error e= {e} masuk if")
                        MetaInspector(sup.__name__, sup.__bases__, dict(sup.__dict__), [cls])



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