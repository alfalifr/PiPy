from typing import Dict, Any, List

from generic.Generics_ import T
from meta.MetaInspectable import MetaInspectable

#TODO
class MetaMetaInspectable(MetaInspectable):
    """
    Meta dari Meta. Tujuan dari kelas ini adalah untuk menyediakan informasi terkait meta yg digunakan.
    """

    def __init__(this, content: T = None, **kwargs):
        if not (isinstance(content, MetaInspectable) or content is None):
            raise TypeError(f"""Meta: "{this}" hanya untuk MetaInspectable yg lain, bkn untuk content= "{content}".""")
        super().__init__(content, **kwargs)
        print(f"MetaMetaInspectable.__init__() this = {this} isinstance(this, MetaInspectable)= {isinstance(this, MetaInspectable)}")

    def isImplementationValid(this, inspectedCls: type, supers: List[type], immediateSubclasses: List[type],
                              inspectedUnit: Dict[str, Any]) -> bool:
        return True  # Karena MetaMetaInspectable hanya meninjeksi data.
