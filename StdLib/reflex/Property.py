from typing import Callable, Generic

from exception.IllegalAccessExc import IllegalAccessExc
from reflex.Field import Field
from val.generic import T, R


class Property(Generic[T, R]):
    def __init__(
        this,
        initValue: R,
        getter: Callable[[T, Field[T, R]], R] = lambda obj, field: field.get(),
        setter: Callable[[T, Field[T, R], R], None] = lambda obj, field, value: field.set(value)
    ) -> None:
        super().__init__()

        this._accessor = Field(initValue)

        def _getter(obj: T) -> R: return getter(obj, this._accessor)

        def _setter(obj: T, value: R):
            if setter: return setter(obj, this._accessor, value)
            else: raise IllegalAccessExc(f"Property `{this.propName}` tidak punya setter.")

        this._getter = _getter
        this._setter = _setter

    @property
    def propName(this):
        return this._propName[1:]

    @property
    def __name__(this) -> str:
        return this.propName

    def __set_name__(this, owner, name):
        this._propName = "_" + name
        pass

    def __set__(this, obj, value):
        this._setter(obj, value)

    def __get__(this, obj, objType: type = None):
        return this._getter(obj)
