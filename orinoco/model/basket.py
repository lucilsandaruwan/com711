# this file contains db connection related functions relevent to basket and basket items

from model import db_connector
from view import str_format as sf
import sqlite3

def create_basket(shopper_id, product):
    """This should be called to create new basket when a basket is not available for user.
        Args:
            shopper_id(string): the shopper_id field of shoppers table should be passed as this argument
            product(dictionary): this should have product_id, seller_id, quantity and price to store in basket contents table
        Returns: 
            bool: it returns True if the basket creation is completed successfully. Otherwise, it returns False
    """
    con = db_connector.get_connection()
    cursor = con.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")  
    cursor.execute("BEGIN TRANSACTION")	   
    try:
        # used this query to create bucket and get primary key in the same query to avoid exceptions using same bucket id in two requests.    
        q_add_basket = """
                INSERT INTO shopper_baskets(basket_id,shopper_id,basket_created_date_time) 
                    SELECT IFNULL((SELECT seq + 1 FROM sqlite_sequence WHERE name = "shopper_baskets"  ), 1)
                    ,?
                    ,datetime('now')
                WHERE NOT EXISTS(SELECT 1 FROM shopper_baskets WHERE shopper_id = ?);
            """
        cursor.execute(
            q_add_basket
            , (
                shopper_id
                , shopper_id
            )
        )
        # Used this query to read basket_id and insert product in the same query
        q_add_item = """
                INSERT INTO basket_contents(basket_id,product_id,seller_id,quantity,price) 
                    SELECT ( SELECT MAX(basket_id) FROM shopper_baskets WHERE shopper_id = ? )
                    ,?
                    ,?
                    ,?
                    ,?;
            """
       
        cursor.execute(q_add_item, (
            shopper_id
            ,product["product_id"] 
            ,product["seller_id"] 
            ,product["quantity"] 
            ,product["price"]
        ))

        cursor.execute("COMMIT")     
        con.close()                  
        return True
    except sqlite3.IntegrityError as err: 
        # this exception will not trigger for normal scenarios as it is handled in the controller.
        if err.args == ('UNIQUE constraint failed: basket_contents.basket_id, basket_contents.product_id',):
            print(sf.warning("\nThe product has been added from a different seller. So, please try to buy it from the same seller"))
            return False
    except:				 
        print(sf.warning("\nTransaction failed, rolling back"))
        cursor.execute("ROLLBACK")	
        con.close()
        return False

def update_basket_content(product):
    """This is to update basket contents when there is basket_id and product_id. If there is a new item with same product id to the 
       basket, it updates the quantity and price from controller by calling this function.
            Args:
                product(dictionary): the dictionry objecgt should have following elements
                    1. quantity
                    2. price
                    3. basket_id
                    4. product_id
            Returns:
                bool: True if success False for any failier
    """
    con = db_connector.get_connection()
    cursor = con.cursor()
    cursor.execute("PRAGMA foreign_keys=ON") 
    try:
        query = """
            UPDATE basket_contents
                SET quantity = ?,
                price = ? 
            WHERE basket_id = ?
                AND product_id = ?
                    ;
        """
        cursor.execute(query, (product["quantity"], product["price"], product["basket_id"], product["product_id"]))
        cursor.execute("COMMIT")
        con.close()
        return True
    except:
        con.close()
        return False

def create_basket_content(product):
    """This is used to create basket content if the basket_id is available.
            Args:
                product(dictionary): this is a dictionary having following elements
                    1. quantity
                    2. price
                    3. basket_id
                    4. product_id 
            Returns:
                bool: True if success False for any failier
    """
    con = db_connector.get_connection()
    cursor = con.cursor()
    cursor.execute("PRAGMA foreign_keys=ON") 
    try:
        query = """
                INSERT INTO basket_contents(basket_id,product_id,seller_id,quantity,price) 
                    SELECT ?
                    ,?
                    ,?
                    ,?
                    ,?;
            """
        cursor.execute(query, (
            product["basket_id"]
            , product["product_id"]
            , product["seller_id"]
            , product["quantity"]
            , product["price"]
            
        ))
        cursor.execute("COMMIT")
        con.close()
        return True
    except:
        con.close()
        return False

def get_by_shopper(shopper_id):
    """This query is used in both order and basket controllers to get basket items from shopper_id.
        So, this function returns a dictionary objects list as result to avoid index issues when adding new fields to fetch query
        Args:
            shopper_id(string): this is the shopper_id taking from user.
        Returns(list): this is a list of dictionaries having all selected fields as keys and values as dictionary values.
    """
    con = db_connector.get_dict_connection()
    cursor = con.cursor()
    query = """
        SELECT p.product_description
        ,s.seller_name
        ,SUM(bc.quantity) AS quantity
        ,PRINTF("£%.2f", bc.price) AS formatted_price
        ,price
        ,SUM(bc.quantity * bc.price) AS total
        ,sb.basket_id
        ,bc.product_id
        ,bc.seller_id
        FROM (
            SELECT * FROM shopper_baskets WHERE shopper_id = ?
        )AS sb
        JOIN basket_contents as bc
            ON sb.basket_id = bc.basket_id
        JOIN products AS p
            ON bc.product_id = p.product_id
        JOIN sellers AS s
            ON bc.seller_id = s.seller_id
        GROUP BY p.product_description
        ,s.seller_name
        ,bc.price
    """
    cursor.execute(query, (shopper_id,))
    return cursor.fetchall()

