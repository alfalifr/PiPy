from typing import Iterable

from collection.List import listOf

print(isinstance([1,2,3,4], Iterable))
ls = listOf(1,2,3,4)
#ls.isImmutable = True
print(f"1 in range(0, 10)={1 in range(0, 10)}")
ls.append(10)
ls.extend([11, 20, 30])
ls.forEach(lambda x: print(f"hoyeah NON x={x}"))
print()
ls.map(lambda x: f"x={x}").forEach(lambda x: print(f"hoyeah x={x}"))
print()
print(ls)
print(ls.map(lambda x: f"x={x}"))
print(ls.map(lambda x: f"x={x}").reduce(lambda acc, x: acc+x))
print(ls.reduce(lambda acc, x: acc + x))
print(ls.map(lambda x: x*2).reduce(lambda acc, x: acc + x))
print(ls.reduce(lambda acc, x: acc * x))
print(ls.reduce(lambda acc, x: acc - x))
print(ls.reduce(lambda acc, x: x - acc))
print(ls.map(lambda x: x*2).reduce(lambda acc, x: x - acc))
