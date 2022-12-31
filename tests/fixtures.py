from xrc_simulations.simulations import PowSimulator


# Blocks 154998 and 15499 were extracted directly from a break-point while running the Electrum wallet.
ELECTRUM_154998 = {
    "version": 536870912,
    "previousBlockHash": "a872f8d169e7f48d04f31f174024501d0ec2898ea16e07ae2091b2526be8aa1c",
    "merkleroot": "a6c992b4c9356687987c8fa296988ee5775cc2fd6efa2f1f437157d5b553c30e",
    "blockTime": 1664212587,
    "bits": 453165802,
    "nonce": 3081508237,
    "blockIndex": 154998,
}

ELECTRUM_154999 = {
    "version": 536870912,
    "previousBlockHash": "536fd637e87dfa548857b81c46f9078344949f2b8d858b305a5c1f6b4ce06640",
    "merkleroot": "4f72d77f443edb77eadf67ad3cbdad4d0115a31f481968af04772629ee570b73",
    "blockTime": 1664212597,
    "bits": 453151324,
    "nonce": 3374795661,
    "blockIndex": 154999,
}

# BLOCKCORE_SAMPLE data was downloaded directly from the blockCore API.
BLOCKCORE_SAMPLE = [
    {
        "blockHash": "a71caca3f80bbedbaf588745244f8781e97fcea109fabbc63b52943dc468ab57",
        "blockIndex": 160998,
        "blockSize": 203,
        "blockTime": 1667707581,
        "nextBlockHash": "584d643e54b75d833b6b37fdd55b0c57063f644113229ade3a95348c07dca4bb",
        "previousBlockHash": "94804512f8aaec765336a1c3379a4c37dee3109fc0e5365de0eff5e60cd2bb71",
        "syncComplete": True,
        "transactionCount": 1,
        "confirmations": 3,
        "bits": "1b0ddcf8",
        "difficulty": 4727.277466165347,
        "chainWork": "00000000000000000000000000000000000000000000000efac9ce662205c865",
        "merkleroot": "fb719372c152aa629ccf0ca909be983fe099076c459550ddb87d1891ab305dd5",
        "nonce": 2037483597,
        "version": 536870912,
    },
    {
        "blockHash": "584d643e54b75d833b6b37fdd55b0c57063f644113229ade3a95348c07dca4bb",
        "blockIndex": 160999,
        "blockSize": 203,
        "blockTime": 1667707582,
        "nextBlockHash": "a1b8070fcf1699598efd4c607d95f679ad943e8b465240b10a6390d3bf32d3e6",
        "previousBlockHash": "a71caca3f80bbedbaf588745244f8781e97fcea109fabbc63b52943dc468ab57",
        "syncComplete": True,
        "transactionCount": 1,
        "confirmations": 2,
        "bits": "1b1014cd",
        "difficulty": 4075.242133748805,
        "chainWork": "00000000000000000000000000000000000000000000000efac9de516fed9081",
        "merkleroot": "e8bdbeaee58692de18747d8762e9ac5fbef6489a8e3b2ea4951ee481d11eaf04",
        "nonce": 209584543,
        "version": 536870912,
    },
]

# Extracted from unit tests in https://github.com/dashevo/dark-gravity-wave-js
DASH_MAINNET_BLOCKS = [
  {
    "blockIndex": 999900,
    "blockTime": 1546794811,
    "target": 0x1937efd3,
  },
  {
    "blockIndex": 999901,
    "blockTime": 1546794872,
    "target": 0x193bdb17,
  },
  {
    "blockIndex": 999902,
    "blockTime": 1546795363,
    "target": 0x193c2e06,
  },
  {
    "blockIndex": 999903,
    "blockTime": 1546795705,
    "target": 0x19436374,
  },
  {
    "blockIndex": 999904,
    "blockTime": 1546795801,
    "target": 0x1942c8da,
  },
  {
    "blockIndex": 999905,
    "blockTime": 1546796153,
    "target": 0x1942a824,
  },
  {
    "blockIndex": 999906,
    "blockTime": 1546796323,
    "target": 0x19466999,
  },
  {
    "blockIndex": 999907,
    "blockTime": 1546796325,
    "target": 0x194815a5,
  },
  {
    "blockIndex": 999908,
    "blockTime": 1546796396,
    "target": 0x19481272,
  },
  {
    "blockIndex": 999909,
    "blockTime": 1546796425,
    "target": 0x1948b446,
  },
  {
    "blockIndex": 999910,
    "blockTime": 1546796594,
    "target": 0x194767ac,
  },
  {
    "blockIndex": 999911,
    "blockTime": 1546797416,
    "target": 0x194798d6,
  },
  {
    "blockIndex": 999912,
    "blockTime": 1546797529,
    "target": 0x19560a56,
  },
  {
    "blockIndex": 999913,
    "blockTime": 1546797597,
    "target": 0x19592a34,
  },
  {
    "blockIndex": 999914,
    "blockTime": 1546797677,
    "target": 0x195bb28f,
  },
  {
    "blockIndex": 999915,
    "blockTime": 1546797788,
    "target": 0x195c638e,
  },
  {
    "blockIndex": 999916,
    "blockTime": 1546798067,
    "target": 0x195a9134,
  },
  {
    "blockIndex": 999917,
    "blockTime": 1546798096,
    "target": 0x195a40bd,
  },
  {
    "blockIndex": 999918,
    "blockTime": 1546798145,
    "target": 0x19532245,
  },
  {
    "blockIndex": 999919,
    "blockTime": 1546798220,
    "target": 0x194eadda,
  },
  {
    "blockIndex": 999920,
    "blockTime": 1546798311,
    "target": 0x1950aaf2,
  },
  {
    "blockIndex": 999921,
    "blockTime": 1546798458,
    "target": 0x195298e1,
  },
  {
    "blockIndex": 999922,
    "blockTime": 1546798565,
    "target": 0x1955383b,
  },
  {
    "blockIndex": 999923,
    "blockTime": 1546798603,
    "target": 0x195587da,
  },
  {
    "blockIndex": 999924,
    "blockTime": 1546798801,
    "target": 0x19514193,
  },
]


class FixtureSimulator(PowSimulator):
    def __init__(self, network, miners, time_deltas):
        self._time_deltas = time_deltas
        super().__init__(network, miners)

    def get_block_time(self, target, hashrate):
        """
        Override get_block_time routine, to return known block-times for tests
        """
        assert len(self._time_deltas) > 0, "No block-times available"
        time = self._time_deltas[0]
        self._time_deltas = self._time_deltas[1:]
        return time
