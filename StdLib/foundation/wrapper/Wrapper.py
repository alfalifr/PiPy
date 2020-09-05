from typing import Generic, Union, Tuple, Any

from generic.Generics_ import T


class Wrapper(Generic[T]):
    """
    Kelas dasar semua wrapper pada library ini.
    """

    def __init__(this, content: T) -> None:
        """
        Subclass haru memanggil fungsi ini (super().__init__()) agar kinerja kelas ini optimal.
        :param content:
        """
        this.content = content

    def __eq__(this, o: object) -> bool:
        try: return this.content.__eq__(o)
        except: return super().__eq__(o)

    def __ne__(this, o: object) -> bool:
        try: return this.content.__ne__(o)
        except: return super().__ne__(o)

    def __sizeof__(this) -> int:
        try: return this.content.__sizeof__()
        except: return super().__sizeof__()

    def __str__(this) -> str:
        try: return this.content.__str__()  # super(Wrapper, this).content.__str__()
        except: return super().__str__()

    def __reduce__(this) -> Union[str, Tuple[Any, ...]]:
        try: return this.content.__reduce__()
        except: return super().__reduce__()

    def __reduce_ex__(this, protocol: int) -> Union[str, Tuple[Any, ...]]:
        try: return this.content.__reduce_ex__(protocol)
        except: return super().__reduce_ex__(protocol)














