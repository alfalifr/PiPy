from foundation.wrapper.Wrapper import Wrapper
from generic.Generics_ import T
from stdop.StdAttrFun_ import copyMember


class FlatWrapper(Wrapper[T]):
    """
    Kelas dasar Wrapper pada library ini yg memiliki sifat "flat", yaitu men-copy semua member (properti dan fungsi)
    pada [_content].
    """

    def __init__(this, content: T):
        super().__init__(content)
        try: copyMember(content, this)
        except: print(f"Tidak dapat men-copy semua atribut dari {content} ke kelas {this}")
        this.content = content
