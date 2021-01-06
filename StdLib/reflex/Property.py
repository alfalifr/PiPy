from typing import Callable, Generic

from exception.IllegalAccessExc import IllegalAccessExc
from log.logs import prinw
from reflex.BoundedFun import BoundedFun
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

    def __call__(this, initValue: R):
        """
        Berguna saat kelasi ini dijadikan sebagai anotasi.
        :param initValue:
        :return:
        """
        this._accessor.set(initValue)

"""
class Setter(Property[T, R]):
    def __init__(
        this,
        setter: Callable[[T, Field[T, R], R], None],
        initValue: R = None,
    ):
        super().__init__(initValue, setter=setter)


class Getter(Property[T, R]):
    def __init__(
        this,
        getter: Callable[[T, Field[T, R]], R],
        initValue: R = None,
    ):
        super().__init__(initValue, getter=getter)
"""


class ImmutableProperty(Property[T, R]):
    def __init__(
        this,
        initValue: R = None,
        initGetter: Callable[[T, Field[T, R]], R] = None,
    ):
        this._isInited = False

        def _initGetter(obj, field) -> R:
            res = field.get() if this._isInited or not initGetter else initGetter(obj, field)
            if not this._isInited:
                field.set(res)
            this._isInited = True
            return res

        super().__init__(
            initValue,
            _initGetter,
            lambda owner, field, value: prinw(f"Property `{this.propName}` tidak dapat di-overwrite"),
        )


class BoundedImmutableProperty(ImmutableProperty[T, R]):
    def __init__(
        this,
        initValue: R = None,
    ):
        super().__init__(initValue, lambda owner, field: BoundedFun(owner, field.get()))
