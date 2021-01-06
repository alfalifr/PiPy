from typing import Any, List, Callable

from collection.iterator.SkippingIterator import skippingIteratorOf
from exception.NoSuchElementExc import NoSuchElementExc
from val.generic import T, T_out, R
from collection.OperableIterable import OperableIterable


class OperableList(OperableIterable[T], List[T]):
    """
    Kelas yg berisi sekumpulan data yg mirip dg List dg fungsi tambahan.
    """

    _itrIndex = 0

    def __new__(cls, content: T) -> Any:
        if not isinstance(content, List):
            raise TypeError(f"""content: {content} harus List.""")
        inst = super().__new__(cls, content)
        inst.content = content
        # print(f"OprList new(): content= {inst.content}")
        return inst

    def filter(this, op: Callable[[T_out], bool]) -> "OperableList[T]":
        # print(f"OprList filter() op= ${inspect.getsource(op)} *[e for e in this.content]= {[e for e in this.content]}")
        itr_ = skippingIteratorOf(*[e for e in this.content], skipFun = op, reverseFunResult = True)
        return OperableList([e for e in itr_])

    def map(this, op: Callable[[T], R]) -> "OperableList[R]":  #(lambda it: object)
        """
        Fungsi yg digunakan untuk mengubah isi dari `this.content` menjadi newList dg tipe data apapun itu
        hasilnya yg di hasilkan oleh :param op.

        :param op: lambda untuk operasi `map` dg param
          -`it` adalah isi dari `this.content` pada setiap iterasinya.

        :return: newList dg tipe OperableList dg isi sesuai hasil :param op.
        """
        # print(f"OprList map() op= {inspect.getsource(op)}")

        this.breakItr = False
        this._itrIndex = 0
        newList = []
        for e in this.content:
            if this.breakItr: break
            newList.append(op(e))
        newList = OperableList(newList)
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
        if this.isEmpty:
            return None

        acc = {"val" : this.first}

        def opForMap(it):
            acc["val"] = op(acc["val"], it)  # or this.content[this._itrIndex]
            return acc["val"]
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


    """
    Dikomen karena mengakibatkan circular import.
    def asSequence(this) -> OperableSequence[T]:
        " ""
        Mengubah kelas ini menjadi sequence.
        :return:
        " ""
        return OperableSequence(this.content)
    """


def listOf(*varargs) -> OperableList[T]:
    """
    Fungsi instansiasi `OperableList` yg isinya adalah `varargs`.
    :param varargs: kumpulan elemen yg mengisi `OperableList`.
    :return: `OperableList`
    """
    return OperableList(list(varargs))
