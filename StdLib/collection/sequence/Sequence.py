from abc import ABC, abstractmethod
from typing import Generic, Iterable

from collection.iterator.Iterator import iteratorOf, Iterator
from collection.iterator.SkippingIterator import skippingIteratorOf
from val.generic import T_out


class Sequence(Generic[T_out], ABC, Iterable[T_out]):
    """
    Kelas dasar untuk semua sequence pada library ini.
    """

    @abstractmethod
    def __iter__(this) -> Iterator[T_out]: pass

    """
    Kelas yg berisi sekumpulan data yg mirip dg Sequence yg memiliki operasi scr lazy.
    """

    _itrIndex = 0
    _transformingFun: (lambda it: object) = None
    """
    Lambda yg mengubah isi data dari `this.content` menjadi data lain.
    Lambda ini digunakan pada fungsi [map] agar fungsi tersebut tidak langsung menjalankan semua isi
    dari `this.content` dg for.
    """

    def __new__(cls, content: T_out, transformingFun: (lambda it: object) = None) -> any:
        return super().__new__(cls, content)

    def __init__(this, content: Iterable[T_out], transformingFun: (lambda it: object) = None):
        super().__init__(content)
        this.content = content
        this._transformingFun = transformingFun
        # print(f"OprSeq init(): content= {this.content}")

    def filter(this, op: (lambda it: bool)):
        itr_ = skippingIteratorOf(src=this.__iter__(), skipFun=op, reverseFunResult=True)
        return Sequence(itr_, this._transformingFun)

    def map(this, op: (lambda it: object)):
        """
        Fungsi yg digunakan untuk mengubah isi dari `this.content` menjadi newSequence dg tipe data apapun itu
        hasilnya yg di hasilkan oleh :param op.
        Operasi dalam :param op dilakukan scr lazy.

        :param op: lambda untuk operasi `map` dg param
          -`it` adalah isi dari `this.content` pada setiap iterasinya.

        :return: newSequence dg isi sesuai hasil :param op.
        """
        def transform(it):
            res = op(it)
            # print(f"seq map() it= {it} res= {res}")
            return res

        new = OperableSequence(this.content, transform)
        return new

    def reduce(this, op: (lambda accumulation, it: object)):
        """
        Fungsi yg digunakan untuk mengubah isi dari `this.content` menjadi sebuah `accumulation`
        yg betipe data sama dg isi dari `this.content`.

        :param op: lambda untuk operasi `reduce` dg param
          -`accumulation` adalah akumulasi hasil perubahan isi dari `this.content` yg bertipe data sama pula.
          -`it` adalah isi dari `this.content` pada setiap iterasinya.

        :return: object `accumulation` hasil reduce yg bertipe data sama dg isi dari `this.content`.
        """
        this.breakItr = False
        acc = {"val" : this.first}

        def opForMap(it):
            acc["val"] = op(acc["val"], it)
            return acc["val"]
        this.forEach(opForMap, 1)
        return acc["val"]
    """
    Dikomen karena mengakibatkan circular import.
    def toList(this) -> OperableList[T]:
        " ""
        Mengubah kelas ini menjadi sequence.
        :return:
        " ""
        return OperableList([e for e in this.content])
    """

    def __iter__(this) -> Iterator[T_out]:
        #print(f"seq iter() this._transformingFun is not None = {this._transformingFun is not None}")
        if this._transformingFun is not None:
            itr = []
            this.forEach(lambda it: itr.append(this._transformingFun(it)))
            return iteratorOf(*itr)
        else:
            #print(f"seq iter() : masuk catch")
            return super().__iter__()

    def __str__(this) -> str:
        str_ = "("
        for e in this:
            #print(f"seq str() for str_= {str_} e= {e}")
            str_ += e.__str__() +", "
        try: str_ = str_.removesuffix(", ")
        except:
            try: str_ = str_.rstrip(", ")
            except: pass
        str_ += ")"
        return str_


class SequenceImpl(Sequence[T_out]):
    def __new__(cls, content: Iterable[T_out]):
        if not isinstance(content, Iterable):
            raise TypeError("""content: %s harus Iterable.""" % content)
        inst = super().__new__(cls)
        inst.content = content
        return inst

    def __iter__(this) -> Iterator[T_out]:
        return iteratorOf(*this.content)


def simpleSequenceOf(*vararg) -> Sequence[T_out]:
    return SequenceImpl(vararg)
