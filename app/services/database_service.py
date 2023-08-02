from typing import Any, Union
import pandas as pd
from app.models.database import get_connection
from app.models.trips import Base
from sqlalchemy.sql import text


def write_to_database(
    file_path: str, table_name: str, engine_type: str = "postgres"
) -> bool:
    """
    Write data from a CSV file into a specified table in the database.

    Args:
        file_path (str): The path to the CSV file containing the data.
        table_name (str): The name of the table in the database to write the data into.
        engine_type (str, optional): The type of database engine. Default is "postgres".

    Returns:
        bool: True if the data is successfully written to the database, False otherwise.
    """
    engine = get_connection(engine_type=engine_type)
    with engine.connect() as con:
        statement = text(
            f"""
            CREATE EXTENSION IF NOT EXISTS postgis;
            """
        )
        con.execute(statement)
        con.commit()
    Base.metadata.create_all(engine)
    with engine.connect() as con:
        statement = text(
            f"""
            TRUNCATE TABLE {table_name} 
            RESTART IDENTITY;
            """
        )
        con.execute(statement)
        statement = text(
            f"""
            COPY {table_name}(region,origin_coord,destination_coord,datetime,datasource)
            FROM '{file_path}'
            DELIMITER ','
            CSV HEADER;
            """
        )
        con.execute(statement)
        statement = text(
            f"""
            CREATE INDEX if not exists idx_destination_coord ON trips USING gist (destination_coord);
            """
        )
        con.execute(statement)
        statement = text(
            f"""
            CREATE INDEX if not exists idx_origin_coord ON trips USING gist (origin_coord);
            """
        )
        con.execute(statement)
        con.commit()
    return True


def query_from_database(
    query: str, engine_type: str = "postgres"
) -> Union[pd.DataFrame, Any]:
    """
    Execute a SQL query and retrieve the result as a DataFrame.

    Args:
        query (str): The SQL query to be executed.
        engine_type (str, optional): The type of database engine. Default is "postgres".

    Returns:
        Union[DataFrame, Any]: A DataFrame containing the query result if successful,
        or any other value indicating an error occurred during the query execution.
    """
    engine = get_connection(engine_type=engine_type)
    df = pd.read_sql(query, con=engine)
    return df
