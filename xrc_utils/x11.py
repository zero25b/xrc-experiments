from ctypes import *
from xrc_utils import X11_DIR

try:
    LIB_X11 = cdll.LoadLibrary(X11_DIR.joinpath('libx11.so').as_posix())
except Exception as e:
    raise RuntimeError('libx11 did not load. It is either not installed or it could not load. Message: ' + str(e))


def get_pow_hash_x11(value):
    result = create_string_buffer(32)
    LIB_X11.x11_hash(value, len(value), result)
    return result
