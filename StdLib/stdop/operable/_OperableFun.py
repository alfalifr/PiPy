from exception.NoSuchElementExc import NoSuchElementExc
from collection.OperableList import OperableList
from collection.OperableSequence import OperableSequence


def toSequence(obj):
    """
    Fungsi yg mengubah `obj` jadi `OperableSequence`.
    :param obj: object tipe Iterable.
    :return: `OperableSequence`
    """

    """
    if not isinstance(obj, Iterable):
        raise TypeError("toSequence(): obj harus Iterable.")
    """
    try: return OperableSequence([e for e in obj])
    except: raise NoSuchElementExc("toSequence(): obj harus Iterable.")


def toList(obj):
    """
    Fungsi yg mengubah `obj` jadi `OperableList`.
    :param obj: object tipe Iterable.
    :return: `OperableList`
    """
    try: return OperableList([e for e in obj])
    except: raise NoSuchElementExc("toList(): obj harus Iterable.")
