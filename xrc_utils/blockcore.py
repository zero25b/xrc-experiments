import pandas as pd
import requests
from typing import List, Dict


def get_blockcore_df(nmb_blocks=1000, offset=160000) -> pd.DataFrame:
    """
    Query Blockcore to get XRC blockchain data
    Args:
        nmb_blocks: number of blocks to return
        offset: index of starting block

    Returns: list of blockchain headers in json format

    """
    headers = {"accept": "*/*"}

    data = []

    # Query BlockCore for header-data in chunks of 50
    for k in range(nmb_blocks // 50 + 1):
        params = {"offset": str(offset + k * 50), "limit": "50"}
        response = requests.get(
            "https://xrc.indexer.blockcore.net/api/query/block",
            params=params,
            headers=headers,
        )
        data.extend(response.json())

    # Check that the data is in the correct order
    for idx in range(1, len(data)):
        assert (
            data[idx]["previousBlockHash"] == data[idx - 1]["blockHash"]
        ), "Block hashes out of order"
        assert (
            data[idx]["blockIndex"] == data[idx - 1]["blockIndex"] + 1
        ), "Indexes out of order"

    df = pd.DataFrame(data)

    # Reorder columns for convenience
    df = df[
        [
            "blockIndex",
            "blockHash",
            "blockTime",
            "merkleroot",
            "previousBlockHash",
            "bits",
            "nonce",
            "version",
            "nextBlockHash",
            "blockSize",
            "syncComplete",
            "transactionCount",
            "confirmations",
            "difficulty",
            "chainWork",
        ]
    ]

    return df


def get_blockcore_data(nmb_blocks=1000, offset=160000) -> List[Dict]:
    """
    Query Blockcore to get XRC blockchain data
    Args:
        nmb_blocks: number of blocks to return
        offset: index of starting block

    Returns: list of blockchain headers in json format

    """
    headers = {"accept": "*/*"}

    data = list([])

    # Query BlockCore for header-data in chunks of 50
    for k in range(nmb_blocks // 50 + 1):
        params = {"offset": str(offset + k * 50), "limit": "50"}
        response = requests.get(
            "https://xrc.indexer.blockcore.net/api/query/block",
            params=params,
            headers=headers,
        )
        data.extend(response.json())

    # Check that the data is in the correct order
    for idx in range(1, len(data)):
        assert (
            data[idx]["previousBlockHash"] == data[idx - 1]["blockHash"]
        ), "Block hashes out of order"
        assert (
            data[idx]["blockIndex"] == data[idx - 1]["blockIndex"] + 1
        ), "Indexes out of order"

    return data
