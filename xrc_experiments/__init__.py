import pathlib

EXPERIMENTS_DIR = pathlib.Path(__file__).parent

ROOT_DIR = EXPERIMENTS_DIR.parent

X11_DIR = ROOT_DIR.joinpath("x11-hash")

X13_DIR = ROOT_DIR.joinpath("x13-hash")

DATA_DIR = ROOT_DIR.joinpath("data")
