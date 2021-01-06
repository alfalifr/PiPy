import inspect
from typing import Type

from log.logs import prind
from meta.Private import Private
from reflex.Reflex import caller, callerClass, callerClassName
from text.text import contentStr
import sys, gc
"""
p1 = 1
p2 = 2

baris1 = [2,1,1,3]
baris2 = [0,0,0,3]
baris3 = [0,0,0,4]
baris4 = [0,0,0,4]
arr = [baris1, baris2, baris3, baris4]

x = 0
y = 0
limit = 5
sum = 0
for i in range(arr.__len__()):
    if arr[y][i] == p1:
        sum += 1
    else:
        sum = 0

    if sum >= limit:
        return True

    return False

for i in range(arr.__len__()):
    if arr[i][x] != p1:
        return False
    return True


for i in range(arr.__len__()):
    if arr[y+i][x+i] != p1:
        return False
    return True

    if arr[y+i][n+x-i] != p1:
        return False
    return True
"""

def f2():
   curframe = inspect.currentframe()
   calframe = inspect.getouterframes(curframe, 4)

   print('caller name:', calframe[1][3])
   #print(calframe[1].f_code())
   print(f"f2.caller()={caller()}")
   print(f"f2.callerClass()={callerClass()}")
   print("aufagajg ======= agag caller:", calframe[1][3])
   print(contentStr(inspect.stack(2), sep="\n"))
   print("===== yss =========")
   print(gc.get_referrers(sys._getframe(1).f_code)[0])


def f1(): f2()

class O:
    def o1(self): f2()
    def o2(self): print(callerClass())

#f2()
#f1()
o = O()
print(O.o1)
print(o.o1)
o.o1()
print("-=== jngoai ====")
o.o2()
print("-===++A jngoai ====")
print(o.o1.__self__.__class__)
print(o.o1.__self__.__class__)
#print(f1.__self__)
print(f"caller()={caller()}")
print(f"callerClass()={callerClass()}")


class prop:
    def __init__(this, prop) -> None:
        super().__init__()
        this.prop = prop

    def __get__(this, *var):
        print(f"var={var}")
        return "avc" if this else 1

    def __getattr__(this=None, *var):
        print(f"var={var}")
        setattr()
        return "this.prop" if this else 10

class private:
    _bound = None
    def _checkScope(this):
        print(f"this._bound={this._bound} callerClassName(2, False)={callerClassName(2, False)}")
        if this._bound != callerClassName(2, False):
            raise TypeError()

    def __init__(this, prop) -> None:
        super().__init__()
        this._bound = callerClassName(1, False)
        print(f"__init__ this._bound={this._bound}")
        this.prop = prop

    def __get__(this, *var):
        this._checkScope()
        print(f"var={var}")
        return "avc" if this else 1

    def __getattr__(this=None, *var):
        print(f"var={var}")
        setattr()
        return "this.prop" if this else 10

print(" = a-=f asf jias ")

@Private
class A:
    ar = "halo"
    priv = private(3)

    #@property
    def aag(self): return 1

    @Private
    def priva(self): return "ajufaofoa"

    def priva2(self):
        prind(f"A.priva2() self.__class__={self.__class__} __self_class__={self.__class__.__self_class__}")
        return self.priva()

    @property
    def __class__(self: "A") -> Type["A"]:
        print("A.__class__")
        return super().__class__()

    def __init__(self) -> None:
        super().__init__()
        print(f"self.priv={self.priv}")



A.ar = prop("a")
a = A()
#a.ar = 11294
print(a.aag)
#a.aag = 2
print(a.aag)

print(a.aag.__class__)
print(a.ar)
print(f"a.priva2={a.priva2}")
print(f"a.priva2()={a.priva2()}")
print(A)
print(a)
#print(a.priva)
#print(a.priv)

@Private
def privt(): print("halo bro")

print(privt())
print(privt)