
class IllegalArgumentExc(Exception):
    def __init__(this, *args: object) -> None:
        super().__init__(*args)
