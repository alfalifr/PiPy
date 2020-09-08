from exception.IllegalArgumentExc import IllegalArgumentExc
from meta import Meta
from meta.metameta.MetaMetaInspectable import MetaMetaInspectable


class Target(MetaMetaInspectable):
    CLASS = 1
    FUNCTION = 2
    META = 3
    _DEFAULT = FUNCTION

    def __init__(this, *targets: int):
        if len(targets) == 0 or (len(targets) == 1 and not isinstance(targets[0], int)):
            raise IllegalArgumentExc(f"""Argumen untuk anotasi @Target harus int setidaknya berjumlah 1.""")
        super().__init__(None, **{Meta.META_KWARGS_NAME: list(targets)})

