from typing import Dict

from xrc_simulations.simulations import MockNetworkBase, NetworkConfig
from xrc_utils.digishield import (
    DIGISHIELDX11_BLOCK_HEIGHT,
    MissingHeader,
    MAX_TARGET,
)
from xrc_utils.headers import bits_to_target, target_to_bits


class XRCDigishieldNetwork(MockNetworkBase):
    def get_averageTimepast(self, height: int) -> int:
        medianTimespan = 11
        median = list()

        for i in range(medianTimespan):
            chainedHeader = self.read_header(height - i)
            if chainedHeader is None:
                break
            else:
                median.append(chainedHeader.get("blockTime"))

        median.sort()

        firstTimespan = median[0]
        lastTimespan = median[-1]
        differenceTimespan = lastTimespan - firstTimespan
        timespan = int(differenceTimespan / 2)
        averageDateTime = firstTimespan + timespan

        return averageDateTime

    def get_medianTimepast(self, height: int) -> int:
        medianTimespan = 11
        median = medianTimespan * [0]
        begin = medianTimespan
        end = medianTimespan

        for i in range(medianTimespan):
            chainedHeader = self.read_header(height - i)
            if chainedHeader is None:
                break
            else:
                begin = begin - 1
                median[i] = chainedHeader.get(
                    "blockTime"
                )  # Note that 'timestamp' in Electrum is 'blockTime' in Blockcore

        median.sort()

        return median[int(begin + ((end - begin) / 2))]

    def get_target(self, height):
        nAveragingInterval = 10 * 5  # block
        multiAlgoTargetSpacingV4 = 10 * 60  # seconds
        nAveragingTargetTimespanV4 = nAveragingInterval * multiAlgoTargetSpacingV4
        nMaxAdjustDownV4 = 16
        nMaxAdjustUpV4 = 8
        nMinActualTimespanV4 = nAveragingTargetTimespanV4 * (100 - nMaxAdjustUpV4) / 100
        nMaxActualTimespanV4 = (
            nAveragingTargetTimespanV4 * (100 + nMaxAdjustDownV4) / 100
        )
        # medianTimespan = 11

        if (height - DIGISHIELDX11_BLOCK_HEIGHT) <= (nAveragingInterval + 11):
            return int(
                0x000000000001A61A000000000000000000000000000000000000000000000000
            )

        last = self.read_header(height - 1)
        first = self.read_header(height - nAveragingInterval)
        if not first or not last:
            raise MissingHeader()

        # Limit adjustment step
        # Use medians to prevent time-warp attacks
        last_averagetimestamp = self.get_averageTimepast(
            last.get("blockIndex")
        )  # Note that blockIndex in blockcore -> block_height in electrum
        first_averagetimestamp = self.get_averageTimepast(first.get("blockIndex"))
        nActualTimespan = last_averagetimestamp - first_averagetimestamp
        nActualTimespan = (
            nAveragingTargetTimespanV4
            + (nActualTimespan - nAveragingTargetTimespanV4) / 4
        )

        if nActualTimespan < nMinActualTimespanV4:
            nActualTimespan = nMinActualTimespanV4
        if nActualTimespan > nMaxActualTimespanV4:
            nActualTimespan = nMaxActualTimespanV4

        bits = last.get("bits")
        target = bits_to_target(bits)
        new_target = target * int(nActualTimespan)
        new_target = new_target * 1.0 / nAveragingTargetTimespanV4
        new_targetBits = target_to_bits(int(new_target))
        bitsToTarget = bits_to_target(new_targetBits)
        bitsToTarget = min(MAX_TARGET, bitsToTarget)
        # assert bits_to_target(target_to_bits(bitsToTarget)) == bitsToTarget
        return target_to_bits(bitsToTarget)


class DarkGravityWaveNetwork(MockNetworkBase):
    def __init__(
        self,
        blockchain: Dict,
        config: NetworkConfig,
        nAveragingInterval=75,
        multiAlgoTargetSpacingV4=10 * 60,
    ):
        self.nAveragingInterval = nAveragingInterval
        self.multiAlgoTargetSpacingV4 = multiAlgoTargetSpacingV4
        super().__init__(blockchain, config)

    def get_target(self, height):

        nAveragingTargetTimespanV4 = (
            self.nAveragingInterval * self.multiAlgoTargetSpacingV4
        )

        if (height - DIGISHIELDX11_BLOCK_HEIGHT) <= (self.nAveragingInterval + 11):
            return int(
                0x000000000001A61A000000000000000000000000000000000000000000000000
            )

        last = self.read_header(height - 1)
        first = self.read_header(height - self.nAveragingInterval)
        if not first or not last:
            raise MissingHeader()

        bnPastTargetAvg = 0

        for nCountBlocks in range(1, self.nAveragingInterval + 1):
            header = self.read_header(height - nCountBlocks)
            bnTarget = bits_to_target(header.get("bits"))
            if nCountBlocks == 1:
                bnPastTargetAvg = bnTarget
            else:
                bnPastTargetAvg = (bnPastTargetAvg * nCountBlocks + bnTarget) / (
                    nCountBlocks + 1
                )

        nActualTimespan = last.get("blockTime") - first.get("blockTime")

        if nActualTimespan < 1 / 3.0 * nAveragingTargetTimespanV4:
            nActualTimespan = 1 / 3.0 * nAveragingTargetTimespanV4
        elif nActualTimespan > 3 * nAveragingTargetTimespanV4:
            nActualTimespan = 3 * nAveragingTargetTimespanV4

        new_target = bnPastTargetAvg * nActualTimespan / nAveragingTargetTimespanV4
        new_target = min(MAX_TARGET, new_target)
        new_targetBits = target_to_bits(int(new_target))
        bitsToTarget = bits_to_target(new_targetBits)

        return target_to_bits(bitsToTarget)
