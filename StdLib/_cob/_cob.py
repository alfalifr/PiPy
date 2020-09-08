import inspect
from typing import List


from meta.CallSuper import CallSuper
from meta.Final import Final
from meta.MetaInspectable import MetaInspectable
from meta.MetaInspector import MetaInspector
from meta._Meta import classMeta
from reflex import _Reflex
from stdop.operable.OperableFun_ import toSequence, toList
from stdop.operable.OperableList import listOf
from stdop.operable.OperableSequence import OperableSequence

itr = {'v' : 0}


def transform(itrable):
    itrr = {"itr" : list}
    if isinstance(itrable, OperableSequence):
        itrr["itr"] = seq

    def trans(it):
        itr['v'] += 1
        if itr['v'] not in range(4):
            itrr["itr"].breakItr = True
        return it * 3
    return trans


pList= [*(1,3,2,4)]
print(f"pList= {pList}")
for e in pList: pass

print(f"pList= {pList}")


list= listOf(*[i for i in range(8)])
print(list)
list.append(109)
print(list)
itr = {'v' : 0}
print(list.map(transform(list)))
itr = {'v' : 0}
print(list.map(transform(list)))
itr = {'v' : 0}
print(list.map(transform(list)).reduce(lambda acc, it: acc + it))
print(f"""len= {list.size}""")
print(f"""last= {list.last}""")

seq = toSequence(list)
print(f"seq= {seq}")
itr = {'v' : 0}
print(f"seq2= {seq.map(transform(seq))}")

itr = {'v' : 0}
for e in seq.map(transform(seq)):
    print(f"seq2 e= {e}")

itr = {'v' : 0}
seq2 = seq.map(transform(seq))

print(seq2)


itr = {'v' : 0}
# list2 =
print(
    toList(seq2)
)
print(
    seq2
)

print(
    toList(seq2).filter(lambda it: it < 20 and it % 2 == 0)
)

print(
    toList(seq2).map(lambda it: it * 5)
)

a = 4

print(*[i for i in range(10) if i % a == 0])


def fun():
    print("halo dari fun")

fun.halo = "ok tambahan"

print(fun)
print(fun.halo)
print(fun.__dict__)
#print(fun.ok)

def attach(name: str, nilai):
    def inner(fun):
        fun.atch = 10
        print(f"attach.inner() name= {name} nilai= {nilai}")
        setattr(fun, name, nilai)
        return fun
    return inner

def inspectMeta(*metas: MetaInspectable):
    def innerClassFun(cls):
        name = cls.__name__
        print(f"inspectMeta() name= {name}")
        print(f"inspectMeta() dict= {cls.__dict__}")
        print(f"inspectMeta() members= {inspect.getmembers(cls)}")
#        metas[0].cob()
        return cls
    if len(metas) == 1 and not (issubclass(metas[0], MetaInspectable) or isinstance(metas[0], MetaInspectable)):
        raise TypeError(f"argumen inspectMeta() harus bertipe MetaInspectable, argumen aktual = {metas[0]}")
    return innerClassFun

class Meta(type):
    clsList: List[str]
    def __init__(mcls, something, b, c):
        cls = super().__init__(something, b, c)
        print(f"something= {something}", f"b= {b}", f"c= {c}", f"\"ada\" in c = {'ada' in c}")
        mcls.cobMet()
        return cls

    def cobMet(cls: str):
        print(f"Meta cobMet() cls= {cls}")


@inspectMeta(CallSuper) #@attach("halo", 1091)
class A(metaclass=Meta):
    def __init__(this, a):
        print(f"A init this.ada= {this.ada}")
#        this.ada.ok = 1
    @attach('makmu', 109)
    def ada(this):
        print(f"ada() ok= {this.ada.ok}")
        print(f"ada() 2 ok= {this.ada.ok}")
    def __dict__(this):
        return "haha"
