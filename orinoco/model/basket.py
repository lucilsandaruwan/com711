from model import db_connector
from view import str_format as sf
import sqlite3

def create_basket(shopper_id, product):
    con = db_connector.get_connection()
    cursor = con.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")  # Enforce foreign keys
    cursor.execute("BEGIN TRANSACTION")	   # Begin a transaction
    try:					   # Start a try block of code
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

        q_add_item = """
                INSERT INTO basket_contents(basket_id,product_id,seller_id,quantity,price) 
                    SELECT ( SELECT MAX(basket_id) FROM shopper_baskets WHERE shopper_id = ? )
                    ,?
                    ,?
                    ,?
                    ,?;
            """
        insert_obj = (shopper_id, product["product_id"] ,product["seller_id"] ,product["quantity"] ,product["price"])
        cursor.execute(q_add_item, insert_obj)

        cursor.execute("COMMIT")     
        con.close()                  
        return True
    except sqlite3.IntegrityError as err:
        if err.args == ('UNIQUE constraint failed: basket_contents.basket_id, basket_contents.product_id',):
            print(sf.warning("\nThe product has been added from a different seller. So, please try to buy it from the same seller"))
            return False
    except:				 
        print(sf.warning("\nTransaction failed, rolling back"))
        cursor.execute("ROLLBACK")	
        con.close()
        return False

def update_basket_content(product):
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
    con = db_connector.get_dict_connection()
    cursor = con.cursor()
    query = """
        SELECT p.product_description
        ,s.seller_name
        ,SUM(bc.quantity) AS quantity
        ,PRINTF("£%.2f", bc.price) AS formatted_price
        ,price
        ,SUM(bc.quantity) * bc.price AS total
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

