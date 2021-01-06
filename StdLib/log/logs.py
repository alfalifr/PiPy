from text.text import contentStr
from val import unicode


def prin(
    *msg, color: str = unicode.ANSI_RESET, sep: str = ", ", prefix: str = "", suffix: str = ""
):
    res = contentStr(msg, sep, prefix, suffix)
    print(color + res + unicode.ANSI_RESET)


def prine(*msg, sep: str = ", ", prefix: str = "", suffix: str = ""):
    prin(*msg, color=unicode.ANSI_RED, sep=sep, prefix=prefix, suffix=suffix)


def prinw(*msg, sep: str = ", ", prefix: str = "", suffix: str = ""):
    prin(*msg, color=unicode.ANSI_YELLOW, sep=sep, prefix=prefix, suffix=suffix)


def prind(*msg, sep: str = ", ", prefix: str = "", suffix: str = ""):
    prin(*msg, color=unicode.ANSI_BLUE, sep=sep, prefix=prefix, suffix=suffix)


def prinr(*msg, sep: str = ", ", prefix: str = "", suffix: str = ""):
    prin(*msg, color=unicode.ANSI_GREEN, sep=sep, prefix=prefix, suffix=suffix)
