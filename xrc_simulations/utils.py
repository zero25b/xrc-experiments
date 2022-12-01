from typing import List, Dict


def convert_list_to_blockchain(raw_data: List[Dict]):
    """
    Return blockchain data in a dictionary, with the blockIndex as the key
    """
    blockchain = {}

    for data in raw_data:
        idx = data["blockIndex"]
        blockchain[idx] = data

    return blockchain
