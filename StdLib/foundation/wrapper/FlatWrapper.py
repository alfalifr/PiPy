from foundation.wrapper.Wrapper import Wrapper
from val.generic import T
from stdop._StdAttrFun import copyMember


class FlatWrapper(Wrapper[T]):
    """
    Kelas dasar Wrapper pada library ini yg memiliki sifat "flat", yaitu men-copy semua member (properti dan fungsi)
    pada [_content].
    """

    def __init__(this, content: T):
        super().__init__(content)
        try: copyMember(content, this)
        except: print(f"Tidak dapat men-copy semua atribut dari {content} ke kelas {this}")
        if "content" not in this.__dict__.keys():
            this.content = content
        #this.content = content  # seharusnya tidak di-assign lagi karena `this` merupakan FlatWrapper sehingga tidak perlu menampung ke dalam property `content`.
        # Selain itu, jika [content] jika memiliki property yang bernama `content`, maka nilai itu tidak akan hilang.
