import inspect
from typing import List


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
