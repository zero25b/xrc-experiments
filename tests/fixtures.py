
# Note that the following values of blocks 154998 and 15499 were extracted directly from a break-point while running
# Electrum. They can be used to test the read_headers() function when calling Electrum routines.

ELECTRUM_154998 = {'version': 536870912, 'previousBlockHash': 'a872f8d169e7f48d04f31f174024501d0ec2898ea16e07ae2091b2526be8aa1c',
 'merkleroot': 'a6c992b4c9356687987c8fa296988ee5775cc2fd6efa2f1f437157d5b553c30e', 'blockTime': 1664212587,
 'bits': 453165802, 'nonce': 3081508237, 'blockIndex': 154998}

ELECTRUM_154999 = {'version': 536870912, 'previousBlockHash': '536fd637e87dfa548857b81c46f9078344949f2b8d858b305a5c1f6b4ce06640',
 'merkleroot': '4f72d77f443edb77eadf67ad3cbdad4d0115a31f481968af04772629ee570b73', 'blockTime': 1664212597,
 'bits': 453151324, 'nonce': 3374795661, 'blockIndex': 154999}

# The following data was downloaded directly from the blockCore API. It can be used to test routines that
# handle blockCore data.

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
