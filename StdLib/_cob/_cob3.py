
st = """
agaga
agag
  if a:
"""

def ch(fun):
    print(fun)

class C:
    @ch
    def afa(self):pass
    pro = 1

from meta.metameta.MetaAnnotation import MetaAnnotation
from meta.Final import Final
from meta.Annotation import Annotation
from reflex import Reflex

ls = []

print(Reflex.classesTree(MetaAnnotation))
print(Annotation in Reflex.classesTree(MetaAnnotation))
print(Reflex.isSuperclassOf(Annotation, MetaAnnotation))

#print(Reflex.classesTree(ls))

print(isinstance(Final, Annotation))
ann = Final()#()
print(Reflex.isAnnotation(ann))

#from stdlib import *
from sidev.stdlib import *

ls = listOf(1,2,3,4)
ls2 = ls.map(lambda x: f"x={x}")

ls

print(ls2)