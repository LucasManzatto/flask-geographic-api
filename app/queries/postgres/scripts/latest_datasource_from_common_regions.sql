WITH cte1 AS
  (SELECT count(*) AS total_trips,
          region,
          max(datetime) AS latest_datetime
   FROM trips
   GROUP BY region
   ORDER BY total_trips DESC
   LIMIT 2)
SELECT DISTINCT c.total_trips,
                c.region,
                t.datasource
FROM cte1 c
JOIN trips t ON c.region = t.region
WHERE c.latest_datetime = t.datetime