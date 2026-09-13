select * from amazon_sales;

SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'amazon_sales'
AND column_name IN ('Date', 'Amount', 'Qty');

ALTER TABLE amazon_sales
ALTER COLUMN "Date" TYPE DATE
USING TO_DATE("Date", 'MM-DD-YY');

select count(*) - count("order_id") as null_order_ids from amazon_sales;

select count(*) - count("Amount") as null_amount from amazon_sales;

select count(*) - count("ship-state") as null_states from amazon_sales;

select count(*) as duplicate_rows 
from(
select *,count(*) over (
partition by "order_id","Date","Amount"
) as cnt
from amazon_sales
)t
where cnt>1;

-- Revenue contribution %

SELECT
"Category",
SUM("Amount") AS revenue,
ROUND(
(100.0 * SUM("Amount")/ SUM(SUM("Amount")) OVER ())::numeric,2) AS revenue_percentage
FROM amazon_sales
GROUP BY "Category"
ORDER BY revenue DESC;


-- Order value Segmentation 


with order_value as (
select "order_id",sum("Amount") as order_value
from amazon_sales
group by "order_id"
)
select
case 
when order_value < 500 then 'Low Value'
when order_value <1500 then 'Medium Value'
else 'High Value'
end as order_segment,
count(*) as number_of_orders,
round(avg(order_value):: numeric ,2) as avg_order_value,
round(sum(order_value):: numeric ,2) as total_revenue
from order_value
group by 1
order by total_revenue desc;

-- Revenue concentration 

WITH style_revenue AS (
    SELECT
        "Style",
        SUM("Amount") AS revenue
    FROM amazon_sales
    GROUP BY "Style"
),

ranked AS (SELECT "Style",revenue,SUM(revenue) OVER ( ORDER BY revenue DESC)
AS cumulative_revenue,
SUM(revenue) OVER () AS total_revenue
FROM style_revenue)
SELECT "Style",revenue,ROUND((100.0 * revenue / total_revenue)::numeric,2)
AS revenue_percentage,
ROUND((100.0 * cumulative_revenue / total_revenue)::numeric,2) 
AS cumulative_percentage
FROM ranked
ORDER BY revenue DESC;


-- Data quality score 


SELECT COUNT(*) AS total_rows,COUNT(*) FILTER ( 
WHERE "order_id" IS NULL) AS missing_order_id,
COUNT(*) FILTER (WHERE "Date" IS NULL) AS missing_date,
COUNT(*) FILTER (WHERE "Amount" IS NULL)
AS missing_amount,
COUNT(*) FILTER (WHERE "Qty" IS NULL)
AS missing_quantity,
COUNT(*) FILTER (
WHERE "Qty" <= 0) AS invalid_quantity,
COUNT(*) FILTER (
WHERE "Amount" < 0
) AS invalid_amount
FROM amazon_sales;


--Identify repeat orders 

SELECT "order_id",
COUNT(*) AS line_items,
SUM("Qty") AS total_quantity,
SUM("Amount") AS order_value
FROM amazon_sales
GROUP BY "order_d"
HAVING COUNT(*) > 1
ORDER BY line_items DESC;


-- Month over month revenue growth 

WITH monthly_sales AS 
(SELECT DATE_TRUNC('month',"Date") AS month,
SUM("Amount") AS revenue
FROM amazon_sales
GROUP BY 1
),
monthly_growth AS (
SELECT month, revenue,
LAG(revenue) OVER (ORDER BY month)
AS previous_revenue
FROM monthly_sales)
SELECT month,
ROUND(revenue::numeric, 2) AS revenue,
ROUND(previous_revenue::numeric, 2)
AS previous_revenue,
ROUND((100.0 *(revenue - previous_revenue)/
NULLIF(previous_revenue, 0))::numeric,2)
AS growth_percentage
FROM monthly_growth
ORDER BY month;


-- Analytical View 

CREATE VIEW vw_order_analysis AS

SELECT "order_id",
MIN("Date") AS order_date,

MAX("Status") AS order_status,

MAX("Fulfilment") AS fulfilment,

COUNT(*) AS line_items,

COUNT(DISTINCT "Category") AS category_count,

SUM("Qty") AS total_quantity,

SUM("Amount") AS order_value

FROM amazon_sales

GROUP BY "order_id";

select * from vw_order_analysis;



