from abc import ABC, abstractmethod, abstractproperty
from typing import Tuple, Dict, Any, List

from foundation.wrapper.FlatWrapper import FlatWrapper
from generic.Generics_ import T
from meta.MetaConst import MetaConst
from meta.MetaInspectable import MetaInspectable

#TODO
class MetaMetaInspectable(MetaInspectable):
    """
    Meta dari Meta. Tujuan dari kelas ini adalah untuk menyediakan informasi terkait meta yg digunakan.
    """

    def __init__(this, content: T):
        if not isinstance(content, MetaInspectable):
            raise TypeError(f"""Meta: "{this}" hanya untuk MetaInspectable yg lain, bkn untuk content= "{content}".""")
        super().__init__(content)
        setattr(content, MetaConst.INSPECTABLE_META_PROP_NAME, this)
        print(f"MetaMetaInspectable.__init__() this = {this} isinstance(this, MetaInspectable)= {isinstance(this, MetaInspectable)}")

    def isImplementationValid(this, inspectedCls: Any, supers: List[type], immediateSubclasses: List[type],
                              inspectedMember: Dict[str, Any]) -> bool:
        return True  # Karena MetaMetaInspectable hanya meninjeksi data.

    @abstractmethod
    def injectData(this, content: T): pass
