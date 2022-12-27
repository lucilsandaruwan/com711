# This file contains the functions related to data base queries regarding products
from model import db_connector
def list_by_cat_id(category_id):
    """This is to get rquired fields from products using category_id. This function can be extended by appending fields but don't-
    change the order of existing fields in select query.
        Args:
            category_id(string): this is the category_id taken from the user
        Returns: 
            list: the list contains an array for the selected fields for each row.
    """
    con = db_connector.get_connection()
    cursor = con.cursor()
    query = "SELECT product_id, product_description FROM products WHERE category_id = ?"
    cursor.execute(query, (category_id,))
    ret = cursor.fetchall()
    con.close()
    return ret

def list_p_sellers_by_id(product_id):
    """This is to get rquired fields from product_sellers using product_id. This function can be extended by appending fields but don't-
    change the order of existing fields in select query.
        Args:
            product_id(string): this is the product_id taken from the user
        Returns: 
            list: the list contains an array for the selected fields for each row.
    """
    con = db_connector.get_connection()
    cursor = con.cursor()
    query = """
                SELECT 
                    ps.seller_id
                    ,ps.price
                    ,s.seller_name
                    ,ps.product_id
                FROM product_sellers AS ps
                    JOIN sellers AS s
                        ON ps.seller_id = s.seller_id
                WHERE ps.product_id = ?
            """
    cursor.execute(query, (product_id,))
    ret = cursor.fetchall()
    con.close()
    return ret

