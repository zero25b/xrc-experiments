from xrc_simulations.simulations import MockMinerBase, NetworkConfig, THZ, GHZ


class SimpleMiner(MockMinerBase):
    def set_hash_rate(self, *args):
        """
        Hash-rate is set by the constructor. So pass.
        """
        pass


class AttackMiner(MockMinerBase):
    def __init__(self, blockchain: dict, hash_rate: int, on: bool = False):
        self._hp = hash_rate
        if on:
            self._hash_rate = hash_rate
        else:
            self._hash_rate = 0

        super().__init__(blockchain, hash_rate)

    def set_hash_rate(self, config: NetworkConfig, *args):
        if config.difficulty < 50000 * 2**12:
            if self._hash_rate == 0:
                self._hash_rate = self._hp
        elif config.difficulty > 750000 * 2**12:
            self._hash_rate = 0
