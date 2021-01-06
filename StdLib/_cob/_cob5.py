import inspect
from typing import Type

from foundation.wrapper.FlatWrapper import FlatWrapper
from meta.Final import Final
#from meta.Private import Private
from reflex.BoundedFun import BoundedFun
from reflex.Property import Property
from reflex.Reflex import memoryAddress

#@Final
class A:
    def __init__(this, a, b, c) -> None:
        this.a = a
        this.b = b
        this.c = c

    def aop(self): return "oklak"

a = A(1, "apa", 40.2)
aW = FlatWrapper(a)
aWW = FlatWrapper(FlatWrapper(a))
#FlatWrapper(FlatWrapper(a))

print(dir(a))
print(dir(aW))
print(f"aW={aW}")
print(f"aW.aop()={aW.aop()}")
print(f"aWW.aop()={aWW.aop()}")

print(f"a.__class__={a.__class__}")
print(f"aW.__class__={aW.__class__}")
print(f"aWW.__class__={aWW.__class__}")
print(f"aW.__ori_class__()={aW.__ori_class__()}")
print(f"aWW.__ori_class__()={aWW.__ori_class__()}")


class B:
    a = Property("aku")
    b = 10
    def ao(self): print("ok")

    def __init__(self) -> None:
        super().__init__()
        self.c = 1098


b = B()

print(b.a)
b.a = "akuaj"
print(b.a)

print(inspect.getmembers(b))

len_ = b.__repr__().__len__()

print(b.__repr__()[len_-11:len_-1])

print(id(b))
print(hex(id(b)))
print(memoryAddress(b))

boundedFun = BoundedFun(b, B.ao)
print(f"boundedFun={boundedFun.__str__()}")