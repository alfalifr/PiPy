import inspect
from typing import List

from meta import Meta


def isType(obj) -> bool:
    return isinstance(obj, type)


def isFunction(obj) -> bool:
    return obj.__class__.__name__ == "function"


def isAnnotatedUnit(obj) -> bool:
    return isType(obj) or isFunction(obj)


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


def getLineInfo(member) -> str:
    fileName = inspect.getfile(member)
    lineNo = inspect.getsourcelines(member)[1]
    name = member.__name__

    return f"""File "{fileName}", line {lineNo}, in {name}"""
