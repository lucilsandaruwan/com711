# this file is created to manage order related requests.
from model import order as o_mdl
from model import basket as b_mdl
from controller import basket as b_cntrl
from view import table
from view import options_list as ol
from view import validated_input as vi
from view import str_format as sf 

def order_history(shopper_id):
    """"This is to get data from model to list all orders from the user and process to show them
        Args:
            shoppper_id(string): the shopper_id of the user
        Returns: void
    """
    orders = o_mdl.get_by_shopper_id(shopper_id)
    # get only the first 6 selected fields from the model to display
    v_orders = orders[0:7]
    # setting headers with the width of each column to show in the table
    headers = (
        {"length": 10, "lable": "Order ID"}
        ,{"length": 15, "lable": "Order Date"}
        ,{"length": 70, "lable": "Product Description"}
        ,{"length": 20, "lable": "Seller"}
        ,{"length": 10, "lable": "Price"}
        ,{"length": 8, "lable": "Qty"}
        ,{"length": 8, "lable": "Status"}
    )

    table.dinamic_table("Order History", headers, v_orders)

def get_delivery_address(shopper_id):
    """This is to get existing delivery address from data base.
        this has three scenarios
            1. There is only one record in db: this time it returns the delivery address id from the table
            2. There are more than one address: for this case, 
                    it prompt user to select one address and pass the id of that to calling function
            3. There is no any address for the shopper: function returns none for this
        Args:
            shopper_id(string): shopper_id taken from the user
        Returns:
            delivery_address_id(string) / None: returns delivery address id if it is exists or None if it is not exist
    """
    d_addresses = o_mdl.get_shopper_delevery_addresses(shopper_id)
    add_lngth = len(d_addresses)
    # scenario one
    if add_lngth == 1:
        return d_addresses[0][0]
    # scenario two
    elif add_lngth > 1:
        d_add_2_show = list(
            map(
                lambda x: (
                    x[0], ', '.join(
                        filter(None,x[1:6])
                    )
                ), d_addresses
            )
        )
        return ol._display_options(d_add_2_show, "Delivery Addresses", "delivery address")
    # scenario three
    else:
        return None

def get_card(shopper_id):
    """This is to get existing card details from data base.
        this has three scenarios
            1. There is only one record in db: this time it returns the card id from the table
            2. There are more than one address: for this case, 
                    it prompt user to select one card and pass the id of that to calling function
            3. There is no any card for the shopper: function returns none for this
        Args:
            shopper_od(string): shopper_id taken from the user
        Returns:
            payment_card_id(string) / None: returns payment card id if it is exists or None if it is not exist
    """
    cards = o_mdl.get_cards(shopper_id)
    lngth = len(cards)
    # case one
    if lngth == 1:
        return cards[0][0]
    # case two
    elif lngth > 0:
        c_2_show = list(
            map(
                lambda x: (
                    x[0], ' ending in '.join(
                        filter(None,x[1:3])
                    )
                ), cards
            )
        )
        return ol._display_options(c_2_show, "Payments Cards", "payment card")
    # case three
    else:
        return None

def create_address():
    """This is to collect component of address from the user
        Returns:
            ret(dictionary): this object has all the required field to add into delivery address table
    """
    ret = {}
    print("\nAs you have not yet placed any orders, you will need to enter a delivery address")
    add_line = "Enter the delivery address line {}: "
    ret["add_line_1"] = vi.mandatory(add_line.format(1))
    ret["add_line_2"] = vi.mandatory(add_line.format(2))
    ret["add_line_3"] = input(add_line.format(3))
    ret["country"] = vi.mandatory("Enter the delivery country: ")
    ret["post_code"] = vi.mandatory("Enter the delivery post code: ")
    return ret

def create_card():
    """This is to collect component of payment card from the user
        Returns:
            ret(dictionary): this object has all the required field to add into payment cards table
    """
    ret = {}
    print("\nAs you have not yet placed any orders, you will need to enter your payment card details")
    ret["c_type"] = vi.defined_values(
        "Enter the card type (Visa, Mastercard or AMEX): "
        ,("Visa", "Mastercard", "AMEX")
        ,True
    )
    ret["c_number"] = vi.fix_length_number("Enter the 16-digit card number: ", 16, True)
    return ret

def checkout(shopper_id):
    """This is to handle checkout request from the menue item. it does few things relevent checkout
        1. create delivery address if it is not created before
        2. get card details if the card is not created
        3. created order and order products.
    """
    # check the products are available in the basket to checout.
    basket = b_mdl.get_by_shopper(shopper_id)
    if(len(basket) == 0):
        print(sf.warning("There are no products in basket to checkout"))
        return
    # show the existing producs in the basket to checkout
    b_cntrl.view_basket(shopper_id)

    # get user confirmatin to do checkout
    confirm = input("Enter {} to continue or any other key to exit: ".format(sf.blue("1")))
    if confirm != "1":
        return

    
    d_add_id = get_delivery_address(shopper_id)
    card_id = get_card(shopper_id)
    # the object to pass to order model to create checkout
    params = {
        "shopper_id": shopper_id
        ,"basket": basket
        ,"d_add_id": d_add_id
        ,"card_id": card_id
        ,"d_address": {}
        ,"card": {}
    }

    # if thre is no delivery address for the shoper, it calls address create handler to collect address information and pass it-
    # to the argument object
    if d_add_id == None:
       params["d_address"] = create_address()

    # if the payment card details of shopper is empty it calls the card create handler to collect card details and pass it to the argument object
    if card_id == None:
        params["card"] = create_card()

    
    ret = o_mdl.creae_order(params)
    if ret:
        print(sf.sucess("Checkout complete, your order has been placed"))
    else:
        print(sf.error("Please try again"))

