from ctypes import cdll, create_string_buffer
from xrc_utils import X13_DIR
import os

try:
    LIB_X13 = cdll.LoadLibrary(X13_DIR.joinpath(os.name + "/libx13.so").as_posix())
except Exception as e:
    raise RuntimeError(
        "libx13 did not load. It is either not installed or it could not load. Message: "
        + str(e)
    )


def get_pow_hash_x13(value):
    result = create_string_buffer(32)
    LIB_X13.x13_hash(value, len(value), result)
    return result
