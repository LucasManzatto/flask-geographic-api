from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from app.config import (
    MYSQL_USERNAME,
    MYSQL_PASSWORD,
    MYSQL_HOST,
    MYSQL_PORT,
    MYSQL_DATABASE,
    POSTGRES_DATABASE,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USERNAME,
)


def get_connection(engine_type: str) -> str:
    """
    Get a database engine connection based on the specified engine type.

    Args:
        engine_type (str): The type of database engine. Currently supported options are "mysql" and "postgres".

    Returns:
        SQLAlchemy Engine: An SQLAlchemy Engine object representing the connection to the specified database.

    Raises:
        ValueError: If the specified engine_type is not "mysql" or "postgres".
    """
    if engine_type == "mysql":
        return __get_mysql_connection()
    if engine_type == "postgres":
        return __get_postgres_connection()
    raise f"Engine type {engine_type} not implemented."


def __get_mysql_connection() -> Engine:
    """
    Get a MySQL database engine connection.

    Returns:
        SQLAlchemy Engine: An SQLAlchemy Engine object representing the connection to the MySQL database.
    """
    connection_string = f"mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}"

    engine = create_engine(connection_string)
    return engine


def __get_postgres_connection() -> Engine:
    """
    Get a PostgreSQL database engine connection.

    Returns:
        SQLAlchemy Engine: An SQLAlchemy Engine object representing the connection to the PostgreSQL database.
    """
    connection_string = f"postgresql+psycopg2://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DATABASE}"

    engine = create_engine(connection_string)
    return engine
