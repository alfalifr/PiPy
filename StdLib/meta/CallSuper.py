import inspect
import re
from typing import Dict, Any, List

from meta.Annotation import Annotation
from meta.metameta.Target import Target


@Target(Target.FUNCTION)
class CallSuper(Annotation):
    name: str = "CallSuper"

    def isImplementationValid(
        this, inspectedCls: type,
        supers: List[type], immediateSubclasses: List[type],
        inspectedUnit: Dict[str, Any]
    ) -> bool:
        name = list(inspectedUnit.keys())[0]
        patternStr = f"super\\s*\\([\\s\\S]*\\)\\.{name}\\s*\\([\\s\\S]*\\)"

        for sub in immediateSubclasses:
            for methodName in sub.__dict__:
                if name == methodName:
                    this._subCls = sub
                    this._meth = inspectedUnit[name]
                    this._subMeth = sub.__dict__[methodName]
                    src = inspect.getsource(this._subMeth)
                    if re.search(patternStr, src):
                        return True
                    return False
        return True

    def implementationErrorMsg(this) -> str:
        return f"""Method: "{this._meth}" CallSuper, namun method override pada kelas: "{this._subCls}" tidak memanggil super."""

    def errorImplemetedMember(this):
        return this._subMeth



