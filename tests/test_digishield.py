from tests.fixtures import ELECTRUM_154999, ELECTRUM_154998
from xrc_utils.digishield import (
    read_header,
    target_to_bits,
    get_targetDigishield,
    bits_to_target,
)
from xrc_utils.electrum import dump_blockchain_headers_file_to_df


def test_read_header():
    # Get raw data directly from the Electrum blockchain_headers file
    df = dump_blockchain_headers_file_to_df(
        read_header.DATA_PATH, bits_format="electrum"
    )

    for h in [149585, 154990, 151877]:
        header = read_header(h)
        for key in header:
            assert (
                header[key] == df.loc[h].to_dict()[key]
            ), f"Mismatch between read_header and parsed df at height = {h}"


def test_read_header_against_extracted_data():
    # Compare the decoding against data extracted from the Electrum wallet internals using a breakpoint...
    block_154999 = read_header(154999)
    for key in ELECTRUM_154999:
        assert ELECTRUM_154999[key] == block_154999[key]

    block_154998 = read_header(154998)
    for key in ELECTRUM_154998:
        assert ELECTRUM_154998[key] == block_154998[key]


def test_get_targetDigishield():
    # Make sure that get_targetDigishield returns the expected value for the next target, which is stored in the
    # blockchain data.
    for h in [154999, 151515, 152737]:
        assert target_to_bits(get_targetDigishield(h)) == read_header(h)["bits"]

        assert get_targetDigishield(h) == bits_to_target(read_header(h)["bits"])
