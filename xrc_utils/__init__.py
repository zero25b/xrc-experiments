import pathlib

XRC_UTILS_DIR = pathlib.Path(__file__).parent

ROOT_DIR = XRC_UTILS_DIR.parent

EXPERIMENTS_DIR = ROOT_DIR.joinpath("xrc_experiments")

DATA_DIR = ROOT_DIR.joinpath("data")

X13_DIR = ROOT_DIR.joinpath("x13-hash")

X11_DIR = ROOT_DIR.joinpath("x11-hash")
