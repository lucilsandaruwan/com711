-- 01
        SELECT shopper_first_name AS [Shopper first name]
            ,shopper_surname AS [Shopper sir name]
            ,shopper_email_address AS [Email address]
            ,IFNULL(gender, "not known") AS Gender
            ,STRFTIME('%d-%m-%Y', date_joined) AS [Date Joined]
            ,CAST(( ( Julianday('now') ) - Julianday(date_of_birth) ) / 365.25 AS INT) AS [Current Age]
        FROM   shoppers
        WHERE  ( 
                    IFNULL(gender, "not known") != "f"
                    AND date_joined >= "2020-01-01" 
                )
                OR ( gender = "f" )
        ORDER  BY gender,
                [current age] DESC

-- 02

        SELECT s.shopper_first_name                AS [Shopper first name],
            s.shopper_surname                   AS [Shopper sir name],
            so.order_id                         AS [Order ID],
            STRFTIME('%d-%m-%Y', so.order_date) AS [Order Date],
            p.product_description               AS [Product description],
            se.seller_name                      AS [Seller Name],
            op.quantity                         AS [Qty ordered],
            PRINTF("�%.2f", op.price)           AS Price,
            op.ordered_product_status           AS [Order Status]
        FROM   shoppers AS s
            LEFT JOIN shopper_orders AS so
                    ON s.shopper_id = so.shopper_id
            LEFT JOIN ordered_products AS op
                    ON so.order_id = op.order_id
            LEFT JOIN products AS p
                    ON op.product_id = p.product_id
            LEFT JOIN sellers AS se
                    ON op.seller_id = se.seller_id
        WHERE  s.shopper_id = @shoper_id
        ORDER  BY order_date DESC 


--03
        
        SELECT s.seller_account_ref AS [Seller Account Ref]
            ,s.seller_name AS [Seller Name]
            ,p.product_code AS [Product Code]
            ,p.product_description AS [Product Description]
            ,COUNT(DISTINCT op.order_id) AS [No. of Orders]
            ,SUM(IFNULL(op.quantity,0)) AS [Total quantity sold]
            ,(
                PRINTF(
                    "£%.2f"
                    ,SUM(IFNULL(op.price, 0) * IFNULL(op.quantity, 0))
                )
            ) AS [Total Value of Sales]
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
            WHERE op.ordered_product_status != "Cancelled" -- ignored the orders which are cancelled
        ) AS op
            ON s.seller_id = op.seller_id
            AND p.product_id = op.product_id
        GROUP BY [Seller Account Ref]
            ,[Seller Name]
            ,[Product Code]
            ,[Product Description]
        ORDER BY [Seller Name], [Product Description]
        ;

        {

                "Seller Account Ref": "OUK00001"
                ,"Seller Name": "DigiTec Limited"
                ,"Product Code": "MP45322289"
                ,"Product Description": "Huawei Y6 32GB 6.09 inch Smartphone"	
                ,"No. of Orders": "5"	
                ,"Total quantity sold": "30"
                ,"Total Value of Sales": "£3225.00"
                
        }
-- test cases

        SELECT *
        FROM products 
        WHERE product_code = "MP45322289";

        SELECT *
        FROM products 
        WHERE product_code = "AU430303";
        


product_id = 3005955

        SELECT * 
        FROM sellers 
        WHERE seller_account_ref = "OUK00001";

-- 200005

        SELECT *
        FROM ordered_products
        WHERE product_id = 3005955
        AND seller_id = 200005

        SELECT *
        FROM shopper_orders
        WHERE order_id in (
            6919012
            ,7102000
            ,7208009
            ,7302005
            ,7417022
        )

-- 5	30	£537.50

        SELECT s.seller_name
            ,s.seller_account_ref
            ,p.product_code
            ,p.product_description
            ,op.*
        FROM ordered_products AS op
        JOIN ( -- joined to remove invalid orders
            SELECT DISTINCT order_id
            FROM shopper_orders
            WHERE order_date >= "2019-06-01"
        ) AS so
        ON op.order_id = so.order_id
        LEFT JOIN sellers AS s
        ON op.seller_id = s.seller_id
        LEFT JOIN products AS p
        ON op.product_id = p.product_id
        WHERE  "p" || op.product_id || "S" || op.seller_id IN (
            SELECT DISTINCT  "p" || product_id || "S" || seller_id
            FROM ordered_products
            WHERE order_id = (
                SELECT order_id
                FROM shopper_orders
                WHERE order_date < "2019-06-01"
                LIMIT 1
            )
        )

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


