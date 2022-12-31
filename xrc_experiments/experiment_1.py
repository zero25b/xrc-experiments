from datetime import datetime

import pandas as pd

from xrc_simulations.utils import convert_list_to_blockchain
from xrc_simulations.simulations import PowSimulator, NetworkConfig, GHZ, THZ
from xrc_simulations.network import (
    DarkGravityWaveNetwork,
)
from xrc_simulations.miners import SimpleMiner, AttackMiner
from xrc_utils import digishield, OUTPUT_DIR
from xrc_utils.analysis import (
    add_analysis_columns,
    create_bounded_difficulty_plot,
    create_block_difficulty_plot,
)
import matplotlib.pyplot as plt


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
    n = 1150

    start = 150000
    nmb_blocks = 10000
    end = start + nmb_blocks

    raw_data = [digishield.read_header(idx) for idx in range(start, end)]

    blockchain = convert_list_to_blockchain(raw_data[0 : n + 1])

    data = raw_data[n]  # Current data point
    next_data = raw_data[n + 1]

    config = NetworkConfig(
        block_index=data["blockIndex"],
        block_time=data["blockTime"],
        bits=next_data["bits"],
    )

    network = DarkGravityWaveNetwork(blockchain=blockchain, config=config)

    miners = [
        SimpleMiner(blockchain=blockchain, hash_rate=2 * THZ),
        AttackMiner(blockchain=blockchain, hash_rate=70 * THZ, on=True),
    ]

    simulator = PowSimulator(network=network, miners=miners)

    simulator.run(nmb_blocks - n)

    # Extract the simulated blockchain data, and parse it into a useful dataframe
    df_simulated = network.get_df()

    df_simulated = add_analysis_columns(df_simulated)

    start_time = datetime.strptime("2022-08-31", "%Y-%m-%d")

    end_time = start_time + pd.Timedelta("1d")

    create_block_difficulty_plot(
        df_simulated,
        start_time,
        end_time,
        OUTPUT_DIR.joinpath("simulated_august_31_blocks.png"),
    )

    create_bounded_difficulty_plot(
        df_simulated,
        start_time,
        end_time,
        OUTPUT_DIR.joinpath("simulated_august_31_bounds.png"),
    )

    df_real = pd.DataFrame(raw_data)

    df_real = add_analysis_columns(df_real)

    create_block_difficulty_plot(
        df_real, start_time, end_time, OUTPUT_DIR.joinpath("real_august_31_blocks.png")
    )

    create_bounded_difficulty_plot(
        df_real, start_time, end_time, OUTPUT_DIR.joinpath("real_august_31_bounds.png")
    )

    create_plot(df_simulated, df_real)
