/*"Which areas have the highest average rental income?"*/

SELECT L.neighbourhood_group, AVG(C.price) AS average_rental_income
FROM Listings L
JOIN Calendar C ON L.id = C.listing_id
GROUP BY L.neighbourhood_group
ORDER BY average_rental_income DESC;

/*"What are the occupancy rates across different areas?"*/

SELECT L.neighbourhood_group, SUM(CASE WHEN C.available = false THEN 1 ELSE 0 END) / COUNT(C.date) * 100 AS occupancy_rate
FROM Listings L
JOIN Calendar C ON L.id = C.listing_id
GROUP BY L.neighbourhood_group
ORDER BY occupancy_rate DESC;

/*"What amenities are most often referenced in good reviews?"*/

SELECT
    COUNT(CASE WHEN R.comments LIKE '%Wi-Fi%' THEN 1 END) AS wifi_mentions,
    COUNT(CASE WHEN R.comments LIKE '%pool%' THEN 1 END) AS pool_mentions,
    COUNT(CASE WHEN R.comments LIKE '%parking%' THEN 1 END) AS parking_mentions,
    COUNT(CASE WHEN R.comments LIKE '%air conditioning%' THEN 1 END) AS ac_mentions,
    COUNT(CASE WHEN R.comments LIKE '%balcony%' THEN 1 END) AS balcony_mentions
FROM Reviews R
WHERE
    R.comments LIKE '%great%'
    OR R.comments LIKE '%excellent%'
    OR R.comments LIKE '%amazing%'
    OR R.comments LIKE '%comfortable%'
    OR R.comments LIKE '%clean%';

/*"What seasonal trends affect rental income?"*/

SELECT
    CASE
        WHEN EXTRACT(MONTH FROM C.date) IN (12, 1, 2) THEN 'Summer'
        WHEN EXTRACT(MONTH FROM C.date) IN (3, 4, 5) THEN 'Autumn'
        WHEN EXTRACT(MONTH FROM C.date) IN (6, 7, 8) THEN 'Winter'
        WHEN EXTRACT(MONTH FROM C.date) IN (9, 10, 11) THEN 'Spring'
    END AS season,
    AVG(C.price) AS average_rental_income,
    SUM(CASE WHEN C.available = false THEN 1 ELSE 0 END) / COUNT(C.date) * 100 AS occupancy_rate
FROM Calendar C
JOIN Listings L ON C.listing_id = L.id
GROUP BY season
ORDER BY season;

/*"What room type on average rates higher from reviews?"*/

SELECT L.room_type, COUNT(R.id) AS positive_review_count
FROM Reviews R
JOIN Listings L ON R.listing_id = L.id
WHERE
    R.comments LIKE '%great%'
    OR R.comments LIKE '%excellent%'
    OR R.comments LIKE '%amazing%'
    OR R.comments LIKE '%comfortable%'
    OR R.comments LIKE '%clean%'
GROUP BY L.room_type
ORDER BY positive_review_count DESC;
