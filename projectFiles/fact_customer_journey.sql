-- -- Adding row number Identify Duplicated and how many times the row is duplicated 
-- WITH DuplicatteRecords AS (
--     SELECT
--         JourneyID,
--         CustomerID,
--         ProductID,
--         VisitDate,
--         Stage,
--         Action,
--         Duration,

--         ROW_NUMBER() OVER(
--             PARTITION BY CustomerID, ProductID, VisitDate, Stage, Action

--             ORDER BY JourneyID
--         ) AS row_num
--     FROM
--         dbo.customer_journey
-- )

-- SELECT * 
-- FROM DuplicatteRecords

-- ORDER BY JourneyID


-- selecting final cleaned data after filling missing values with average for each day 
-- and removing duplicates
SELECT
    JourneyID,
    CustomerID,
    ProductID,
    VisitDate,
    Stage,
    Action,
    COALESCE(Duration, avg_duration) AS Duration 
FROM
    (
        SELECT 
            JourneyID,
            CustomerID,
            productID,
            VisitDate,
            UPPER(Stage) AS Stage,
            Action,
            Duration,
            AVG(Duration) OVER (PARTITION BY VisitDate) AS avg_duration,
            ROW_NUMBER() OVER (
                PARTITION BY CustomerID, ProductID, VisitDate, UPPER(Stage), Action
                ORDER BY JourneyID
            ) AS row_num
        FROM
            dbo.customer_journey
    ) AS subquery
WHERE
    row_num = 1;  -- Keeps only the first occurrence of each duplicate group identified in the subquery