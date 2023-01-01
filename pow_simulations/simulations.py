from dataclasses import dataclass
from typing import List, Type, Dict
import numpy as np
from numpy.random import choice
from xrc_utils.blockcore import target_to_difficulty
from xrc_utils.headers import bits_to_target
from copy import copy

SEED = 1234

GHZ = 10**9
THZ = 10**12


@dataclass
class PowBlock:
    version: int
    previous_block_hash: str
    merkleroot: str
    block_time: int
    bits: int
    nonce: int
    block_index: int
    hash_rate: int = None

    def to_json(self) -> dict:
        output_dict = {
            "version": self.version,
            "previousBlockHash": self.previous_block_hash,
            "merkleroot": self.merkleroot,
            "blockTime": self.block_time,
            "bits": self.bits,
            "nonce": self.nonce,
            "blockIndex": self.block_index,
        }
        if self.hash_rate is not None:
            output_dict["hashRate"] = self.hash_rate
        return output_dict


@dataclass
class NetworkConfig:
    block_time: int
    block_index: int
    bits: int

    @property
    def difficulty(self) -> float:
        return target_to_difficulty(self.target)

    @property
    def target(self) -> int:
        return bits_to_target(self.bits)


class MockMinerBase:
    """
    Base class for miner-pow_simulations
    """

    def __init__(self, blockchain: dict, hash_rate: int):
        self.blockchain = copy(
            blockchain
        )  # Note: The blockchain should be a copy in each miner...
        self._hash_rate = hash_rate

    def set_hash_rate(self, *args):
        raise NotImplementedError

    @property
    def hash_rate(self):
        return self._hash_rate

    def create_block(self, config: NetworkConfig, time_delta: int, nonce: int):
        synthetic_hash = f"synthetic_{config.block_index}"  # TODO: This is a hack. Replace with the correct hash.
        next_block = PowBlock(
            version=0,
            previous_block_hash=synthetic_hash,
            merkleroot="synthetic",
            block_time=config.block_time + time_delta,
            bits=config.bits,
            nonce=nonce,
            block_index=config.block_index + 1,
            hash_rate=self.hash_rate,
        )
        return next_block

    def update(self, config: NetworkConfig, next_block: PowBlock):
        self.blockchain[next_block.block_index] = next_block.to_json()
        self.set_hash_rate(config)


class MockNetworkBase:
    """
    Base class to simulate various difficulty adjustments schemes such as DigiShield V0. Once the network difficulty is
    set, time-to-next block can be treated as a Gamma random variable that depends on the network-wide hash-rate and
    the difficulty. Inherit from this class and implement the get_target routine, which should contain the difficulty
    adjustment logic.
    """

    def __init__(self, blockchain: Dict, config: NetworkConfig):
        self.blockchain = copy(blockchain)  # The blockchain should be a copy
        self._config = config
        self.logging_list = []

    @property
    def difficulty(self):
        return self._config.difficulty

    @property
    def target(self):
        return self._config.target

    @property
    def config(self):
        return self._config

    def read_header(self, idx):
        header = self.blockchain.get(idx)
        assert (header is not None) & (
            header["blockIndex"] == idx
        ), f"Block index {idx} is not valid"
        return header

    def get_target(self, *args):
        raise NotImplementedError

    def update(self, next_block: PowBlock):
        # Add the next block to the internal blockchain
        self.blockchain[next_block.block_index] = next_block.to_json()

        # Calculate the next target in bits
        bits = self.get_target(next_block.block_index + 1)

        # Update the internal configuration based on the new block
        self._config = NetworkConfig(
            block_time=next_block.block_time,
            block_index=next_block.block_index,
            bits=bits,
        )

    def get_df(self):
        import pandas as pd

        return pd.DataFrame(self.blockchain).T


class PowSimulator(object):
    def __init__(
        self, network: Type[MockNetworkBase], miners: List[Type[MockMinerBase]]
    ):
        self.network = network
        self.miners = miners

    @property
    def hash_rate(self):
        return np.sum([copy(miner).hash_rate for miner in self.miners], axis=0)

    @staticmethod
    def get_block_time(target, hashrate):
        """
        Note: In a proof-of-work network, block times depend on the difficulty and the hash-rate. Assuming a constant
        hash-rate between blocks, implies the block-time can be simulated by sampling from a gamma-random variable.

        We calculate the expected time-to-block as follows: We know there are 2**256 possible hashes.
        Hashes which are less than the target are acceptable. The expected pay-off per-hash is
        essentially P = target/2**256. Expected pay-off per-second equals P * H = H*target/(2**256),
        which implies seconds-until-payoff equals 2**256 / (target * H)
        """
        lmbda = 2**256 * 1.0 / target * 1.0 / hashrate

        block_time = int(np.random.gamma(1, scale=lmbda))

        return np.max([1, block_time])

    def run(self, nmb_iterations, seed=None):
        for idx in range(nmb_iterations):
            # Select a miner to create the next block, based on hash-rates
            hr_list = np.array([miner.hash_rate for miner in self.miners])
            weights = hr_list * 1.0 / self.hash_rate

            miner_idx = np.random.choice(np.arange(len(hr_list)), 1, p=weights)[0]

            time_delta = self.get_block_time(self.network.target, self.hash_rate)

            next_block = self.miners[miner_idx].create_block(
                config=self.network.config, time_delta=time_delta, nonce=miner_idx
            )

            self.network.update(next_block)

            for miner in self.miners:
                miner.update(self.network.config, next_block)
