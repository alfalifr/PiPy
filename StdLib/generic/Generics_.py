from typing import TypeVar

T_out = TypeVar("T_out", covariant = True)
T_in = TypeVar("T_in", contravariant = True)
T = TypeVar("T")
K = TypeVar("K")  # Key typeParam
V = TypeVar("V")  # Value typeParam

# End of line