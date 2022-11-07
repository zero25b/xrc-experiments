import pandas as pd
import os

HEADER_SIZE = 80

DIGISHIELDX11_BLOCK_HEIGHT = 136135

def bh2u(x: bytes) -> str:
    return x.hex()


bfh = bytes.fromhex


def rev_hex(s: str) -> str:
    return bh2u(bfh(s)[::-1])


def int_to_hex(i: int, length: int=1) -> str:
    """Converts int to little-endian hex string.
    `length` is the number of bytes available
    """
    if not isinstance(i, int):
        raise TypeError('{} instead of int'.format(i))
    range_size = pow(256, length)
    if i < -(range_size//2) or i >= range_size:
        raise OverflowError('cannot convert int {} to hex ({} bytes)'.format(i, length))
    if i < 0:
        # two's complement
        i = range_size + i
    s = hex(i)[2:].rstrip('L')
    s = "0"*(2*length - len(s)) + s
    return rev_hex(s)


def serialize_header(header_dict: dict) -> str:
    s = int_to_hex(header_dict['version'], 4) \
        + rev_hex(header_dict['previousBlockHash']) \
        + rev_hex(header_dict['merkleroot']) \
        + int_to_hex(int(header_dict['blockTime']), 4) \
        + int_to_hex(int('0x' + header_dict['bits'], 0), 4) \
        + int_to_hex(int(header_dict['nonce']), 4)
    return s


def hash_encode(x: bytes) -> str:
    return bh2u(x[::-1])


def deserialize_header(s: bytes, height: int) -> dict:
    hex_to_int = lambda s: int.from_bytes(s, byteorder='little')
    h = {}
    h['version'] = hex_to_int(bytes(s[0:4]))
    h['previousBlockHash'] = hash_encode(s[4:36])
    h['merkleroot'] = hash_encode(s[36:68])
    h['blockTime'] = hex_to_int(s[68:72])
    h['bits'] = format(hex_to_int(s[72:76]), 'x')
    h['nonce'] = hex_to_int(s[76:80])
    h['blockIndex'] = height
    return h


def dump_blockchain_headers_file_to_pandas(header_file):
    file_size = os.stat(header_file).st_size
    assert file_size % HEADER_SIZE == 0, "File size should be a multiple of HEADER_SIZE."

    nmb_rows = file_size // HEADER_SIZE
    with open(header_file, 'rb') as f:
        hexdata = f.read().hex()

    raw_data = []

    for h in range(nmb_rows):
        db = bytes.fromhex(hexdata[2 * HEADER_SIZE * h:2 * HEADER_SIZE * (h + 1)])
        raw_data.append(deserialize_header(db, h))

    df = pd.DataFrame(raw_data)

    # Reorder columns for convenience
    df = df[[ 'blockIndex', 'blockTime', 'merkleroot', 'previousBlockHash', 'bits', 'nonce', 'version']]

    return df
