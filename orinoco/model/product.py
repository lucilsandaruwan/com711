from model import db_connector
def list_by_cat_id(category_id):
    con = db_connector.get_connection()
    cursor = con.cursor()
    query = "SELECT product_id, product_description FROM products WHERE category_id = ?"
    cursor.execute(query, (category_id,))
    ret = cursor.fetchall()
    con.close()
    return ret

def list_p_sellers_by_id(product_id):
    con = db_connector.get_connection()
    cursor = con.cursor()
    query = """
                SELECT 
                    ps.seller_id
                    ,ps.price
                    ,s.seller_name
                FROM product_sellers AS ps
                    JOIN sellers AS s
                        ON ps.seller_id = s.seller_id
                WHERE ps.product_id = ?
            """
    cursor.execute(query, (product_id,))
    ret = cursor.fetchall()
    con.close()
    return ret