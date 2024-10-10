-- //2. Which areas have the most frequent bookings?

SELECT 
    `neighbourhood_group`,
    COUNT(`listing_id`) AS total_listings,
    SUM(`reviews_per_month`) AS total_reviews_per_month,
    AVG(`reviews_per_month`) AS avg_reviews_per_listing,
    AVG(`availability_365`) AS avg_availability_365
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
    avg(reviews_per_month) AS avg_reviews_per_listing,
    AVG(availability_365) AS avg_availability_365
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
    SUM(number_of_reviews) AS total_reviews,
    AVG(reviews_per_month) AS avg_reviews_per_month,
    SUM((365-availability_365)) AS total_bookings,
    AVG(365-availability_365) AS Bookings_Per_Listing
FROM 
    `datadwarves`.`listings`
GROUP BY 
    room_type
ORDER BY 
    total_bookings DESC;








