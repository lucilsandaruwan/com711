# This file contains the functions related to data base queries regarding orders
from operator import itemgetter
from model import db_connector
def get_by_shopper_id(shopper_id):
    """This is to get orders and rquired fields using shopper_id. This function can be extended by appending fields but don't-
    change the order of existing fields in select query.
        Args:
            shopper_id(string): this is the shopper_id taken from the user
        Returns: 
            list: the list contains an array for the selected fields for each row.
    """
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
    """This is to get delivery address and rquired fields using shopper_id. This function can be extended by appending fields but don't-
    change the order of existing fields in select query.
        Args:
            shopper_id(string): this is the shopper_id taken from the user
        Returns: 
            list: the list contains an array for the selected fields for each row.
    """
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
    """This is to get payment card and rquired fields using shopper_id. This function can be extended by appending fields but don't-
    change the order of existing fields in select query.
        Args:
            shopper_id(string): this is the shopper_id taken from the user
        Returns: 
            list: the list contains an array for the selected fields for each row.
    """
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

def creae_order(params):
    """This is handling few functionalities regarding order creation in transaction
            1. create delivery address if it is not available
            2. create payent card if it is not available
            3. Create shopper order
            4. Create shoper orders contents for each product in the basket contents
            5. Delete basket contents for the shopper
            6. Delete basket record for the shopper
        Args:
            params(dictionary): this object should have values as follows
                shopper_id(string): considering shopper id
                basket(list): this should be a list of basket items having following filelds
                    product_id(string): the product id from products table
                    seller_id(string): the seller id of the product
                    quantity(integer): the added quantity of the product
                    price(float): the unit price of the product
                d_add_id(string): the delivery address id from the table if shopper has a selected delivery address
                card_id(string): the payment card id from the table if shopper has a selected card
                d_address(dictinary): a dictionary object if shopper need to create a new delivery address with following elements
                    add_line_1(string): the values taken from user
                    add_line_2(string): the values taken from user
                    add_line_3(string): the values taken from user
                    country(string): the values taken from user
                    post_code(string): the values taken from user
                card(dictionary): a dictionary object having following elements when it is required to create new address
                    c_type(string): user entered card type
                    c_number(string): use entered card id having 16 digits
        Returns:
            bool: True if successfuly create the order or False if any exception.

    """
    con = db_connector.get_connection()
    cursor = con.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")  # Enforce foreign keys
    cursor.execute("BEGIN TRANSACTION")	
    # extract elements into variables from dictionary
    shopper_id, basket, d_add_id, card_id, d_address, card = itemgetter(
        'shopper_id', 'basket', 'd_add_id', 'card_id', 'd_address', 'card'
    )(params)
    try:
        # create a delivery address when the address id is None
        if d_add_id == None:
            add_line_1, add_line_2, add_line_3, country, post_code = itemgetter(
                'add_line_1', 'add_line_2', 'add_line_3', 'country', 'post_code'
            )(d_address)
            d_add_id = db_connector.get_sequence_number("shopper_delivery_addresses")
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
            card_id = db_connector.get_sequence_number("shopper_payment_cards") 
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
        order_id = db_connector.get_sequence_number("shopper_orders")
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

    