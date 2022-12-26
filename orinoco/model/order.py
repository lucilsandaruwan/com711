from operator import itemgetter
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

def get_shopper_delevery_addresses(shopper_id):
    con = db_connector.get_connection()
    cursor = con.cursor()
    query = """
        SELECT DISTINCT sda.delivery_address_id
            ,delivery_address_line_1
            ,delivery_address_line_2
            ,delivery_address_line_3
            ,delivery_county
            ,delivery_post_code
        FROM (
            SELECT * 
            FROM shopper_orders 
            WHERE shopper_id = ? 
        ) AS so
        JOIN shopper_delivery_addresses AS sda
            ON so.delivery_address_id = sda.delivery_address_id
        ORDER BY order_id DESC
    """
    cursor.execute(query, (shopper_id,))
    ret = cursor.fetchall()
    con.close()
    return ret

def get_cards(shopper_id):
    con = db_connector.get_connection()
    cursor = con.cursor()
    query = """
        SELECT DISTINCT spc.payment_card_id
            ,card_type
            ,card_number
        FROM (
            SELECT * 
            FROM shopper_orders 
            WHERE shopper_id = ? 
        ) AS so
        JOIN shopper_payment_cards AS spc
            ON so.payment_card_id = spc.payment_card_id
        ORDER BY order_id DESC
    """
    cursor.execute(query, (shopper_id,))
    ret = cursor.fetchall()
    con.close()
    return ret

def get_sequence_number(table_name):
    con = db_connector.get_connection()
    cursor = con.cursor()
    query = "SELECT IFNULL((SELECT seq + 1 FROM sqlite_sequence WHERE name = \"{}\"  ), 1)".format(table_name)
    cursor.execute(query)
    ret = cursor.fetchone()
    con.close()
    return ret[0]


def creae_order(params):
    con = db_connector.get_connection()
    cursor = con.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")  # Enforce foreign keys
    cursor.execute("BEGIN TRANSACTION")	

    shopper_id, basket, d_add_id, card_id, d_address, card = itemgetter(
        'shopper_id', 'basket', 'd_add_id', 'card_id', 'd_address', 'card'
    )(params)
    try:
        # create a delivery address when the address id is None
        if d_add_id == None:
            add_line_1, add_line_2, add_line_3, country, post_code = itemgetter(
                'add_line_1', 'add_line_2', 'add_line_3', 'country', 'post_code'
            )(d_address)
            d_add_id = get_sequence_number("shopper_delivery_addresses")
            add_q = """INSERT INTO shopper_delivery_addresses(
                            delivery_address_id
                            ,delivery_address_line_1
                            ,delivery_address_line_2
                            ,delivery_address_line_3
                            ,delivery_county
                            ,delivery_post_code
                        ) 
                    VALUES(
                        ?,?,?,?,?,?
                    );"""
            cursor.execute(add_q, (
                d_add_id
                ,add_line_1
                ,add_line_2
                ,add_line_3
                ,country
                ,post_code
            ))
        # Create a card when the card id is none
        if card_id == None:
            card_id = get_sequence_number("shopper_payment_cards") 
            c_type, c_number = itemgetter(
                'c_type', 'c_number'
            )(card)  
            card_q = """INSERT INTO shopper_payment_cards(
                        payment_card_id
                        ,card_type
                        ,card_number
                    ) 
                    VALUES(
                        ?,?,?
                    );"""
            cursor.execute(card_q, (
                card_id
                ,c_type
                ,c_number
            ))
        # Create order
        order_id = get_sequence_number("shopper_orders")
        order_q = """ INSERT INTO shopper_orders(
            order_id, shopper_id, delivery_address_id, payment_card_id, order_date, order_status
        )
        VALUES(
            ?, ?, ?, ?, DATE(), "Placed"
        );"""
        cursor.execute(order_q, (
            order_id
            ,shopper_id
            ,d_add_id
            ,card_id
        ))
        # add order product
        ord_prod_q = """
            INSERT INTO ordered_products(
                order_id
                ,product_id
                ,seller_id
                ,quantity
                ,price
                ,ordered_product_status
            )
            VALUES(
                ?,?,?,?,?,"Placed"
            );
        """
        basket_id = 0
        for i in basket:
            cursor.execute(ord_prod_q, (
                order_id
                ,i["product_id"]
                ,i["seller_id"]
                ,i["quantity"]
                ,i["price"]
            ))
            basket_id = i["basket_id"]

        # Delete basket contents
        del_bskt_conts_q = """DELETE FROM basket_contents WHERE basket_id = ?;"""
        cursor.execute(del_bskt_conts_q, (basket_id,))

        # Delete basket
        del_bskt_q = "DELETE FROM shopper_baskets WHERE basket_id = ?;"
        cursor.execute(del_bskt_q, (basket_id,))

        cursor.execute("COMMIT")
        con.close()
        return True

    except:
        print("Transaction failed, rolling back")
        cursor.execute("ROLLBACK")	
        con.close()
        return False

    