WITH cte1 AS
  (SELECT *,
          ST_DISTANCE(LAG(origin_coord::geography) OVER(
                                                        ORDER BY region, origin_coord DESC), origin_coord::geography) AS origin_distance_to_closest,
          ST_DISTANCE(LAG(destination_coord::geography) OVER(
                                                             ORDER BY region, origin_coord DESC), destination_coord::geography) AS destination_distance_to_closest,
          EXTRACT(EPOCH
                  FROM (LAG(datetime) OVER(
                                           ORDER BY region, origin_coord DESC) - datetime)) AS datetime_diff
   FROM trips)
SELECT *,
       CASE
           WHEN datetime_diff < 1800
                AND datetime_diff > -1800
                AND origin_distance_to_closest < 3000
                AND destination_distance_to_closest < 3000 THEN 1
           ELSE 0
       END AS is_similar
FROM cte1
ORDER BY region,
         origin_coord DESC