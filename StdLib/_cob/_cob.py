import inspect
from typing import List

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
        setattr(fun, name, nilai)
        return fun
    return inner

class Meta(type):
    clsList: List[str]
    def __init__(mcls, something, b, c):
        cls = super().__init__(something, b, c)
        print(f"something= {something}", f"b= {b}", f"c= {c}",)
        mcls.cobMet()
        return cls

    def cobMet(cls: str):
        print(f"Meta cobMet() cls= {cls}")

class A(metaclass=Meta):
    def __init__(this, a):
        print(f"A init this.ada= {this.ada}")
#        this.ada.ok = 1
    @attach('makmu', 109)
    def ada(this):
        print(f"ada() ok= {this.ada.ok}")

#A.ada.halo = "bro"
class B(A):
    b = 10
    def __init__(this):
        print(f"B init this.ada= {this.ada}")
#        this.ada.ok = 2
"""
    def ada(this):
        print(f"B.ada() ok")
"""

#b = B()
#tup = (A, B)
#print(tup)
#print(Meta())

print("\n============== batas =================\n")
print(B().ada.atch)
print(B().ada.makmu)
for mem in inspect.getmembers(B()):
    print(f"member= {mem[1]}")

def kwarg(**a: str):
    for e in a.values():
        print(e)
    print(a)


kwarg(halo=1, ok=10)

print(isinstance("afa", int))

B().aadd


# type("HaloCls", (B,), {"x": 1})
