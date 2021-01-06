
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

print(f"isinstance((\"a\":1), Iterable) = {isinstance({'a':1}, Iterable)}")

print(ls2)


class F:
    def ad(self): print("haha")
    def ada(self): print("haha")
    def ade(self): print("haha")
    def adafasfaf(self): print("haha")

class G: pass


fina = Final()
f1 = F()
f2 = F()
f3 = F()
f2.apa = "afhoahfa"
f3.apaafaio = "afhoahfa"
f2.apaafaioadad = "afhoahfa"
f2.apaafaioadaafad = "afhoahfaasgna anga a"
f2.aasapaafaioadaafad = "afhoahfaasgna anga a234324fa"

g1 = G()
g2 = G()
g2.opoaa = "afhoahfa"


sf1 = sys.getsizeof(f1)
sf2 = sys.getsizeof(f2)
sf3 = sys.getsizeof(f3)
sg1 = sys.getsizeof(g1)
sg2 = sys.getsizeof(g2)
sfin = sys.getsizeof(fina)

print(f"sf1={sf1}")
print(f"sf2={sf2}")
print(f"sf3={sf3}")
print(f"sg1={sg1}")
print(f"sg2={sg2}")
print(f"sfin={sfin}")



class D(metaclass=MetaInspector):
    @annotate(Final)
    def oklah(self): print("D.oklah()")

class E(D):
    def oklah(self): print("E.oklah()")