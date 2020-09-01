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
print(f"""len= {list.length}""")
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