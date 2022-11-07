from xrc_experiments.utils import bfh, serialize_header, deserialize_header


BLOCKCORE_SAMPLE = [{'blockHash': 'a71caca3f80bbedbaf588745244f8781e97fcea109fabbc63b52943dc468ab57',
  'blockIndex': 160998,
  'blockSize': 203,
  'blockTime': 1667707581,
  'nextBlockHash': '584d643e54b75d833b6b37fdd55b0c57063f644113229ade3a95348c07dca4bb',
  'previousBlockHash': '94804512f8aaec765336a1c3379a4c37dee3109fc0e5365de0eff5e60cd2bb71',
  'syncComplete': True,
  'transactionCount': 1,
  'confirmations': 3,
  'bits': '1b0ddcf8',
  'difficulty': 4727.277466165347,
  'chainWork': '00000000000000000000000000000000000000000000000efac9ce662205c865',
  'merkleroot': 'fb719372c152aa629ccf0ca909be983fe099076c459550ddb87d1891ab305dd5',
  'nonce': 2037483597,
  'version': 536870912},
 {'blockHash': '584d643e54b75d833b6b37fdd55b0c57063f644113229ade3a95348c07dca4bb',
  'blockIndex': 160999,
  'blockSize': 203,
  'blockTime': 1667707582,
  'nextBlockHash': 'a1b8070fcf1699598efd4c607d95f679ad943e8b465240b10a6390d3bf32d3e6',
  'previousBlockHash': 'a71caca3f80bbedbaf588745244f8781e97fcea109fabbc63b52943dc468ab57',
  'syncComplete': True,
  'transactionCount': 1,
  'confirmations': 2,
  'bits': '1b1014cd',
  'difficulty': 4075.242133748805,
  'chainWork': '00000000000000000000000000000000000000000000000efac9de516fed9081',
  'merkleroot': 'e8bdbeaee58692de18747d8762e9ac5fbef6489a8e3b2ea4951ee481d11eaf04',
  'nonce': 209584543,
  'version': 536870912}]


def test_serialization():
    for header in BLOCKCORE_SAMPLE:

        serialized_header = serialize_header(header)

        deserialized_header = deserialize_header(bfh(serialized_header), header['blockIndex'])

        for key in deserialized_header:

            assert header[key] == deserialized_header[key], f"Deserialization failed at {key}"

