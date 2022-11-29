from datetime import datetime
import pandas as pd

from xrc_simulations.utils import convert_list_to_blockchain
from xrc_simulations.simulations import NetworkConfig, GHZ, THZ
from xrc_simulations.simulations import PowSimulator
from xrc_simulations.network import XRCDigishieldNetwork
from xrc_simulations.miners import SimpleMiner, AttackMiner
from xrc_utils import digishield
from xrc_utils.blockcore import target_to_difficulty, get_blockcore_df
from xrc_utils.digishield import bits_to_target
import matplotlib.pyplot as plt


def parse_df(df):

    # Convert bits to target
    df["target"] = df["bits"].apply(lambda x: bits_to_target(x))

    # Add time-since-last block in minutes
    df["timeDeltaMinutes"] = (df["blockTime"] - df["blockTime"].shift(1)) * 1.0 / 60

    # Convert ordinal time-of-day to timestamp
    df["time"] = df["blockTime"].apply(lambda x: datetime.fromtimestamp(int(x)))

    # Calculate percentage change in target
    df["targetChange"] = df["target"] * 1.0 / df["target"].shift(1)

    # Add difficulty (as shown in blockCore -- could be too low by a factor of 4096)
    df["difficulty"] = df["target"].apply(lambda x: target_to_difficulty(x))

    df["difficultyPercentChange"] = (
        df["difficulty"] * 1.0 / df["difficulty"].shift(1) - 1
    )

    return df


def create_plot(df_simulated, df_real):
    fig, (ax1, ax2) = plt.subplots(2, 1)

    df_simulated[["time", "difficulty"]].set_index("time").plot(ax=ax1, marker="o")

    ax1.set_xlim([df_real["time"].values[0], df_real["time"].values[-1]])

    df_real[["time", "difficulty"]].set_index("time").plot(ax=ax2, marker="o")

    ax2.set_xlim([df_real["time"].values[0], df_real["time"].values[-1]])

    plt.gcf().set_size_inches(10, 5)

    plt.tight_layout()

    plt.show()


if __name__ == "__main__":
    n = 150

    raw_data = [digishield.read_header(idx) for idx in range(150000, 151000)]

    blockchain = convert_list_to_blockchain(raw_data[0 : n + 1])

    data = raw_data[n]  # Current data point
    next_data = raw_data[n + 1]

    config = NetworkConfig(
        block_index=data["blockIndex"],
        block_time=data["blockTime"],
        bits=next_data["bits"],
    )

    network = XRCDigishieldNetwork(blockchain=blockchain, config=config)

    miners = [
        SimpleMiner(blockchain=blockchain, hash_rate=300 * GHZ),
        AttackMiner(blockchain=blockchain, hash_rate=70 * THZ, on=False),
    ]

    simulator = PowSimulator(network=network, miners=miners)

    simulator.run(850)

    # Extract the simulated blockchain data, and parse it into a useful dataframe
    df_simulated = pd.DataFrame(network.blockchain).T

    df_simulated = parse_df(df_simulated)

    # Download data from blockCore
    df_real = get_blockcore_df(nmb_blocks=1000, offset=150000)

    df_real["bits"] = df_real["bits"].apply(
        lambda x: int(x, 16)
    )  # Convert to Electrum bits format

    df_real = parse_df(df_real)

    create_plot(df_simulated, df_real)
