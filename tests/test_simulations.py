from copy import copy

import numpy as np
from xrc_simulations.miners import SimpleMiner
from xrc_simulations.network import XRCDigishieldNetwork
from xrc_simulations.simulations import XRCBlock, NetworkConfig, GHZ, PowSimulator
from tests.fixtures import ELECTRUM_154999, FixtureSimulator
from xrc_simulations.utils import convert_list_to_blockchain
from xrc_utils import digishield
from xrc_utils.blockcore import target_to_difficulty
from xrc_utils.digishield import (
    bits_to_target,
    get_targetDigishield,
    target_to_bits,
)


def test_xrc_block_to_json():

    next_block = XRCBlock(
        version=536870912,
        previous_block_hash="536fd637e87dfa548857b81c46f9078344949f2b8d858b305a5c1f6b4ce06640",
        merkleroot="4f72d77f443edb77eadf67ad3cbdad4d0115a31f481968af04772629ee570b73",
        block_time=1664212597,
        bits=453151324,
        nonce=3374795661,
        block_index=154999,
    )

    next_block_json = next_block.to_json()

    assert next_block_json == ELECTRUM_154999


def test_network_config():
    config = NetworkConfig(block_time=1664212597, block_index=154999, bits=453151324)

    assert config.target == bits_to_target(453151324)

    assert config.difficulty == target_to_difficulty(bits_to_target(453151324))


def test_network_prediction():
    """
    When a synthetic blockchain is initiated from a real data, check that the first target prediction
    agrees with the corresponding target in the real data.
    """
    raw_data = [digishield.read_header(idx) for idx in range(150000, 150500)]

    n = 491
    blockchain = convert_list_to_blockchain(raw_data[0 : n + 1])

    data = raw_data[n]  # Last data point in the blockchain
    next_data = raw_data[n + 1]
    next_idx = next_data["blockIndex"]

    config = NetworkConfig(
        block_index=data["blockIndex"],
        block_time=data["blockTime"],
        bits=next_data["bits"],
    )

    network = XRCDigishieldNetwork(blockchain=copy(blockchain), config=config)

    miners = [
        SimpleMiner(blockchain=copy(blockchain), hash_rate=100 * GHZ),
    ]

    simulator = PowSimulator(network=network, miners=miners)

    simulator.run(1)

    fake_data = network.read_header(next_idx)

    real_data = digishield.read_header(next_idx)

    # The next target from the simulator should be the target from the real data
    assert fake_data["bits"] == target_to_bits(get_targetDigishield(next_idx))

    # The target and block index should agree one-step ahead
    assert real_data["bits"] == fake_data["bits"]
    assert real_data["blockIndex"] == fake_data["blockIndex"]

    # The merkleroot of the fake data equals 'synthetic'
    assert real_data["merkleroot"] != "synthetic"
    assert fake_data["merkleroot"] == "synthetic"


def test_with_known_block_times():
    """
    Check that we recover the correct targets when feeding known block times.
    """
    raw_data = [digishield.read_header(idx) for idx in range(150000, 151000)]

    n = 491  # !- must select n < 1000
    blockchain = convert_list_to_blockchain(raw_data[0 : n + 1])

    data = raw_data[n]  # Last data point in the blockchain
    next_data = raw_data[n + 1]

    config = NetworkConfig(
        block_index=data["blockIndex"],
        block_time=data["blockTime"],
        bits=next_data["bits"],
    )

    # Calculate the time-since-last-block for the blocks walking forward from the end of the real data.
    block_times = []
    for data in raw_data[n:1000]:
        block_times.append(data["blockTime"])

    block_times = np.array(block_times)
    time_deltas = block_times[1:] - block_times[:-1]

    # Instantiate a simulation, using the known time-deltas
    network = XRCDigishieldNetwork(blockchain=copy(blockchain), config=config)

    miners = [
        SimpleMiner(blockchain=copy(blockchain), hash_rate=100 * GHZ),
    ]

    simulator = FixtureSimulator(
        network=network, miners=miners, time_deltas=time_deltas
    )

    simulator.run(1000 - n - 1)

    for idx in network.blockchain:
        assert (
            network.blockchain[idx]["blockTime"]
            == digishield.read_header(idx)["blockTime"]
        )
        assert network.blockchain[idx]["bits"] == digishield.read_header(idx)["bits"]
