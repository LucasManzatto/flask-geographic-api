SELECT region,
       count(*) total_cheap_mobile
FROM trips
WHERE datasource = 'cheap_mobile'
GROUP BY region