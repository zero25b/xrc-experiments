from datetime import datetime

import pandas as pd
from matplotlib import pyplot as plt

from xrc_utils.blockcore import target_to_difficulty
from xrc_utils.headers import bits_to_target


def add_analysis_columns(df: pd.DataFrame) -> pd.DataFrame:

    # Convert bits to target
    df["target"] = df["bits"].apply(lambda x: bits_to_target(x))

    # Add time-since-last block in minutes
    df["timeDeltaMinutes"] = (df["blockTime"] - df["blockTime"].shift(1)) * 1.0 / 60

    # Convert ordinal time-of-day to timestamp
    df["time"] = df["blockTime"].apply(lambda x: datetime.fromtimestamp(int(x)))

    # Calculate percentage change in target
    df["targetChange"] = df["target"] * 1.0 / df["target"].shift(1)

    # Add difficulty
    df["difficulty"] = df["target"].apply(lambda x: target_to_difficulty(x))

    df["difficultyPercentChange"] = (
        df["difficulty"] * 1.0 / df["difficulty"].shift(1) - 1
    )

    return df


def create_block_difficulty_plot(df, start_time, end_time, output_path):
    # Same blocks on November 27, 2022.
    # Plot block-number on the x-axis, change-in-difficulty on the y-axis
    fig, (ax1, ax2) = plt.subplots(2, 1)

    recent_df = df.copy()

    recent_df = recent_df[
        (recent_df["time"] >= start_time) & (recent_df["time"] < end_time)
    ]

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

    fig.suptitle = f"Difficulty: blocks {recent_df.index[0]} - {recent_df.index[-1]}, # blocks = {len(recent_df)}"

    plt.gcf().set_size_inches(20, 10)

    plt.savefig(output_path, dpi=200)

    plt.close()


def create_bounded_difficulty_plot(df, start_time, end_time, output_path):

    recent_df = df.copy()

    recent_df = recent_df[
        (recent_df["time"] >= start_time) & (recent_df["time"] < end_time)
    ]

    # Plot with respect to time
    start_date = recent_df["time"][recent_df.index[0]].date()
    end_date = recent_df["time"][recent_df.index[-1]].date()

    # recent_df["time"] = recent_df["time"].apply(lambda x: x.time())

    recent_df = recent_df.set_index("time")

    title = f"Difficulty: {start_date} - {end_date}: blocks {recent_df['blockIndex'][0]} - {recent_df['blockIndex'][-1]}, # blocks = {len(recent_df)}"

    recent_df[["difficulty"]].plot(marker="o", title=title).set_xlim(
        recent_df.index[0], recent_df.index[-1]
    )

    plt.gcf().set_size_inches(10, 5)

    plt.tight_layout()

    plt.savefig(output_path, dpi=200)

    plt.close()