--CREATE VIEW product_q_and_a AS 
SELECT p.product_id
,p.product_code
,p.product_description
,pr.product_rating_number AS product_rating_avg
,pr.product_rating_stars
,pr.product_rating_lable
,pq.product_question_id
,pq.question
,pq.question_asked_time
,pa.product_answer_id
,answer
,answer_created_time
,(sho.shopper_first_name || " " || shopper_surname) AS answered_shopper
,sho.shopper_id AS answered_shopper_id
,sepa.seller_id AS answered_seller_id
,se.seller_name AS answered_seller_name
,ser.seller_rating_number AS answered_seller_rating_avg
,ser.seller_rating_stars AS answered_seller_rating_stars
,ser.seller_rating_lable AS answered_seller_rating_lable
FROM products AS p
LEFT JOIN (
    SELECT pr.product_id
    ,pr.product_rating_number
    ,rd.rating_stars AS product_rating_stars
    ,rd.rating_lable AS product_rating_lable
    FROM (
        SELECT product_id
        ,ROUND((SUM(CAST( rar.rating_number AS FLOAT))/COUNT(DISTINCT prar.rating_and_review_id)), 0) AS product_rating_number
        FROM product_ratings_and_reviews AS prar
        JOIN ratings_and_reviews rar
            ON prar.rating_and_review_id = rar.rating_and_review_id
        GROUP BY product_id
    ) pr
    JOIN rating_definitions AS rd
    ON pr.product_rating_number = rd.rating_number
) AS pr
ON p.product_id = pr.product_id
LEFT JOIN product_questions AS pq
ON p.product_id = pq.product_id
LEFT JOIN product_answers AS pa
ON pq.product_question_id = pa.product_question_id
LEFT JOIN shopper_product_answers AS spa
ON pa.product_answer_id = spa.product_answer_id
LEFT JOIN shoppers AS sho
ON spa.shopper_id = sho.shopper_id
LEFT JOIN seller_product_answers AS sepa
ON pa.product_answer_id = sepa.product_answer_id
LEFT JOIN sellers AS se
ON sepa.seller_id = se.seller_id
LEFT JOIN (
    SELECT sr.seller_id
    ,sr.seller_rating_number
    ,rd.rating_stars AS seller_rating_stars
    ,rd.rating_lable AS seller_rating_lable
    FROM (
        SELECT seller_id
        ,ROUND((SUM(CAST( rar.rating_number AS FLOAT))/COUNT(DISTINCT srar.rating_and_review_id)), 0) AS seller_rating_number
        FROM seller_ratings_and_reviews AS srar
        JOIN ratings_and_reviews rar
            ON srar.rating_and_review_id = rar.rating_and_review_id
        GROUP BY seller_id
    ) AS sr
    JOIN rating_definitions AS rd
    ON sr.seller_rating_number = rd.rating_number
) AS ser
ON sepa.seller_id = ser.seller_id

--product questions
SELECT DISTINCT product_id
,product_code
,product_description
,product_rating_avg
,product_rating_stars
,product_rating_lable
,product_question_id
,question
,question_asked_time
FROM product_q_and_a
ORDER BY question_asked_time

-- product answers
SELECT product_answer_id
,answer
,answer_created_time
,answered_shopper
,answered_shopper_id
,answered_seller_id
,answered_seller_name
,answered_seller_rating_avg
,answered_seller_rating_stars
,answered_seller_rating_lable
FROM product_q_and_a
WHERE product_question_id = @product_question_id
ORDER BY answer_created_time; 

a)	QUESTION




        SELECT s.seller_account_ref AS [Seller Account Ref]
            ,s.seller_name AS [Seller Name]
            ,p.product_code AS [Product Code]
            ,p.product_description AS [Product Description]
            ,COUNT(DISTINCT op.order_id) AS [No. of Orders]
            ,SUM(IFNULL(op.quantity,0)) AS [Total quantity sold]
            ,(
                PRINTF(
                    "£%.2f"
                    ,SUM(IFNULL(op.price, 0) * IFNULL(op.quantity, 0))
                )
            ) AS [Total Value of Sales]
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
            WHERE op.ordered_product_status != "Cancelled" -- ignored the orders which are cancelled
        ) AS op
            ON s.seller_id = op.seller_id
            AND p.product_id = op.product_id
        GROUP BY [Seller Account Ref]
            ,[Seller Name]
            ,[Product Code]
            ,[Product Description]
        ORDER BY [Seller Name], [Product Description]
        ;

/*

        Seller Account Ref: OUK00001
        Seller Name: DigiTec Limited
        Product Code: MP45322289
        Product Description: Huawei Y6 32GB 6.09 inch Smartphone	
        No. of Orders: 5	
        Total quantity sold: 30	
        Total Value of Sales: £3225.00

*/

        SELECT p.product_description
            ,p.product_code
            ,op.*
        FROM ordered_products AS op
        LEFT JOIN products as p
            ON op.product_id = p.product_id
        WHERE op.product_id IN
        (
            SELECT distinct product_id
            FROM products
            WHERE category_id IN (
                SELECT DISTINCT category_id
                FROM categories
                WHERE category_id IN
                (
                    SELECT category_id
                    FROM products 
                    WHERE product_code = "AU430303"
                )
            )
        )
        AND op.ordered_product_status <> "Cancelled"
        ORDER BY order_id
        