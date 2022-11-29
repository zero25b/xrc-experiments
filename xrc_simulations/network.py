from xrc_simulations.simulations import MockNetworkBase
from xrc_utils.digishield import (
    DIGISHIELDX11_BLOCK_HEIGHT,
    MissingHeader,
    bits_to_target,
    target_to_bits,
    MAX_TARGET,
)


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
        new_target = new_target / nAveragingTargetTimespanV4
        new_targetBits = target_to_bits(int(new_target))
        bitsToTarget = bits_to_target(new_targetBits)
        bitsToTarget = min(MAX_TARGET, bitsToTarget)
        assert bits_to_target(target_to_bits(bitsToTarget)) == bitsToTarget
        return target_to_bits(bitsToTarget)
