from typing import Dict, Optional, Union
import pandas as pd
import app.services.database_service as database_service
from shapely import wkt


def write_to_database(file_path: str) -> bool:
    """
    Write data from a file to the database table named 'trips'.

    Args:
        file_path (str): The path to the file containing the data to be ingested into the database.

    Returns:
        bool: True if the data is successfully written to the database, False otherwise.

    Raises:
        Any exceptions raised by the database_service.write_to_database function.
    """
    return database_service.write_to_database(file_path=file_path, table_name="trips")

def get_weekly_average(region: Optional[str] = None, coordinates: Optional[Dict[str, Union[str, Dict[str, float]]]] = None) -> Dict[str, float]:
    """
    Get the weekly average data for a specific region or coordinates.

    Args:
        region (str, optional): The name of the region for which to calculate the weekly average.
        coordinates (dict, optional): A dictionary containing the coordinates of two points (lat and lon) to calculate the average for trips within the bounding box defined by these points.

    Returns:
        dict: A dictionary containing the weekly average as a float value.

    Raises:
        ValueError: If both 'region' and 'coordinates' are provided in the input.
        KeyError: If 'coordinates' is provided, but any of 'first_point' or 'second_point' is missing from it.
        Any exceptions raised by the database_service.query_from_database function.
    """
    if region:
        filter = f"region = '{region}'"
    if coordinates:
        first_point = f"{coordinates['first_point']['lat']} {coordinates['first_point']['lon']}"
        second_point = f"{coordinates['second_point']['lat']} {coordinates['second_point']['lon']}"
        filter = f"""
        ST_Contains(ST_Envelope('LINESTRING ({first_point}, {second_point})'),
        ST_MakeLine(origin_coord,
        destination_coord))
            """
    query = f"""
        with cte1 as
        (
        select
            COUNT(region) as total,
            extract(WEEK
        from
            datetime) as week
        from
            trips
        where
            {filter}
        group by
            week)
        select
            AVG(total) as weekly_average
        from
            cte1
        """
    return database_service.query_from_database(query=query)
