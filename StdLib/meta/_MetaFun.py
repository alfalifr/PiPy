from typing import Union, Type

from meta.Annotation import Annotation
from meta.MetaInspector import MetaInspector


def classMeta(*metas: Union[Annotation, Type[Annotation]]):
    """
    Fungsi yang digunakan untuk memberikan kelas beberapa `metas`
    :param metas: `MetaInspectable` yang ditambahkan ke kelas yang didekorasi oleh fungsi ini.
    :return: Kelas yang didekorasi oleh fungsi ini.
    """
    print(f"classMeta() metas= {metas}")
    def inner(cls: type):
        print(f"classMeta().inner() cls= {cls}")
        for meta in metas:
            meta(cls) #.isImplementationValid(cls, list(cls.__bases__), list(cls.__subclasses__()), {cls.__name__: cls})
            print(f"classMeta().inner() members= {cls.__dict__}")
            MetaInspector(cls.__name__, cls.__bases__, dict(cls.__dict__))
        return cls
    return inner
