from typing import Generic

from reflex.Reflex import memoryAddress
from val.generic import T, R


class Field(Generic[T, R]):
    def __init__(this, initValue: R):
        this._value = initValue

    def set(this, value: R):
        this._value = value

    def get(this) -> R:
        return this._value

    def __repr__(this) -> str:
        address = memoryAddress(this)
        return f"<Field value={this._value} at {address}>"
