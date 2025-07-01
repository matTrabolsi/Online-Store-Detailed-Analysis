SELECT
    ReviewID,
    CustomerID,
    ProductID,
    ReviewDate,
    Rating,

    REPLACE(ReviewText, '  ', ' ') AS ReviewText  -- Cleans up the ReviewText by replacing double spaces with single spaces
FROM
    dbo.customer_reviews; 