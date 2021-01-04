from typing import Dict, Any, List

from meta.Annotation import Annotation
from reflex import Reflex


class MetaAnnotation(Annotation):
    """
    Meta dari Meta (Annotation). Tujuan dari kelas ini adalah untuk menyediakan informasi terkait meta yg digunakan.
    """

    def __init__(this, content: Annotation = None, **kwargs):
        if not (isinstance(content, Annotation) or content is None):
            raise TypeError(f"""MetaAnnotation: "{this}" hanya untuk `{Annotation.__name__}` yg lain, bkn untuk content= "{content}".""")
        super().__init__(content, **kwargs)
        print(f"MetaMetaInspectable.__init__() this = {this} isinstance(this, MetaInspectable)= {isinstance(this, Annotation)}")


    def isImplementationValid(
            this, inspectedCls: type, supers: List[type],
            immediateSubclasses: List[type], inspectedUnit: Dict[str, Any]
    ) -> bool:
        return True  # Karena MetaMetaInspectable hanya meninjeksi data.

    def __call__(this, inspectedUnit=None):
        res = this.content if this.content is not None else inspectedUnit
        print(f"MetaAnnotation.__call__() res= {res} cls= {this.__class__.__name__}")
        if (not Reflex.isSuperclassOf(Annotation, res)) or res is None:
            raise ValueError(f"MetaAnnotation ({this.__class__.__name__}) harus digunakan ke `Annotation` lainnya.")
        return super().__call__(inspectedUnit)


