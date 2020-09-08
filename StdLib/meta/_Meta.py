from typing import Union, Type

from meta.MetaInspectable import MetaInspectable
from meta.MetaInspector import MetaInspector


def classMeta(*metas: Union[MetaInspectable, Type[MetaInspectable]]):
    print(f"classMeta() metas= {metas}")
    def inner(cls: type):
        print(f"classMeta().inner() cls= {cls}")
        for meta in metas:
            meta(cls) #.isImplementationValid(cls, list(cls.__bases__), list(cls.__subclasses__()), {cls.__name__: cls})
            MetaInspector(cls.__name__, cls.__bases__, dict(cls.__dict__))
        return cls
    return inner
