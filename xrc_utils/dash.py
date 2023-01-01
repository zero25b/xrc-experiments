from tests.fixtures import DASH_MAINNET_BLOCKS
from pow_simulations.utils import convert_list_to_blockchain
from xrc_utils.headers import bits_to_target


class ReadHeader:
    def __init__(self):

        self.DATA = convert_list_to_blockchain(DASH_MAINNET_BLOCKS)

        for idx in self.DATA:
            self.DATA[idx]["bits"] = self.DATA[idx]["target"]
            self.DATA[idx]["target"] = bits_to_target(self.DATA[idx]["target"])

    def __call__(self, h):
        assert (h < 999925) & (h >= 999900), "Please select h in [999900, 999924]"
        return self.DATA.get(h)


read_header = ReadHeader()
