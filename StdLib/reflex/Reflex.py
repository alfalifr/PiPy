import gc
import inspect
import logging
import sys
import types
from typing import List, Callable, Optional

from log.logs import prind
from meta import Meta
from val.generic import R, T


def isType(obj) -> bool:
    return isinstance(obj, type)


def isFunction(obj) -> bool:
    boo = hasattr(obj, "__call__") and not isinstance(obj, type)  #obj.__class__.__name__ == "function"
    #print(f"isFunction() obj={obj} bool={boo}")
    return boo


def isConstructor(obj) -> bool:
    """Apakah [obj] merupakan fungsi `__new__` dari sebuah kelas."""
    if not isFunction(obj): return False
    name = obj.__name__ if hasattr(obj, "__name__") else ""
    #print(f"isConstructor() obj={obj} name={name}")
    return name == "__new__"  #obj.__class__.__name__ == "function"


def isGenerator(obj) -> bool:
    return isinstance(obj, types.GeneratorType) # obj.__class__.__name__ == "generator"


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


def fullName(cls: type) -> str:
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


def lineInfo(member) -> str:
    fileName = inspect.getfile(member)
    lineNo = inspect.getsourcelines(member)[1]
    name = member.__name__

    return f"""File "{fileName}", line {lineNo}, in {name}"""


def callerFile(offset: int = 0) -> str:
    return inspect.getfile(sys._getframe(1+offset).f_code)


def caller(offset: int = 0):
    """
    Mengambil fungsi yang memanggil fungsi ini.
    :param offset: merupakan offset stack fungsi yang memanggil fungsi ini.
       Contoh:
         Stack: 0. caller()
                1. B
                2. C
         Jika [offset] == 1, maka fungsi yang di-return adalah C.
    :return: fungsi yang memangil fungsi ini atau `None` jika caller merupakan `<module>`.
    """
    """
    stack = inspect.stack()
    return stack[1 + offset][3]
    """
    lineCode = sys._getframe(1 +offset).f_code
    res = gc.get_referrers(lineCode)
    #prind(f"Reflex.caller() lineCode={lineCode} res={res} offset={offset}")
    return res[0] if res.__len__() > 0 else None


def callerClass(offset: int = 0, onlyClass: bool = True):
    caller_ = caller(offset +1)
    if not caller_: return None
    clsName = callerClassName(onlyClass=onlyClass, caller_=caller_, qualName=False)
    #prind(f"Reflex.callerClass() offset={offset} caller_={caller_} clsName={clsName}")
    return getattr(inspect.getmodule(caller_), clsName) if clsName else None


def callerClassName(
    offset: int = 0,
    onlyClass: bool = True,
    caller_: Callable = None,
    qualName: bool = True
) -> Optional[str]:
    if not caller_:
        caller_ = caller(offset +1)
    prind(f"callerClassName.caller_={caller_} inspect.getmodule(caller_)={inspect.getmodule(caller_)}")
    if not caller_: return None
    try: return caller_.im_class.__name__
    except AttributeError:
        try:
            clsName = boundClassName(caller_, qualName)  #caller_.__qualname__.rsplit('.', 1)[0]
            prind(f"callerClassName.clsName={clsName}")
            return clsName if not (onlyClass and clsName == caller_.__name__) else None
        except AttributeError: return None


def boundClassName(fun: Callable, qualName: bool = True) -> Optional[str]:
    clsName = fun.__qualname__.rsplit('.', 1)[0]
    prind(f"boundClassName.clsName={clsName}")
    #.split('.<locals>', 1)[0]
    funNameList = fun.__qualname__.split(".")
    if not qualName:
        return funNameList[funNameList.__len__() -2]
    #end = funNameList.__len__() -1
    #start = 0 if qualName else end -1

    #itr = funNameList.__iter__()
    name = funNameList[0]  #itr.__next__()

    for i in range(1, funNameList.__len__() -1):
        name += "." + funNameList[i]

    name = inspect.getmodule(fun).__name__ + "." + name
    return name


def qualName(cls: type) -> str:
    modStr = cls.__module__
    return modStr + "." + cls.__name__


def copyMember(
        fromObj, toObj,
        predicate: Callable[[any], bool] = None,
        transformFun: Callable[[T], R] = None
):
    for name, member in inspect.getmembers(fromObj, predicate):
        #print(f"copyMember().name= {name} member= {member} fromObj= {fromObj} toObj= {toObj}")
        try:
            new = transformFun(member) if transformFun else member
            setattr(toObj, name, new)
        except:
            toObjStr = "<toObj>"
            try:
                try: toObjStr = toObj.__class__
                except: toObjStr = toObj.__str__()
            except: pass
            try: logging.warning(f"copyMember() ({fromObj} -> {toObjStr}): Tidak dapat men-copy member: \"{name} : {member}\".")
            except: pass


def memoryAddress(obj) -> str:
    return hex(id(obj))
