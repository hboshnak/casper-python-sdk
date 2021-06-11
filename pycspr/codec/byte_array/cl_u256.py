import typing

from pycspr.serialization.utils import int_to_le_bytes
from pycspr.codec.byte_array import cl_u32
from pycspr.codec.byte_array import cl_u64
from pycspr.codec.byte_array import cl_u128



# Length when encoded.
_ENCODED_LENGTH: int = 32

# Dimension constraints.
MIN_SIZE = 0
MAX_SIZE = (2 ** 256) - 1


def encode(v: int) -> typing.List[int]:
    """Maps a parsed value to a CL byte array representation.

    :param v: Value to be mapped.

    """
    if v < cl_u32.MAX_SIZE:
        return cl_u32.encode(v)
    elif v < cl_u64.MAX_SIZE:
        return cl_u64.encode(v)
    elif v < cl_u128.MAX_SIZE:
        return cl_u128.encode(v)
    else:
        return int_to_le_bytes(int(v), _ENCODED_LENGTH, False)
