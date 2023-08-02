from flask import Blueprint, flash, request, jsonify
from app.services import trips_service, file_service
from datetime import datetime

trips_blueprint = Blueprint("trips", __name__)


@trips_blueprint.route("/upload", methods=["POST"])
def upload():
    """
    Endpoint for uploading a file and ingesting data into the database.

    Returns:
        JSON: A JSON response containing the status and time taken for ingestion.

    Raises:
        400 (Bad Request): If the request does not have a file part or no file is selected.
        400 (Bad Request): If an error occurs during file writing or database ingestion.
    """
    start_time = datetime.now()
    # check if the post request has the file part
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]

    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    try:
        file_path = file_service.write_file(file=file)
        trips_service.write_to_database(file_path=file_path)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    end_time = datetime.now()
    return (
        jsonify(
            {
                "status": "Ingestion finished sucessfully",
                "time": str(end_time - start_time),
            }
        ),
        200,
    )


@trips_blueprint.route("/get_weekly_average", methods=["POST"])
def get_weekly_average():
    """
    Endpoint for retrieving the weekly average data for a specific region or coordinates.

    Returns:
        JSON: A JSON response containing the weekly average data in records format.

    Raises:
        400 (Bad Request): If the request JSON data is malformed or missing required fields.
    """
    data = request.json
    if "region" in data:
        df = trips_service.get_weekly_average(region=data["region"])
    if "coordinates" in data:
        if "first_point" not in data["coordinates"] or "second_point" not in data["coordinates"]:
            return jsonify({"error": "The 2 points must be provided on the coordinates"}), 400
        df = trips_service.get_weekly_average(coordinates=data["coordinates"])
    return jsonify(df.to_json(orient="records")), 200


# # Upload file as stream to a file.
# @trips_blueprint.route("/upload_test", methods=["POST"])
# def upload_test():
#     start_time = datetime.now()
#     try:
#         folder = "/tmp/trips/"
#         Path(folder).mkdir(parents=True, exist_ok=True)
#         file_path = f"{folder}test.csv"
#         with open(file_path, "bw") as f:
#             chunk_size = 4096
#             while True:
#                 chunk = request.stream.read(chunk_size)
#                 if len(chunk) == 0:
#                     break
#                 f.write(chunk)
#         data = file_service.read_file(file_path=file_path)
#         trips_service.write_to_database(df=data)
#     except Exception as e:
#         raise (e)
#     end_time = datetime.now()
#     return (
#         jsonify(
#             {
#                 "status": "Ingestion finished sucessfully",
#                 "time": str(end_time - start_time),
#             }
#         ),
#         200,
#     )
