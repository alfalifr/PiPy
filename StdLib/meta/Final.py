from typing import Dict, Any, List

from meta.Annotation import Annotation
from meta.metameta.Target import Target
from reflex import Reflex


@Target(Target.CLASS, Target.FUNCTION)
class Final(Annotation):
    name: str = "Final"

    def isImplementationValid(
        this, inspectedCls: type,
        supers: List[type], immediateSubclasses: List[type],
        inspectedUnit: Dict[str, Any]
    ) -> bool:
        print(f"Final.isImplementationValid() inspectedUnit= {inspectedUnit} immediateSubclasses= {immediateSubclasses}")
        name = list(inspectedUnit.keys())[0]
        unit = inspectedUnit[name]
        this._inspected = unit
        if Reflex.isType(unit):
            if len(immediateSubclasses) > 0:
                this._inspectedImpl = immediateSubclasses[0]
                return False
            return True
        else:
            for sub in immediateSubclasses:
                for methodName in sub.__dict__:
                    if name == methodName:
                        this._subCls = sub
                        this._inspectedImpl = sub.__dict__[methodName]
                        return False
        return True

    def implementationErrorMsg(this) -> str:
        if Reflex.isFunction(this._inspected):
            return f"""Method: "{this._inspected}" final, namun di-override pada kelas: "{this._subCls}"."""
        elif Reflex.isType(this._inspected):
            return f"""Kelas: "{this._inspected}" final, namun di-extend oleh kelas: "{this._inspected.__subclasses__()}"."""

    def errorImplemetedMember(this):
        return this._inspectedImpl






