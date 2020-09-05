from typing import TypeVar

T_out = TypeVar("T_out", covariant = True)
T_in = TypeVar("T_in", contravariant = True)
In = TypeVar("In", covariant = True)  # Untuk menunjukan generic pada input
Out = TypeVar("Out", contravariant = True)  # Untuk menunjukan generic pada output
T = TypeVar("T")
K = TypeVar("K")  # Key typeParam
V = TypeVar("V")  # Value typeParam

# End of line