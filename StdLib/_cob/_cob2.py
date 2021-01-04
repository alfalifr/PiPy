import inspect

from meta.Annotation import Annotation

print("========================== test =====================")

def geno():
    for i in range(2):
        yield i

print(geno())
print(geno().__class__.__name__)

a = geno()

print(a.__next__())
print(a.__next__())
#print(a.__next__())
#print(a.__next__())

#import stdlib
#from collection.iterators import *

#stdlib.NestedIterator
a = 2
#print(eval("""def au(): print("haha")"""))
print(eval(""" lambda x: x """))
#print(inspect.getsource(eval(""" lambda x: x """)))

print(inspect.getsource(Annotation.__init__))

print("af afa".split(" "))

print(exec("""
def au(): print("ahha")
"""))

au()
print(exec("""
if a is not None:
    raise RuntimeError()
"""))