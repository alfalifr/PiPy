from typing import Tuple, Dict, Any, List

from generic.Generics_ import T
from meta.MetaInspectable import MetaInspectable
from meta.MetaInspector import MetaInspector


class Final(MetaInspectable):
    name: str = "Final"

    def isImplementationValid(
        this, inspectedCls: Any,
        supers: List[type], immediateSubclasses: List[type],
        inspectedMember: Dict[str, Any]
    ) -> bool:
        name = list(inspectedMember.keys())[0]
        for sub in immediateSubclasses:
            for methodName in sub.__dict__:
                if name == methodName:
                    this._subCls = sub
                    this._meth = inspectedMember[name]
                    this._subMeth = sub.__dict__[methodName]
                    return False
        return True

    def implementationErrorMsg(this) -> str:
        return f"""Method: "{this._meth}" final, namun di-override pada kelas: "{this._subCls}"."""

    def errorImplemetedMember(this):
        return this._subMeth






