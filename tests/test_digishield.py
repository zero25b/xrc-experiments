from tests.fixtures import ELECTRUM_154999, ELECTRUM_154998
from xrc_utils import digishield
from xrc_utils.digishield import (
    get_targetDigishield,
)
from xrc_utils.electrum import dump_blockchain_headers_file_to_df
from xrc_utils.headers import BLOCKCHAIN_HEADERS_PATH, bits_to_target, target_to_bits


def test_digishield_read_header():
    # Get raw data directly from the Electrum blockchain_headers file
    df = dump_blockchain_headers_file_to_df(
        BLOCKCHAIN_HEADERS_PATH, bits_format="electrum"
    )

    for h in [149585, 154990, 151877]:
        header = digishield.read_header(h)
        for key in header:
            assert (
                header[key] == df.loc[h].to_dict()[key]
            ), f"Mismatch between digishield.read_header and parsed df at height = {h}"


def test_digishield_against_extracted_data():
    # Compare the decoding against data extracted from the Electrum wallet internals using a breakpoint...
    block_154999 = digishield.read_header(154999)
    for key in ELECTRUM_154999:
        assert ELECTRUM_154999[key] == block_154999[key]

    block_154998 = digishield.read_header(154998)
    for key in ELECTRUM_154998:
        assert ELECTRUM_154998[key] == block_154998[key]


def test_get_targetDigishield():
    # Make sure that get_targetDigishield returns the expected value for the next target, which is stored in the
    # blockchain data.
    for h in [154999, 151515, 152737]:
        assert (
            target_to_bits(get_targetDigishield(h)) == digishield.read_header(h)["bits"]
        )

        assert get_targetDigishield(h) == bits_to_target(
            digishield.read_header(h)["bits"]
        )
