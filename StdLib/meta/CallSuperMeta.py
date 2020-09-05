from typing import Tuple, Dict, Any

from generic.Generics_ import T
from meta.MetaInspectable import MetaInspectable
from meta.MetaInspector import MetaInspector


class CallSuperMeta(MetaInspectable):
    name: str = "CallSuper"

    def __init__(this):
        super().__init__(None)

    def isImplementationValid(
        this, inspectedCls: Any,
        supers: Tuple[type], inspectedMember: Dict[str, Any]
    ) -> bool:



