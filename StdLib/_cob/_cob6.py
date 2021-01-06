import inspect

import collection
from collection.iterator.Iterator import Iterator
from reflex.Reflex import callerFile

print(Iterator.__module__)

print(inspect.getfile(collection.iterator.Iterator))


#print(inspect.stack(6)[0].filename)

print(callerFile())

from _cob_1 import _cob4

_cob4.privt()