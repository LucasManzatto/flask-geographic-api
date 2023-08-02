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

The following SQL statement is an example of how the application utilizes PostgreSQL's PostGIS extension to determine whether a given line (trip) is contained within a specified bounding box.

```sql
ST_Contains(ST_Envelope('LINESTRING ({first_point_lat} {first_point_lon}, {second_point_lat} {second_point_long})'),
ST_MakeLine(origin_coord,destination_coord))
```

Explanation:

1. `ST_Envelope('LINESTRING ({first_point_lat} {first_point_lon}, {second_point_lat} {second_point_long})'`: This part of the statement creates a rectangular bounding box (envelope) that covers the given line represented by a LINESTRING. The two pairs of coordinates in the LINESTRING define the origin and destination of the trip.

2. `ST_MakeLine(origin_coord, destination_coord)`: This part of the statement creates a line (trip) from two sets of coordinates, 'origin_coord' and 'destination_coord', representing the starting and ending points of the trip.

3. `ST_Contains()`: This function checks if the first geometry (the envelope) contains the second geometry (the trip). In this context, it checks if the rectangular bounding box contains the entire line representing the trip.

By using `ST_Contains` in combination with `ST_Envelope` and `ST_MakeLine`, the application can efficiently identify which trips fall within a specific region defined by a rectangular bounding box. This allows users to retrieve weekly average data for trips that are entirely within a given region, helping to analyze trips within specific geographic boundaries.

Another example is to calculate how close 2 trips are from each other [Query](https://github.com/LucasManzatto/upload_api/blob/main/app/queries/postgres/scripts/similar_trips.sql)

```sql
ST_DISTANCE(LAG(origin_coord::geography) OVER(ORDER BY region, origin_coord DESC), origin_coord::geography) AS origin_distance_to_closest
```
This is an example SQL query that calculates the distance from each row's origin_coord to the closest origin_coord in the previous row, based on the region and sorted by origin_coord in descending order.

Query Explanation
The query uses the ST_DISTANCE function along with the LAG window function to calculate the distance between each origin_coord and the closest previous origin_coord within the same region.

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


## Results

**1. Upload endpoint**

It took 54min42s to upload and insert 55.440.000 million rows into the database. It was not possible to insert more rows because my laptop can't handle, but the endpoint and the queries can handle 100 millions rows just fine.

![image](https://github.com/LucasManzatto/upload_api/assets/12992999/c6b99af3-ee80-40f2-9863-96f10f04f518)

![image](https://github.com/LucasManzatto/upload_api/assets/12992999/da373dfb-bdce-4e8d-b516-7c032321a3ef)

**2. Weekly average endpoint**

Using region takes about 12 seconds

![image](https://github.com/LucasManzatto/upload_api/assets/12992999/fa1453e5-9941-4baf-97a7-ce598aea8302)

Using a bounding box takes about 20 seconds

![image](https://github.com/LucasManzatto/upload_api/assets/12992999/52fa0732-a974-4a28-8661-917a4084783e)

**3. Bonus queries**

The [Query](https://github.com/LucasManzatto/upload_api/blob/main/app/queries/postgres/scripts/latest_datasource_from_common_regions.sql) From the two most commonly appearing regions, which is the latest datasource? took 1min2s to complete
![image](https://github.com/LucasManzatto/upload_api/assets/12992999/28d108d2-1907-4e21-a923-8f4b44b664b4)

The [Query](https://github.com/LucasManzatto/upload_api/blob/main/app/queries/postgres/scripts/datasource_in_regions.sql) What regions has the "cheap_mobile" datasource appeared in? took 23s to complete
![image](https://github.com/LucasManzatto/upload_api/assets/12992999/8eb390e2-0e4d-48d9-bb77-6c006a905d1a)


## Cloud Solution

![Blank diagram - Page 1 (1)](https://github.com/LucasManzatto/upload_api/assets/12992999/1867eafa-c4e2-4cc4-8ff3-8a41545ab9e2)
