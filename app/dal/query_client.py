import awswrangler as wr
import pandas as pd
from app.utils.settings import Settings
import abc
import numpy as np


class ABCQueryClient():

    @abc.abstractmethod
    def run_query(self, query: str) -> pd.DataFrame:
        """Runs a sql query and return a data frame"""


class QueryClient(ABCQueryClient):

    def __init__(self, app_conf: Settings):
        self.config: Settings = app_conf

    def run_query(self, query: str) -> pd.DataFrame:
        return wr.athena.read_sql_query(
            query,
            database=self.config.cestamos_db,
            s3_output=self.config.s3_output_path
        ).replace({np.nan: None})