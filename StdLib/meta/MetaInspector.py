import inspect
from abc import ABC, abstractmethod
from typing import Tuple, Dict, Any

from exception.MetaInspectionExc import MetaInspectionExc
from meta.MetaInspectable import MetaInspectable, createMetaInspectable


class MetaInspector(type):
    def __init__(this, name: str, supers: Tuple[type], namespace: Dict[str, Any], **metas: MetaInspectable):
        super().__init__(name, supers, namespace)
        for meta in metas.values():
            for member in namespace.values():
                for nestedMember in inspect.getmembers(member):
                    if isinstance(meta, str):
                        metaName = meta
                        meta = createMetaInspectable(metaName)
                    try:
                        if meta.name == nestedMember[0]:
                            if not meta.isImplementationValid(this, supers, {nestedMember[0] : nestedMember[1]}):
                                raise MetaInspectionExc(f"""Terjadi kesalahan pada kelas: "{name}" implementasi member: "{nestedMember}" dg meta: "{meta}" """)
                            break
                    except AttributeError: raise TypeError("meta harus MetaInspectable atau String.")

"""
    @abstractmethod
    def _isMetaImplementationValid(
        thisInspectedCls: str, supers: Tuple[type],
        inspectedMember: Dict[str, Any], meta: MetaInspectable
    ) -> bool: pass
"""
