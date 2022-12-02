import pandas as pd

from xrc_utils.analysis import (
    add_analysis_columns,
    create_block_difficulty_plot,
    create_bounded_difficulty_plot,
)
from xrc_utils.electrum import dump_blockchain_headers_file_to_df
from xrc_utils.headers import BLOCKCHAIN_HEADERS_PATH
from datetime import datetime
from xrc_utils import OUTPUT_DIR
import matplotlib.pyplot as plt


def create_global_difficulty_plot(df, output_path):
    # Generate a global image of difficulty versus time
    df[["time", "difficulty"]].set_index("time").plot()

    plt.gcf().set_size_inches(20, 10)

    plt.savefig(output_path, dpi=200)

    plt.close()


def create_difficulty_plot_one_day(df, start_time, output_path):
    end_time = start_time + pd.Timedelta("1d")

    subset_df = df[(df["time"] >= start_time) & (df["time"] < end_time)]

    # Plot with respect to time
    recent_df = subset_df.copy()

    date = recent_df["time"][recent_df.index[0]].date()

    recent_df["time"] = recent_df["time"].apply(lambda x: x.time())

    recent_df = recent_df.set_index("time")

    title = f"Difficulty versus block time {date}: blocks {recent_df['blockIndex'][0]} - {recent_df['blockIndex'][-1]}"

    recent_df[["difficulty"]].plot(marker="o", title=title).set_xlim(
        recent_df.index[0], recent_df.index[-1]
    )

    plt.gcf().set_size_inches(10, 5)

    plt.tight_layout()

    plt.savefig(output_path, dpi=200)

    plt.close()


def create_difficulty_by_block_plot(df, start_time, output_path):
    # Same blocks on November 27, 2022.
    # Plot block-number on the x-axis, change-in-difficulty on the y-axis
    fig, (ax1, ax2) = plt.subplots(2, 1)

    end_time = start_time + pd.Timedelta("3d")

    recent_df = df[(df["time"] >= start_time) & (df["time"] < end_time)]

    recent_df = recent_df.rename(
        columns={
            "blockIndex": "block number",
            "difficultyPercentChange": "difficulty % change",
        }
    )
    recent_df = recent_df.set_index("block number")

    recent_df[["difficulty"]].plot(ax=ax1, marker="o", xticks=recent_df.index.values)
    ax1.set_xlim([recent_df.index.values[0], recent_df.index.values[-1]])

    recent_df[["difficulty % change"]].plot.bar(ax=ax2)

    for ax in [ax1, ax2]:
        # Only display every 50th tick.
        [
            l.set_visible(False)
            for (i, l) in enumerate(ax.xaxis.get_ticklabels())
            if i % 30 != 0
        ]
        [l.set_rotation(90) for l in ax.xaxis.get_ticklabels()]

    print("Number blocks = ", recent_df.shape)

    fig.suptitle = f"Difficulty versus block time: blocks {recent_df.index[0]} - {recent_df.index[-1]}"

    plt.gcf().set_size_inches(20, 10)

    plt.savefig(output_path, dpi=200)

    plt.close()


if __name__ == "__main__":
    """
    Get the headers-data from the BLOCKCHAIN_HEADERS file. Generate images to display
    difficulty versus block-time
    """

    raw_df = dump_blockchain_headers_file_to_df(
        BLOCKCHAIN_HEADERS_PATH, bits_format="electrum"
    )

    # Data is missing before header 136000. Artifact of electrum wallet.
    raw_df = raw_df[136000:].reset_index(drop=True)

    df = add_analysis_columns(raw_df)

    create_global_difficulty_plot(df, OUTPUT_DIR.joinpath("global_difficulty.png"))

    # Now look at blocks on November 27, 2022
    start_time = datetime.strptime("2022-11-27", "%Y-%m-%d")

    end_time = start_time + pd.Timedelta("1d")

    create_bounded_difficulty_plot(
        df, start_time, end_time, OUTPUT_DIR.joinpath("november_27.png")
    )

    end_time = start_time + pd.Timedelta("1d")

    create_block_difficulty_plot(
        df,
        start_time,
        end_time,
        OUTPUT_DIR.joinpath("november_27_change_in_difficulty.png"),
    )
