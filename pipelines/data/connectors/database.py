"""Define data connector to interact with databases."""

from typing import Self

import pandas as pd
from sqlalchemy import create_engine

from pipelines.data.connectors.base import BaseConnector


class DatabaseConnector(BaseConnector):
    """Define data connector to interact with database."""

    def __init__(  # noqa: PLR0913
        self: Self,
        dialect: str,
        host: str,
        db_name: str,
        username: str,
        password: str,
    ) -> None:
        """Initialize database connector.

        :param dialect: Database dialect, e.g., postgresql.
        :param host: Database host.
        :param db_name: Database name.
        :param username: Database username.
        :param password: Database password.
        """
        self.engine = create_engine(
            f"{dialect}://{username}:{password}@{host}/{db_name}",
        )

    def read_dataframe(
        self: Self,
        data_object_name: str,
        **kwargs: dict,
    ) -> pd.DataFrame:
        """Read DataFrame.

        :param data_object_name: Data object to read.
        :return: Retrieved DataFrame.
        """
        return pd.read_sql_table(
            table_name=data_object_name,
            con=self.engine,
            schema=kwargs.get("schema"),
        )

    def write_dataframe(
        self: Self,
        data_object_name: str,
        df: pd.DataFrame,
        **kwargs: dict,
    ) -> None:
        """Write DataFrame.

        :param data_object_name: Data object to write.
        :param df: DataFrame to write.
        """
        df.to_sql(
            name=data_object_name,
            con=self.engine,
            schema=kwargs.get("schema"),
            if_exists=kwargs.get("if_exists", "replace"),
            index=False,
        )
