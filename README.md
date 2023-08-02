# Upload API

This is a Flask-based web application that allows users to upload trips data, ingest it into a database, and retrieve weekly average data for specific regions or coordinates.

## Installation
1. Clone the repository:

```bash
git clone https://github.com/LucasManzatto/upload_api.git
```

2. Navigate to the project directory:
```bash
cd upload_api
```

3. Build and run the Docker containers using Docker Compose:

```bash
docker-compose up --build
```
The application will start running on http://localhost:5000/.

## Database
The SQL database used for this application is PostgreSQL. PostgreSQL was chosen because of its excellent support for geographic data and advanced spatial features. It allows us to efficiently store and query location-based information, making it an ideal choice for managing trips data with geographic coordinates.

## Usage

**1. Upload trips data:**
To upload trips data, use the **/upload** endpoint by sending a POST request with the file field containing the data file path. The application will ingest the data into the database.

```bash
curl -X POST -F "file=@/fullpath/to/file/trips.csv" http://localhost:5000/upload
```
Replace **'/fullpath/to/file/trips.csv'** with the complete file path of the CSV file you want to upload.

**2. Retrieve weekly average data:**

To get the weekly average data, use the /get_weekly_average endpoint by sending a POST request with JSON data containing either the region or coordinates. The application will return the weekly average data in JSON format.

**Retrieve weekly average data by region:**
```bash
curl -X POST --header "Content-Type: application/json" -d '{"region": "Prague"}' http://localhost:5000/get_weekly_average
```

**Retrieve weekly average data by coordinates::**

```bash
curl -X POST --header "Content-Type: application/json" -d '{
    "coordinates": {
        "first_point": {"lat": 14.4973794438195, "lon": 50.00136875782316},
        "second_point": {"lat": 14.43109483523328, "lon": 50.04052930943246}
    }
}' http://localhost:5000/get_weekly_average
```
Replace {"lat": ..., "lon": ...} with the latitude and longitude coordinates of your desired first_point and second_point.

## Endpoints
The application exposes the following endpoints:

**Upload trips data:** /upload

**Retrieve weekly average data:** /get_weekly_average
