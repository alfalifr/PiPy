import inspect
from typing import List, Iterable

from meta import Meta


def isType(obj) -> bool:
    return isinstance(obj, type)


def isFunction(obj) -> bool:
    return obj.__class__.__name__ == "function"


def isGenerator(obj) -> bool:
    return obj.__class__.__name__ == "generator"


def isAnnotatedUnit(obj) -> bool:
    return isType(obj) or isFunction(obj) or isGenerator(obj)


def isAnnotation(obj) -> bool:
    for cls in classesTree(obj.__class__, False):
        if cls.__name__ == "Annotation":
            return True
    return False


def hasInspectable(obj) -> bool:
    try:
        if obj.__dict__[Meta.INSPECTABLE_PROP_NAME]:
            return True
        return False
    except AttributeError: return False


def getInspectable(obj):
    print(f"getInspectable() obj= {obj}")
    try: return obj.__dict__[Meta.INSPECTABLE_PROP_NAME]
    except (KeyError, AttributeError): return None


def getFullName(cls: type) -> str:
    return f"{cls.__module__}.{cls.__qualname__}"


def classesTree(cls: type, includeObjectCls: bool = True) -> List[type]:
    clss = cls.mro()
    if not includeObjectCls:
        clss.remove(object)
    return clss


def superclassesTree(cls: type, includeObjectCls: bool = True) -> List[type]:
    supers = classesTree(cls, includeObjectCls)
    supers.remove(cls)
    return supers


def isSuperclassOf(super: type, sub: type) -> bool:
    return super in superclassesTree(sub)


def isSubclassOf(sub: type, super: type) -> bool:
    return isSuperclassOf(super, sub)


def getLineInfo(member) -> str:
    fileName = inspect.getfile(member)
    lineNo = inspect.getsourcelines(member)[1]
    name = member.__name__

    return f"""File "{fileName}", line {lineNo}, in {name}"""