class A2:
    def ada2(this):
        print(f"ada2()")

attr = "bc"
#A.ada.halo = "bro"

#@inspectMeta(CallSuperMeta, CallSuperMeta)
@attach("aka", 1018)
class B(A2, A):
    b = 10
    # [attr] = "101"

    def __init__(this, b):
        print(f"B init this.ada= {this.ada}")
        this.c = b
#        this.ada.ok = 2

class C(B): pass
"""
    def ada(this):
        print(f"B.ada() ok")
"""

#b = B()
#tup = (A, B)
#print(tup)
#print(Meta())

print("\n============== batas =================\n")
b = B(14)
print(b.ada.atch)
print(b.ada.makmu)
print(b.ada.__dict__)
print(B.ada.__dict__)
print(b.__dict__)
print(b.__class__.__dict__)
print(B.mro())
print(C.mro())
#print(B.c)

print("\n============== batas =================\n")
for mem in inspect.getmembers(B(15)):
    print(f"member= {mem[1]}")

def kwarg(**a: str):
    for e in a.values():
        print(f"""kwarg e= {e}""")
    print(a)
def arg(*a: str):
    for e in a:
        print(f"""arg e= {e}""")
    print(a)

kwarg(halo=1, ok=10)
arg(1,2,3)

@property
def propFun(): return "propFun"

print(propFun)

print(isinstance("afa", int))
print(isinstance("afa", str))
print("afa" is str)

#print(f"CallSuperMeta is MetaInspectable = {isinstance(CallSuperMeta, MetaInspectable)}")


print(f"isinstance(CallSuperMeta, type)= {isinstance(CallSuper, type)}")
print(f"isinstance(kwarg, type)= {isinstance(kwarg, type)}")

dick = { 'a':1 }
for d in dick:
    print(f"dick= {d}")

print(dick.keys())


print("\n=================== link =================\n")

print(C.__bases__)
print(A.ada.__dict__)
print(A.ada.__call__)
print(inspect.getsourcelines(A.ada))
print(inspect.getsourcelines(A.ada))
print(inspect.getfile(A.ada))
print(_Reflex.classesTree(B))
print(_Reflex.classesTree(B, False))
print(type(A.__class__).__name__)
print(type(A.ada).__name__)
print(A.ada.__class__.__name__)
print(A.ada.__name__)

print("\n=================== Final Meta =================\n")


class D(metaclass=MetaInspector):
    @Final(a=10, b="halo")
    def ada(this):
        print(f"D.ada()")

    @CallSuper
    def adade(this):
        print(f"D.adade()")


print(f"D.__subclasses__() = {D.__subclasses__()}")

@classMeta(Final(a=10, z="ok"), CallSuper)
class E(D): pass

print(f"E= {E}")
print(f"E()= {E()}")
#print(f"E().__meta_inspectable__= {E().__meta_inspectable__}")
#print(f"E().__meta_inspectable__.__dict__= {E().__meta_inspectable__}")
class F(E):
    def adade(this):
        print(f"F.adade()")

        return super(

        ).adade(

        )

    def ada(this):
        return super().ada()


class G(E): pass



f = F()
f.adade()
print(f"f.adade.__dict__= {f.adade.__dict__}")
#print(f"c.ada.a= {c.ada.a}")


"""    
    def ada(this):
        print(f"C.ada()")
        print(f"C.ada() 2")
"""



# type("HaloCls", (B,), {"x": 1})

print(f"D.__subclasses__() = {D.__subclasses__()}")

print(f"inspect.getmembers(E)= {inspect.getmembers(E)}")
print(f"E.__dict__= {E.__dict__}")

print(D())


class Meta:
    def __init__(this, a, b, **kwargs) -> None:
        super().__init__()
        print("Meta.init", this, a, b)

    def __call__(this, fun):
        print("Meta.call", this, fun)
        return fun

@Meta(1, 2)
class A2: pass

A2()