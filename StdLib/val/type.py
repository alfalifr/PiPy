import types
from typing import Union, Callable, Iterable, Iterator

AnnotatedUnit = Union[type, Callable]
IterableLike = Union[Iterable, Iterator, types.GeneratorType]
GeneratorLike = Union[Iterable, types.GeneratorType]
