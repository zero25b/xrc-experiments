from xrc_experiments.utils import dump_blockchain_headers_file_to_pandas
from xrc_experiments.blockcore_utils import get_blockcore_df
from xrc_experiments import DATA_DIR

def test_blockchain_headers_file_data_integrity():

    blockchain_headers_file = DATA_DIR.joinpath("blockchain_headers_corrupt").as_posix()

    df_blockcore = get_blockcore_df(nmb_blocks=6000, offset=150000)

    df_file = dump_blockchain_headers_file_to_pandas(blockchain_headers_file)

    # The data available on blockcore contains more columns than the blockchain_headers_corrupt file
    df_blockcore = df_blockcore[df_file.columns]

    # The blockcore data we have downloaded extends past the end of the file data. So select all rows in
    # blockcore_data until the end of file data. Then remove the beginning of the file data to match the start of the
    # downloaded blockcore data
    file_index_selection = (df_file['blockIndex'] >= df_blockcore['blockIndex'].min())

    df_file = df_file[file_index_selection].reset_index(drop=True)

    blockcore_index_selection = (df_blockcore['blockIndex'] <= df_file['blockIndex'].max())

    df_blockcore = df_blockcore[blockcore_index_selection]

    # The last row in the file-data is corrupt
    assert not df_blockcore.equals(df_file)

    # Everything else should agree
    assert df_blockcore[:-1].equals(df_file[:-1])
