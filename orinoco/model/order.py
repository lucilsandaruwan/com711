from model import db_connector
def get_by_shopper_id(shopper_id):
    con = db_connector.get_connection()
    cursor = con.cursor()
    query = """select so.order_id 
                ,STRFTIME('%d-%m-%Y', so.order_date)  
                ,p.product_description 
                ,se.seller_name 
                ,PRINTF("£%.2f", op.price) 
                ,op.quantity 
                ,op.ordered_product_status 
                from shopper_orders AS so
                left join ordered_products AS op
                    ON so.order_id = op.order_id
                left join products AS p
                    ON op.product_id = p.product_id
                left join sellers AS se
                    ON op.seller_id = se.seller_id
                where so.shopper_id = ?
                order by order_date DESC
            """
    cursor.execute(query, (shopper_id,))
    ret = cursor.fetchall()
    con.close()
    return ret