from typing import List, Dict, Any, Callable

from exception.IllegalArgumentExc import IllegalArgumentExc
from meta import Meta
from meta.Annotation import Annotation
from meta.metameta.MetaAnnotation import MetaAnnotation
from reflex import Reflex


class Target(MetaAnnotation):
    class _Enum:
        def __init__(this, value: int, name: str, checkFun: Callable[[any], bool]) -> None:
            super().__init__()
            this.value = value
            this.name = name
            this.checkFun = checkFun

        def __str__(this) -> str:
            return this.name

        def __repr__(this) -> str:
            return f"Target of {this.__str__()}"

    CLASS = _Enum(1, "Class", Reflex.isType)
    FUNCTION = _Enum(2, "Function", lambda x: Reflex.isFunction(x) or Reflex.isGenerator(x))
    META = _Enum(3, "Meta", lambda x: isinstance(x, Annotation))
    _DEFAULT = FUNCTION

    def __init__(this, *targets: _Enum):
        if len(targets) == 0 or (len(targets) == 1 and not isinstance(targets[0], Target._Enum)):
            raise IllegalArgumentExc(f"""Argumen untuk anotasi @Target harus int setidaknya berjumlah 1.""")
        super().__init__(None, **{Meta.META_TARGETS_NAME: list(targets)})

    def isImplementationValid(this, inspectedCls: type, supers: List[type], immediateSubclasses: List[type],
                              inspectedUnit: Dict[str, Any]) -> bool:
        return super().isImplementationValid(inspectedCls, supers, immediateSubclasses, inspectedUnit)
