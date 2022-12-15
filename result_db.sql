-- 01
select shopper_first_name AS [Shopper first name]
    ,shopper_surname AS [Shopper sir name]
    ,shopper_email_address AS [Email address]
    ,ifnull(gender, "Not known") AS Gender
    ,STRFTIME('%d-%m-%Y', date_joined) AS [Date Joined]
    ,CAST(((JulianDay('now')) - JulianDay(date_of_birth))/365.25 AS INT) AS Age
    ,date_of_birth AS dob
    ,strftime('%s', date_joined)
FROM shoppers 
WHERE 
    (
        ifnull(gender, "Not known") != "F" 
        AND strftime('%s', date_joined) >= strftime('%s', "2020-01-01")
    )
    OR (gender = "F")
ORDER BY Gender, Age DESC

-- 02
select s.shopper_first_name AS [Shopper first name]
,s.shopper_surname AS [Shopper sir name]
,so.order_id AS [Order ID]
,STRFTIME('%d-%m-%Y', so.order_date)  AS [Order Date]
,p.product_description AS [Product description]
,se.seller_name AS [Seller Name]
,op.quantity AS [Qty ordered]
,PRINTF("£%.2f", op.price) AS Price
,op.ordered_product_status AS [Order Status]
from shoppers AS s
left join shopper_orders AS so
    ON s.shopper_id = so.shopper_id
left join ordered_products AS op
    ON so.order_id = op.order_id
left join products AS p
    ON op.product_id = p.product_id
left join sellers AS se
    ON op.seller_id = se.seller_id
where s.shopper_id = @shoper_id
order by order_date DESC

--03
SELECT s.seller_account_ref AS [Seller Account Ref]
,s.seller_name AS [Seller Name]
,p.product_code AS [Product Code]
,p.product_description AS [Product Description]
,COUNT(DISTINCT op.order_id) AS [No. of Orders]
,SUM(ifnull(op.quantity,0)) AS [Total quantity sold]
,PRINTF("£%.2f", SUM(ifnull(op.price, 0) * ifnull(op.quantity, 0))) AS [Total Value of Sales]
FROM sellers AS s
JOIN product_sellers AS ps -- removed sellers who does not have products to be sold
    ON s.seller_id = ps.seller_id
LEFT JOIN products AS p
    ON ps.product_id = p.product_id
LEFT JOIN (
    SELECT product_id
    ,seller_id
    ,quantity
    ,price
    ,op.order_id
    FROM ordered_products AS op
    JOIN (
        SELECT order_id
        FROM shopper_orders
        WHERE strftime('%s', order_date) >= strftime('%s', "2019-06-01")
    ) AS so
    ON op.order_id = so.order_id
    WHERE op.ordered_product_status != "Cancelled" -- ignored the orders which is cancelled
) AS op
    ON s.seller_id = op.seller_id
        AND p.product_id = op.product_id
GROUP BY [Seller Account Ref]
    ,[Seller Name]
    ,[Product Code]
    ,[Product Description]
ORDER BY [Seller Name], [Product Description]
;

-- test cases
select *
from products 
where product_code = "MP45322289";

--3007679
--3005955

select * from sellers 
where seller_account_ref = "OUK00001";

-- 200010
-- 200005

select *
from ordered_products
where product_id = 3005955
and seller_id = 200005


-- 5	30	£537.50

--04

WITH op AS (
    SELECT * FROM ordered_products
    WHERE ordered_product_status != "Cancelled"
),
pc AS (
    SELECT p.product_code
    ,p.product_description
    ,p.category_id
    ,c.category_description
    ,CAST(IFNULL(op.quantity, 0) AS REAL) AS quantity
    ,order_id
    FROM products AS p
    LEFT JOIN op
        ON p.product_id = op.product_id
    LEFT JOIN categories AS c
        ON p.category_id = c.category_id
),
p AS (
    SELECT product_code
    ,product_description
    ,category_id
    ,SUM(quantity)/COUNT(DISTINCT order_id) AS avg
    FROM pc
    GROUP BY product_code
    ,product_description
    ,category_id
)
,c AS (
    SELECT category_id
    ,category_description
    ,SUM(quantity)/COUNT(DISTINCT order_id) AS avg
    FROM pc
    GROUP BY category_id, category_description
)
SELECT c.category_description AS [Category Description]
,p.product_code AS [Product Code]
,p.product_description AS [Product Description]
,PRINTF("%.2f", p.avg) AS [Avg Qty Sold]
,PRINTF("%.2f", c.avg) AS [Avg Qty Sold for Category]
FROM p
JOIN c
    ON p.category_id = c.category_id
    AND IFNULL(p.avg, 0) < c.avg
ORDER BY [Category Description], [Product Description]
;