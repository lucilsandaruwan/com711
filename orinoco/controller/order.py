from model import order as o_mdl
from model import basket as b_mdl
from controller import basket as b_cntrl
from view import table
from view import options_list as ol
from view import validated_input as vi
from view import str_format as sf 

def order_history(shopper):
    
    orders = o_mdl.get_by_shopper_id(shopper["shopper_id"])
    v_orders = orders[0:7]
    headers = (
        {"length": 10, "lable": "Order ID"}
        ,{"length": 15, "lable": "Order Date"}
        ,{"length": 70, "lable": "Product Description"}
        ,{"length": 20, "lable": "Seller"}
        ,{"length": 10, "lable": "Price"}
        ,{"length": 8, "lable": "Qty"}
        ,{"length": 8, "lable": "Status"}
    )
    # print(orders)
    table.dinamic_table("Order History", headers, v_orders)

def get_delivery_address(shopper_id):
    d_addresses = o_mdl.get_shopper_delevery_addresses(shopper_id)
    print(d_addresses)
    if len(d_addresses) > 0:
        d_add_2_show = list(
            map(
                lambda x: (
                    x[0], ', '.join(
                        filter(None,x[1:6])
                    )
                ), d_addresses
            )
        )
        d_add_id = ol._display_options(d_add_2_show, "Delivery Addresses", "delivery address")
        return d_add_id
    else:
        return None

def get_card(shopper_id):
    cards = o_mdl.get_cards(shopper_id)
    lngth = len(cards)
    if lngth == 1:
        return cards[0][0]
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
    else:
        return None

def create_address():
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
    ret = {}
    print("\nAs you have not yet placed any orders, you will need to enter your payment card details")
    ret["c_type"] = vi.defined_values(
        "Enter the card type (Visa, Mastercard or AMEX): "
        ,("Visa", "Mastercard", "AMEX")
        ,True
    )
    ret["c_number"] = vi.fix_length_number("Enter the 16-digit card number: ", 16, True)
    return ret

def checkout(shopper):
    shopper_id = shopper["shopper_id"]
    basket = b_mdl.get_by_shopper(shopper_id)
    if(len(basket) == 0):
        print(sf.warning("There are no products in basket to checkout"))
        return
    b_cntrl.view_basket(shopper)

    d_add_id = get_delivery_address(shopper_id)
    card_id = get_card(shopper_id)

    params = {
        "shopper_id": shopper_id
        ,"basket": basket
        ,"d_add_id": d_add_id
        ,"card_id": card_id
        ,"d_address": {}
        ,"card": {}
    }

    if d_add_id == None:
       params["d_address"] = create_address()

    # ----------------
    # payment mthd
    

    if card_id == None:
        params["card"] = create_card()

    
    ret = o_mdl.creae_order(params)
    print(params)
    if ret:
        print(sf.sucess("Checkout complete, your order has been placed"))
    else:
        print(sf.error("Please try again"))

