#from _typeshed import SupportsLessThan, SupportsLessThanT
from typing import Any, List as PyList, Callable, overload, Union, Iterator

from collection.iterator.SkippingIterator import skippingIteratorOf
from exception.IllegalStateExc import IllegalStateExc
from exception.NoSuchElementExc import NoSuchElementExc
from log.logs import prind
from reflex.Property import BoundedImmutableProperty
from val.generic import T, T_out, R
from collection.Iterable import Iterable
from val.type import IterableLike


class List(Iterable[T], PyList[T]):
    """
    Kelas yg berisi sekumpulan data yg mirip dg List dg fungsi tambahan.
    """

    _itrIndex = 0
    isImmutable: bool = False

    def __init__(this, origin: IterableLike = None):
        super().__init__(origin, overwriteExisting=False)

    def filter(this, op: Callable[[T_out], bool]) -> "List[T]":
        # print(f"OprList filter() op= ${inspect.getsource(op)} *[e for e in this.content]= {[e for e in this.content]}")
        itr_ = skippingIteratorOf(this, skipFun=op)
        return listOf(itr_)

    def map(this, op: Callable[[T], R]) -> "List[R]":  #(lambda it: object)
        """
        Fungsi yg digunakan untuk mengubah isi dari `this.content` menjadi newList dg tipe data apapun itu
        hasilnya yg di hasilkan oleh :param op.

        :param op: lambda untuk operasi `map` dg param
          -`it` adalah isi dari `this.content` pada setiap iterasinya.

        :return: newList dg tipe OperableList dg isi sesuai hasil :param op.
        """
        # print(f"OprList map() op= {inspect.getsource(op)}")

        #this.breakItr = False
        this._itrIndex = 0
        newList = []
        for e in this.content:
            #prind(f"List.map() for e={e}")
            #if this.breakItr: break
            newList.append(op(e))
        newList = List(newList)
        #prind(f"List.map() newList={newList}")
        this._itrIndex = 0
        return newList

    def reduce(this, op: Callable[[T, T], T]) -> T:  # (lambda accumulation, it: object)
        """
        Fungsi yg digunakan untuk mengubah isi dari `this.content` menjadi sebuah `accumulation`
        yg betipe data sama dg isi dari `this.content`.

        :param op: lambda untuk operasi `reduce` dg param
          -`accumulation` adalah akumulasi hasil perubahan isi dari `this.content` yg bertipe data sama pula.
          -`it` adalah isi dari `this.content` pada setiap iterasinya.

        :return: object `accumulation` hasil reduce yg bertipe data sama dg isi dari `this.content`.
        """

        #prind(f"List.reduce() this.isEmpty={this.isEmpty} this.size={this.size}")

        if this.isEmpty: return None
        acc = {"val" : this.first}

        def opForMap(it):
            #prind(f"List.reduce() acc[\"val\"]={acc['val']}")
            acc["val"] = op(acc["val"], it)  # or this.content[this._itrIndex]

        this.forEach(opForMap, 1)
        return acc["val"]

    @property
    def size(this) -> int:
        return len(this.content)

    @property
    def first(this) -> T:
        try: return this.content[0]
        except: raise NoSuchElementExc("List kosong.")

    @property
    def last(this) -> T:
        try: return this.content[this.size - 1]
        except: raise NoSuchElementExc("List kosong.")

    def __getitem__(this, index: int) -> T:
        return this.content[index]

    def __setitem__(this, index: int, value: T) -> T:
        this._checkImmutability()
        old = this.content[index]
        this.content[index] = value
        return old

    def _checkImmutability(this):
        #prind(f"List._checkImmutability() this.isImmutable={this.isImmutable}")
        if this.isImmutable:
            raise IllegalStateExc(f"List ini immutable, tidak bisa diubah isinya.")

    """
    Dikomen karena mengakibatkan circular import.
    def asSequence(this) -> OperableSequence[T]:
        " ""
        Mengubah kelas ini menjadi sequence.
        :return:
        " ""
        return OperableSequence(this.content)
    """

    @BoundedImmutableProperty
    def append(this, __object: T) -> bool:
        this._checkImmutability()
        this._callDelegateFun(__object)
        #super().append(__object)
        return True

    @BoundedImmutableProperty
    def remove(this, __value: T) -> bool:
        this._checkImmutability()
        try:
            this._callDelegateFun(__value)
            #super().remove(__value)
            return True
        except ValueError:
            return False

    @BoundedImmutableProperty
    def clear(this) -> bool:
        this._checkImmutability()
        this._callDelegateFun()
        #super().clear()
        return True

    @BoundedImmutableProperty
    def insert(this, __index: int, __object: T) -> bool:
        this._checkImmutability()
        this._callDelegateFun(__index, __object)
        #super().insert(__index, __object)
        return True

    @BoundedImmutableProperty
    def extend(this, __iterable: Iterable[T]) -> bool:
        this._checkImmutability()
        this._callDelegateFun(__iterable)
        #super().extend(__iterable)
        return True

    @BoundedImmutableProperty
    def reverse(this) -> bool:
        this._checkImmutability()
        this._callDelegateFun()
        #super().reverse()
        return True

    @BoundedImmutableProperty
    def pop(this, __index: int = last) -> T:
        this._checkImmutability()
        return this._callDelegateFun(__index)
        #return super().pop(__index)

    """
    @overload
    def sort(this, *, key: None = ..., reverse: bool = False) -> None:
        this._checkImmutability()
        super().sort(key=key, reverse=reverse)

    @overload
    def sort(this, *, key: Callable[[T], SupportsLessThan], reverse: bool = False) -> None:
        this._checkImmutability()
        super().sort(key=key, reverse=reverse)
    """

    @BoundedImmutableProperty
    def sort(this, *, key: None = ..., reverse: bool = False) -> None:
        this._checkImmutability()
        this._callDelegateFun(key=key, reverse=reverse)
        #super().sort(key=key, reverse=reverse)

    @BoundedImmutableProperty
    def __delitem__(this, i: Union[int, slice]) -> T:
        this._checkImmutability()
        old = this[i]
        this._callDelegateFun(i)
        #super().__delitem__(i)
        return old

    @BoundedImmutableProperty
    def __iadd__(this, x: Iterable[T]):
        this._checkImmutability()
        this._callDelegateFun(x)
        #super().__iadd__(x)

    @BoundedImmutableProperty
    def __imul__(this, n: int):
        this._checkImmutability()
        this._callDelegateFun(n)
        #super().__imul__(n)

    def __iter__(this) -> Iterator[T]:
        return this._callDelegateFun()


def listOf(*args) -> List[T]:
    """
    Fungsi instansiasi `OperableList` yg isinya adalah `varargs`.
    :param args: kumpulan elemen yg mengisi `OperableList`.
    :return: `OperableList`
    """

    #prind(f"args.__class__={args.__class__} list(args).__class__={list(args).__class__}")
    return List(list(args))
