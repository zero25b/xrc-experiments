from xrc_utils import DATA_DIR
from xrc_utils.utils import serialize_header, bfh, hash_encode, HEADER_SIZE, \
    deserialize_header
from xrc_utils.x11 import get_pow_hash_x11

"""
Most of these routines were extracted verbatim from the Electrum wallet. Those routines, in turn 
reproduce many of the C# routines for difficulty calculations and blockchain handling in the xrhodiumnode repo. 
The only major modification here, is to mock the read_headers() function with a callable object, which reads from an
existing blockchain_headers file. 
"""

TESTNET = False
MAX_TARGET = 0x00000fffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
MAX_TARGET_2 = 0x00000fffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
TARGET_2_FROMBLOCK_HEIGHT = 0
DIGISHIELDX11_BLOCK_HEIGHT = 136135


class MissingHeader(Exception):
    pass


def hash_for_pow(header: dict) -> str:
    header_serialized = serialize_header(header)

    assert (header['blockIndex'] > DIGISHIELDX11_BLOCK_HEIGHT)

    return hash_encode(get_pow_hash_x11(bfh(header_serialized)))

def bits_to_target(bits: int) -> int:
    bitsN = (bits >> 24) & 0xff
    #if not (0x03 <= bitsN <= 0x1d):
    #    raise Exception("First part of bits should be in [0x03, 0x1d]")
    bitsBase = bits & 0xffffff
    #if not (0x8000 <= bitsBase <= 0x7fffff):
    #    raise Exception("Second part of bits should be in [0x8000, 0x7fffff]")
    return bitsBase << (8 * (bitsN-3))

def target_to_bits(target: int) -> int:
    c = ("%064x" % target)[2:]
    while c[:2] == '00' and len(c) > 6:
        c = c[2:]
    bitsN, bitsBase = len(c) // 2, int.from_bytes(bfh(c[:6]), byteorder='big')
    if bitsBase >= 0x800000:
        bitsN += 1
        bitsBase >>= 8
    return bitsN << 24 | bitsBase


def get_target(index: int, height: int) -> int:
    # compute target from chunk x, used in chunk x+
    if TESTNET:
        return 0
    if index == -1:
        return MAX_TARGET
    if index == TARGET_2_FROMBLOCK_HEIGHT:
        return MAX_TARGET_2

    # if (height <= DIGISHIELDX11_BLOCK_HEIGHT) and (index < len(checkpoints)):
    #     h, t = checkpoints[index]
    #     return t

    # new target - check digishield height
    if height > DIGISHIELDX11_BLOCK_HEIGHT:
        return get_targetDigishield(height)

    first = read_header(index * 2016)
    last = read_header(index * 2016 + 2015)
    if not first or not last:
        raise MissingHeader()
    bits = last.get('bits')
    target = bits_to_target(bits)

    nActualTimespan = last.get('timestamp') - first.get('timestamp')
    nTargetTimespan = 14 * 24 * 60 * 60
    nActualTimespan = max(nActualTimespan, nTargetTimespan // 4)
    nActualTimespan = min(nActualTimespan, nTargetTimespan * 4)
    new_target = min(MAX_TARGET, (target * nActualTimespan) // nTargetTimespan)

    # not any target can be represented in 32 bits:
    new_target = bits_to_target(target_to_bits(new_target))
    return new_target


def get_targetDigishield(height: int) -> int:

    nAveragingInterval = 10 * 5 # block
    multiAlgoTargetSpacingV4 = 10 * 60 # seconds
    nAveragingTargetTimespanV4 = nAveragingInterval * multiAlgoTargetSpacingV4
    nMaxAdjustDownV4 = 16
    nMaxAdjustUpV4 = 8
    nMinActualTimespanV4 = nAveragingTargetTimespanV4 * (100 - nMaxAdjustUpV4) / 100
    nMaxActualTimespanV4 = nAveragingTargetTimespanV4 * (100 + nMaxAdjustDownV4) / 100
    medianTimespan = 11

    if ((height - DIGISHIELDX11_BLOCK_HEIGHT) <= (nAveragingInterval + 11)):
        return int(0x000000000001a61a000000000000000000000000000000000000000000000000)

    last = read_header(height - 1)
    first = read_header(height - nAveragingInterval)
    if not first or not last:
        raise MissingHeader()

    # Limit adjustment step
    # Use medians to prevent time-warp attacks
    last_averagetimestamp = get_averageTimepast(last.get('blockIndex')) # Note that blockIndex in blockcore -> block_height in electrum
    first_averagetimestamp = get_averageTimepast(first.get('blockIndex'))
    nActualTimespan = last_averagetimestamp - first_averagetimestamp
    nActualTimespan = nAveragingTargetTimespanV4 + (nActualTimespan - nAveragingTargetTimespanV4) / 4

    if nActualTimespan < nMinActualTimespanV4:
        nActualTimespan = nMinActualTimespanV4
    if nActualTimespan > nMaxActualTimespanV4:
        nActualTimespan = nMaxActualTimespanV4

    bits = last.get('bits')
    target = bits_to_target(bits)
    new_target = target * int(nActualTimespan)
    new_target = new_target / nAveragingTargetTimespanV4
    new_targetBits = target_to_bits(int(new_target))
    bitsToTarget = bits_to_target(new_targetBits)
    bitsToTarget = min(MAX_TARGET, bitsToTarget)
    return bitsToTarget

def get_medianTimepast(height:int) -> int:
    medianTimespan = 11
    median = medianTimespan * [0]
    begin = medianTimespan
    end = medianTimespan

    for i in range(medianTimespan):
        chainedHeader = read_header(height - i)
        if chainedHeader is None:
            break
        else:
            begin = begin - 1
            median[i] = chainedHeader.get('blockTime') # Note that 'timestamp' in Electrum is 'blockTime' in Blockcore

    median.sort() # Note, could be a bug here in electrum...

    return median[int(begin + ((end - begin) / 2))]

def get_averageTimepast(height:int) -> int:
    medianTimespan = 11
    median = list()

    for i in range(medianTimespan):
        chainedHeader = read_header(height - i)
        if chainedHeader is None:
            break
        else:
            median.append(chainedHeader.get('blockTime'))

    median.sort()

    firstTimespan = median[0]
    lastTimespan = median[-1]
    differenceTimespan = lastTimespan - firstTimespan
    timespan = int(differenceTimespan / 2)
    averageDateTime = firstTimespan + timespan

    return averageDateTime

class ReadHeader:
    DATA_PATH = DATA_DIR.joinpath("blockchain_headers_corrupt")

    def __call__(self, height, bits_format='electrum'):
        assert height > DIGISHIELDX11_BLOCK_HEIGHT, "Please select a height after the X11-Digishield fork"

        delta = height
        with open(self.DATA_PATH, 'rb') as f:
            f.seek(delta * HEADER_SIZE)
            serialized_header = f.read(HEADER_SIZE)
            if len(serialized_header) < HEADER_SIZE:
                raise Exception('Expected to read a full header. This was only {} bytes'.format(len(serialized_header)))
        if serialized_header == bytes([0])*HEADER_SIZE:
            return None

        return deserialize_header(serialized_header, height, bits_format=bits_format)


read_header = ReadHeader()
