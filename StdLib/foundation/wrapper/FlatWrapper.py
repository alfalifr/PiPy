from typing import Type, Optional

from foundation.wrapper.Wrapper import Wrapper
from log.logs import prinw, prind
from reflex import Reflex
from reflex.BoundedFun import BoundedFun
from reflex.Property import Property
from reflex.Reflex import copyMember
from val.generic import T


class FlatWrapper(Wrapper[T]):
    """
    Kelas dasar Wrapper pada library ini yg memiliki sifat "flat", yaitu men-copy semua member (properti dan fungsi)
    pada [_content].
    """

    def __setContent(this, content: Optional[T]):
        #print(f"FlatWrapper.__setContent() content={content} content.__class__={content.__class__}")

        transformFun = lambda member: BoundedFun(content, member) \
            if Reflex.isFunction(content) and not Reflex.isConstructor(content) else member

        if isinstance(content, FlatWrapper):
            content = content.__content__  # setattr(this, "__content__", content)
        elif isinstance(content, Wrapper):
            content = content.content  # setattr(this, "__content__", content)
        if content:
            try: copyMember(content, this, transformFun=transformFun)
            except: prinw(f"Tidak dapat men-copy semua atribut dari {content} ke kelas {this}")

        this.__content__ = content

    def __getContent(this) -> Optional[T]:
        if hasattr(this, "__content__"):
            return this.__content__
        return None

    # TODO tambah descriptor untuk attrib `content`
    content = Property(
        None,
        lambda obj, field: obj.__getContent(),  # prind(f"FlatWrapper.content().obj={obj} field={field} obj.__getContent={obj.__getContent}"),  #
        lambda obj, field, value: obj.__setContent(value)
    )

    def __init__(this, content: T):
        super().__init__(content)
        this.content = content
        prind(f"hasattr(this.__getContent, '__call__') = {hasattr(this.__getContent, '__call__')} this.__getContent={this.__getContent}")
        #try: copyMember(content, this)
        #except: prind(f"Tidak dapat men-copy semua atribut dari {content} ke kelas {this}")
        #if not hasattr(this, "content"):
            #this.content = content

        #this.content = content  # seharusnya tidak di-assign lagi karena `this` merupakan FlatWrapper sehingga tidak perlu menampung ke dalam property `content`.
        # Selain itu, jika [content] jika memiliki property yang bernama `content`, maka nilai itu tidak akan hilang.

    def __repr__(this) -> str:
        return repr(this.__getContent())
        #try: return content.__repr__()  # super(Wrapper, this).content.__str__()
        #except: return content.__repr__(content)

    @classmethod
    def __ori_class__(cls):
        #old = this.__class__
        #this.__ori_class__ = old
        return cls

    #"""
    @property
    def __class__(this: T) -> Type[T]:
        content = this.__getContent()
        #prind(f"FlatWrapper.__class__ content={content} this.content={this.content} __ori_class__={this.__ori_class__()}")
        return content.__class__ if content else this.__ori_class__()  # super().__class__()
    #"""
