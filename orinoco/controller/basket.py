# This file contains basket related handlers and functions 
# and some functions of this file is depending on the functools library

from model import category
from model import product as p
from model import basket as b
from view import options_list as ol
from view import table
from view import str_format as sf
import functools

def get_quantity():
    """This is a recursive function to take a correct product quantity from user.
        Returns:
            qty(Integer): The converted number taken by the user 
    """
    try:
        qty = int(input("Enter the quantity of the selected product you want to buy: "))
        return qty
    except: # the exception trigger if user enter a value that can't be casted to integer
        print(sf.error("\nYou have entered a wrong input. Please try with an integer"))
        return get_quantity()

def update_basket(basket, product):
    """This is to handle add to basket request when there is a basket that has been created already by the shopper
        There are two scenarios that handle from this function
            1. add an item that already exist in the basket - in this case, the new quantity is added into the existing quantity and-
                update the same record
            2. add a new item into  the basket - a new record is added into the basket contents table using the same basket id.
        Furthermore, there is one exception that user can't add same item to basket from two different sellers according to the table-
        design. That exception also handled in this method with a warning message to user. 

        Args:
            basket(dictionary): This dictionary object has all selected fields of basket returns from the get_by_shopper function.
                                This is considered the basket that shopper has already created.
            product(dictionary): This dictionary object has the elements which are required to add an item to basket contents table.
        Returns:
            ret(bool): it returns True if the update or create is successful and False if there is any exception
     """
    u_prod = {
        "basket_id": basket[0]["basket_id"]
        ,"product_id": product["product_id"]
        ,"quantity": product["quantity"]
        ,"price": product["price"]
        ,"seller_id": product["seller_id"]
    }
    # create filtered variable if added product is already available in the basket
    filtered = list(filter(lambda i: i["product_id"] == product["product_id"], basket))
    # if the product is avaialable in filtered need to increase the quantity
    if len(filtered) > 0: 
        f_product = filtered[0]
        u_prod["quantity"] = int(u_prod["quantity"]) + int(f_product["quantity"])
        # this is to handle an exception that shopper can't buy same product from two sellers at the same time according to-
        # the unique key design of basket_contents table.
        if f_product["seller_id"] != product["seller_id"]:
            print(sf.warning("""\nThe product has been added to cart from the seller {} already. 
                If you need to add more from the same product, select the same seller""".format(f_product["seller_name"])))
            return False
        else:
            return b.update_basket_content(u_prod)
    else:
        return b.create_basket_content(u_prod)
    return True

def add_item(shopper_id):
    """This handler function is called from the router when there is a add to basket request from user.
        The implementation has been splitted into sub functions according to the differnt scenarios.
        Args:
            shopper_id(string): shopper_id fileds of shoppers table
        Returns: void
    """
    cats = category.get_list()
    cat_id = ol._display_options(cats,"Porduct Categories","category")

    prods = p.list_by_cat_id(cat_id)
    prod_id = ol._display_options(prods,"Porducts","product")

    sellers = p.list_p_sellers_by_id(prod_id)
    # sellers_2_show variable is created to make sellers list compatible with the list_p_sellers_by_id view implementation
    sellers_2_show = list(map(lambda x: (x[0], "{} ({})".format(x[2], x[1])), sellers))
    seller_id = ol._display_options(sellers_2_show,"Sellers who sell products","seller")
    # it calls another handler function to get quantity from user with relevent prompt messages
    qty = get_quantity()
    # assign product seller details of user selected seller to selected_seller variable to get price and other relevent fields 
    selected_seller = list(filter(lambda x: (x[0] == seller_id), sellers)).pop()
    product = {
        "product_id": prod_id
        ,"seller_id": seller_id
        ,"quantity": qty
        ,"price": selected_seller[1]
    }
    #the result variable is used to get status of sub functions to give the final message to updated the status to user.
    result = False
    basket = b.get_by_shopper(shopper_id)
    if len(basket) > 0:
        result = update_basket(basket, product)
    else: 
        result = b.create_basket(shopper_id, product)
    
    if (result):
        print(sf.sucess("\nItem added to your basket\n"))
    else:
        print(sf.warning("please try again"))
    
def view_basket(shopper_id):
    """This function is called to show a list of basket items to user. 
        Args:
            shopper_id(string): shopper_id fileds of shoppers table
    """
    basket = b.get_by_shopper(shopper_id)
    # if use does not have items in basket gives a warning message
    if len(basket) == 0:
        print(sf.warning("There are no products in the basket to view."))
        return 
    # total variable is used to hold total price of the cart item. The price of each item is added to this in the loop.
    total = 0
    # loop the basket list and change elements to be compatile to draw table and add pricess to total variable
    for place, item in enumerate(basket):
        item_l = [
            item["product_description"]
            ,item["seller_name"]
            ,item["quantity"]
            ,item["formatted_price"]
            ,item["total"]
        ]
        total += item["total"]
        item_l[4] = "£{:.2f}".format(item_l[4])
        basket[place] = item_l
    # add an empty element to draw empty line between total and product_ist
    basket.append(("", "", "", "", ""))
    # add element to draw Basket Total row.
    basket.append(("", "Basket Total", "", "", "£{:.2f}".format(total)))
    # set headers to pass to the view to draw the table
    headers = (
        {"length": 70, "lable": "Product Description"}
        ,{"length": 20, "lable": "Seller Name"}
        ,{"length": 10, "lable": "Qty"}
        ,{"length": 10, "lable": "Price"}
        ,{"length": 15, "lable": "Total"}
    )
    table.dinamic_table("Basket Contents", headers, basket)