from typing import Callable

from reflex.Reflex import memoryAddress


class BoundedFun(Callable):
    def __init__(this, owner, callable: Callable) -> None:
        super().__init__()
        this._callable = callable
        this._owner = owner

    def __call__(this, *args, **kwargs):
        print(f"BoundedFun this._callable={this._callable}")
        return this._callable(this._owner, *args, **kwargs)

    def __repr__(this) -> str:
        address = memoryAddress(this._owner)
        return f"<BoundedFun '{this._callable.__name__}' of object {this._owner.__class__.__name__} at {address}>"


def boundedFun(owner, callable: Callable) -> BoundedFun:
    return BoundedFun(owner, callable)