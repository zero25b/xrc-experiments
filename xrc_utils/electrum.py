import os
import pandas as pd
from xrc_utils.utils import HEADER_SIZE, deserialize_header


def dump_blockchain_headers_file_to_df(header_file, bits_format="blockCore") -> pd.DataFrame:
    """
    Routine to dump an Electrum "blockchain_headers" file to a pandas dataframe.
    """
    assert bits_format in ['blockCore', 'electrum'], "Please select bits_format in ['blockCore', 'electrum']"

    file_size = os.stat(header_file).st_size

    assert file_size % HEADER_SIZE == 0, "File size should be a multiple of HEADER_SIZE."

    nmb_rows = file_size // HEADER_SIZE
    with open(header_file, 'rb') as f:
        hexdata = f.read().hex()

    raw_data = []

    for h in range(nmb_rows):
        db = bytes.fromhex(hexdata[2 * HEADER_SIZE * h:2 * HEADER_SIZE * (h + 1)])
        raw_data.append(deserialize_header(db, h, bits_format))

    df = pd.DataFrame(raw_data)

    # Reorder columns for convenience
    df = df[['blockIndex', 'blockTime', 'merkleroot', 'previousBlockHash', 'bits', 'nonce', 'version']]

    return df
