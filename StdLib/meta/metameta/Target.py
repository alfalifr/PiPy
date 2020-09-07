from typing import Any, List, Dict

from generic.Generics_ import T
from meta.MetaConst import MetaConst
from meta.metameta.MetaMetaInspectable import MetaMetaInspectable


class Target(MetaMetaInspectable):
    CLASS = 1
    FUNCTION = 2

    def injectData(this, content: T):
        setattr(content, MetaConst.INSPECTABLE_META_RETENTION_PROP_NAME, "")
