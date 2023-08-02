import pandas as pd
from pathlib import Path


def write_file(folder: str, file: bytes) -> str:
    """
    Write the uploaded file to the temporary directory.

    Args:
        file (bytes): The file object to be saved.

    Returns:
        str: The file path where the file is saved.
    """
    folder = f"/tmp/{folder}"
    Path(folder).mkdir(parents=True, exist_ok=True)
    file_path = f"{folder}{file.filename}"
    file.save(file_path)
    # with open(file_path, "bw") as f:
    #     chunk_size = 4096
    #     while True:
    #         chunk = request.stream.read(chunk_size)
    #         if len(chunk) == 0:
    #             break
    #         f.write(chunk)
    return file_path


def read_file(file_path: str) -> pd.DataFrame:
    """
    Read the data from the given file path and return it as a pandas DataFrame.

    Args:
        file_path (str): The path of the file to read.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the data from the file.

    Raises:
        Exception: If the file format is not allowed (only CSV format is allowed).
    """
    if not __allowed_file(file=file_path):
        raise Exception("Only csv format is allowed")
    if ".csv" in file_path:
        return __read_csv(file_path=file_path)


def __read_csv(file_path: str) -> pd.DataFrame:
    """
    Read the data from the CSV file and return it as a pandas DataFrame.

    Args:
        file_path (str): The path of the CSV file to read.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the data from the CSV file.
    """
    df = pd.read_csv(file_path, skiprows=[0, 1, 2], skipfooter=1)
    return df


def __allowed_file(file: str) -> bool:
    """
    Check if the file has an allowed format (CSV).

    Args:
        file (str): The name of the file to check.

    Returns:
        bool: True if the file has an allowed format, False otherwise.
    """
    return "." in file and file.rsplit(".", 1)[1].lower() in ["csv"]
