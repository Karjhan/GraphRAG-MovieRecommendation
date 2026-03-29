import pandas as pd
import pyarrow.parquet as pq
from config.settings import settings


def load_movies():

    return pd.read_csv(settings.MOVIES_PATH)


def load_embeddings():

    table = pq.read_table(settings.EMBEDDINGS_PATH)
    return table.to_pandas()