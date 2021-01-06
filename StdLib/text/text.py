
from typing import Callable, Iterable

from collection._CollectionFun import isEmpty
from val.generic import T_out


def isBlank(s: str) -> bool:
    return True if not s else False


def isNotBlank(s: str) -> bool:
    return not isBlank(s)


def contentStr(
    obj: Iterable[T_out],
    sep: str = ", ",
    prefix: str = None,
    suffix: str = None,
    contentToStrFun: Callable[[T_out], str] = lambda x: x.__str__()
) -> str:
    if not isinstance(obj, Iterable):
        return obj.__str__()

    if prefix is None:
        prefix = "[" if isinstance(obj, list) \
            else "{" if isinstance(obj, dict) or isinstance(obj, set) \
            else prefix

    if suffix is None:
        suffix = "]" if isinstance(obj, list) \
            else "}" if isinstance(obj, dict) or isinstance(obj, set) \
            else suffix

    if isEmpty(obj):
        return prefix +suffix

    getContentFun = lambda x: x if isinstance(obj, list) or isinstance(obj, set) \
        else lambda x: obj[x]

    itr = obj.__iter__()
    res = prefix +itr.__next__().__str__()

    try:
        while True:
            e = itr.__next__()
            eStr = contentToStrFun(getContentFun(e))
            res += sep +eStr
    except StopIteration: pass

    res += suffix
    return res
