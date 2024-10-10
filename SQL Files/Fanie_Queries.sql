-- //2. Which areas have the most frequent bookings?

SELECT 
    `neighbourhood_group`,
    COUNT(`listing_id`) AS total_listings,
    ROUND(SUM(`reviews_per_month`), 2) AS total_reviews_per_month,
    ROUND(AVG(`reviews_per_month`), 2) AS avg_reviews_per_listing,
    ROUND(AVG(`availability_365`), 2) AS avg_availability_365
FROM 
    `datadwarves`.`listings`
WHERE 
    `availability_365` < 365 -- Only include listings that are not fully available
GROUP BY 
    `neighbourhood_group`
ORDER BY 
    avg_availability_365 ASC;


-- //4. What amenities do the highest rated properties provide?
-- //We have no amenities column (I swear it was in the data?)

-- //6. Are there any areas that meet the criteria to be good but have few Airbnb listings?
SELECT 
    neighbourhood_group,
    COUNT(listing_id) AS total_listings,
    ROUND(AVG(reviews_per_month), 2) AS avg_reviews_per_listing,
    ROUND(AVG(availability_365),2) AS avg_availability_365
FROM 
    `datadwarves`.`listings`
GROUP BY 
    neighbourhood_group
HAVING 
    avg(reviews_per_month) > 1
    AND COUNT(listing_id) < 10 
ORDER BY 
    avg_reviews_per_listing DESC;

-- 8. What room type has more frequent bookings?
SELECT 
    room_type,
    COUNT(listing_id) AS total_listings,
    ROUND(SUM(number_of_reviews), 2) AS total_reviews,
    ROUND(AVG(reviews_per_month), 2) AS avg_reviews_per_month,
    ROUND(SUM(365 - availability_365), 2) AS total_bookings,
    ROUND(AVG(365 - availability_365), 2) AS bookings_per_listing
FROM 
    `datadwarves`.`listings`
GROUP BY 
    room_type
ORDER BY 
    total_bookings DESC;









