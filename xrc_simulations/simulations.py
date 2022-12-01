from dataclasses import dataclass
from typing import List, Type
import numpy as np
from numpy.random import choice
from xrc_utils.blockcore import target_to_difficulty
from xrc_utils.digishield import bits_to_target, MAX_TARGET
from copy import copy

SEED = 1234

GHZ = 10**9
THZ = 10**12


@dataclass
class XRCBlock:
    version: int
    previous_block_hash: str
    merkleroot: str
    block_time: int
    bits: int
    nonce: int
    block_index: int

    def to_json(self) -> dict:
        return {
            "version": self.version,
            "previousBlockHash": self.previous_block_hash,
            "merkleroot": self.merkleroot,
            "blockTime": self.block_time,
            "bits": self.bits,
            "nonce": self.nonce,
            "blockIndex": self.block_index,
        }


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
    Base class for miner-xrc_simulations
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
        next_block = XRCBlock(
            version=0,
            previous_block_hash=synthetic_hash,
            merkleroot="synthetic",
            block_time=config.block_time + time_delta,
            bits=config.bits,
            nonce=nonce,
            block_index=config.block_index + 1,
        )
        return next_block

    def update(self, config: NetworkConfig, next_block: XRCBlock):
        self.blockchain[next_block.block_index] = next_block.to_json()
        self.set_hash_rate(config)


class MockNetworkBase:
    """
    Base class to simulate various difficulty adjustments schemes such as DigiShield V0. Once the network difficulty is
    set, time-to-next block can be treated as a Gamma random variable that depends on the network-wide hash-rate and
    the difficulty. Inherit from this class and implement the get_target routine, which should contain the difficulty
    adjustment logic.
    """

    def __init__(self, blockchain: dict, config: NetworkConfig):
        self.blockchain = copy(blockchain)  # The blockchain should be a copy
        self.config = config
        self.logging_list = []

    @property
    def difficulty(self):
        return self.config.difficulty

    @property
    def target(self):
        return self.config.target

    def read_header(self, idx):
        header = self.blockchain.get(idx)
        assert (header is not None) & (
            header["blockIndex"] == idx
        ), f"Block index {idx} is not valid"
        return header

    def get_target(self, *args):
        raise NotImplementedError

    def update(self, next_block: XRCBlock):
        # Add the next block to the internal blockchain
        self.blockchain[next_block.block_index] = next_block.to_json()

        # Calculate the next target in bits
        bits = self.get_target(next_block.block_index + 1)

        # Update the internal configuration based on the new block
        self.config = NetworkConfig(
            block_time=next_block.block_time,
            block_index=next_block.block_index,
            bits=bits,
        )


class PowSimulator(object):
    def __init__(
        self, network: Type[MockNetworkBase], miners: List[Type[MockMinerBase]]
    ):
        self.network = network
        self.miners = miners

    @property
    def hash_rate(self):
        return np.sum([miner.hash_rate for miner in self.miners], axis=0)

    @staticmethod
    def get_block_time(target, hashrate):
        """
        Note: In a proof-of-work network, block times depend on the difficulty and the hash-rate. Assuming a constant
        hash-rate between blocks, implies the block-time can be simulated by sampling from a gamma-random variable.

        We calculate the expected time-to-block as follows: We know MAX_TARGET = (2**236 - 1), and there are 2**256
        possible hashes. Hashes which are less than the target are acceptable. The expected pay-off per-hash is
        essentially P = target/2**256 ~ target/(MAX_TARGET*2**20) = 1/(2**20*D). Expected pay-off per-second is
        P * H = H/(2**20 * D), which implies seconds-until-payoff equals 2**20 * D / H
        """
        lmbda = 2**20 * (MAX_TARGET * 1.0 / target) * 1.0 / hashrate

        block_time = np.random.gamma(1, scale=lmbda)

        return block_time

    def run(self, nmb_iterations, seed=None):
        for idx in range(nmb_iterations):
            # Select a miner to create the next block, based on hash-rates
            hr_list = np.array([miner.hash_rate for miner in self.miners])
            weights = hr_list * 1.0 / self.hash_rate

            miner_idx = np.random.choice(np.arange(len(hr_list)), 1, p=weights)[0]

            time_delta = self.get_block_time(self.network.target, self.hash_rate)

            next_block = self.miners[miner_idx].create_block(
                self.network.config, time_delta, miner_idx
            )

            self.network.update(next_block)

            for miner in self.miners:
                miner.update(self.network.config, next_block)
