from tests.fixtures import BLOCKCORE_SAMPLE
from xrc_utils.utils import bfh, serialize_header, deserialize_header


def test_serialization():
    for header in BLOCKCORE_SAMPLE:
        serialized_header = serialize_header(header)
        deserialized_header = deserialize_header(bfh(serialized_header), header['blockIndex'])
        for key in deserialized_header:
            assert header[key] == deserialized_header[key], f"Deserialization failed at {key}"
