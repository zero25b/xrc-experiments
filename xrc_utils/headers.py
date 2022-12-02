from xrc_utils import DATA_DIR

HEADER_SIZE = 80

BITS_FORMATS = ["blockcore", "electrum"]

BLOCKCHAIN_HEADERS_PATH = DATA_DIR.joinpath("blockchain_headers")


def bh2u(x: bytes) -> str:
    return x.hex()


bfh = bytes.fromhex


def rev_hex(s: str) -> str:
    return bh2u(bfh(s)[::-1])


def int_to_hex(i: int, length: int = 1) -> str:
    """Converts int to little-endian hex string.
    `length` is the number of bytes available
    """
    if not isinstance(i, int):
        raise TypeError("{} instead of int".format(i))
    range_size = pow(256, length)
    if i < -(range_size // 2) or i >= range_size:
        raise OverflowError("cannot convert int {} to hex ({} bytes)".format(i, length))
    if i < 0:
        # two's complement
        i = range_size + i
    s = hex(i)[2:].rstrip("L")
    s = "0" * (2 * length - len(s)) + s
    return rev_hex(s)


def serialize_header(header_dict: dict) -> str:
    s = (
        int_to_hex(header_dict["version"], 4)
        + rev_hex(header_dict["previousBlockHash"])
        + rev_hex(header_dict["merkleroot"])
        + int_to_hex(int(header_dict["blockTime"]), 4)
        + int_to_hex(int("0x" + header_dict["bits"], 0), 4)
        + int_to_hex(int(header_dict["nonce"]), 4)
    )
    return s


def hash_encode(x: bytes) -> str:
    return bh2u(x[::-1])


def hex_to_int(s):
    return int.from_bytes(s, byteorder="little")


def deserialize_header(s: bytes, height: int, bits_format="blockcore") -> dict:
    assert (
        bits_format in BITS_FORMATS
    ), "Please select bits_format in ['blockcore', 'electrum']"

    h = {}
    h["version"] = hex_to_int(bytes(s[0:4]))
    h["previousBlockHash"] = hash_encode(s[4:36])
    h["merkleroot"] = hash_encode(s[36:68])
    h["blockTime"] = hex_to_int(s[68:72])
    bits = hex_to_int(s[72:76])
    if bits_format == "blockcore":
        bits = format(bits, "x")
    h["bits"] = bits
    h["nonce"] = hex_to_int(s[76:80])
    h["blockIndex"] = height
    return h


def bits_to_target(bits: int) -> int:
    bitsN = (bits >> 24) & 0xFF
    # if not (0x03 <= bitsN <= 0x1d):
    #    raise Exception("First part of bits should be in [0x03, 0x1d]")
    bitsBase = bits & 0xFFFFFF
    # if not (0x8000 <= bitsBase <= 0x7fffff):
    #    raise Exception("Second part of bits should be in [0x8000, 0x7fffff]")
    return bitsBase << (8 * (bitsN - 3))


def target_to_bits(target: int) -> int:
    c = ("%064x" % target)[2:]
    while c[:2] == "00" and len(c) > 6:
        c = c[2:]
    bitsN, bitsBase = len(c) // 2, int.from_bytes(bfh(c[:6]), byteorder="big")
    if bitsBase >= 0x800000:
        bitsN += 1
        bitsBase >>= 8
    return bitsN << 24 | bitsBase
