from model import category
from view import options_list as ol
from view import table
from model import product as p
from model import basket as b
import functools

def get_quantity():
    try:
        qty = int(input("Enter the quantity of the selected product you want to buy: "))
        return qty
    except:
        print("\nYou have entered a wrong input. Please try with an integer")
        return get_quantity()

def update_basket(basket, product):
    u_prod = {
        "basket_id": basket[0][5]
        ,"product_id": product["product_id"]
        ,"quantity": product["quantity"]
        ,"price": product["price"]
        ,"seller_id": product["seller_id"]
    }
    filtered = list(filter(lambda i: i[6] == product["product_id"], basket))
    if len(filtered) > 0:
        f_product = filtered[0]
        u_prod["quantity"] = int(u_prod["quantity"]) + int(f_product[2])
        if f_product[7] != product["seller_id"]:
            print("""\nThe product has already added to cart from the seller {}. 
                If you need to add more from the same product, select the same seller""".format(f_product[1]))
            return False
        else:
            return b.update_basket_content(u_prod)
    else:
        return b.create_basket_content(u_prod)
    return True

def add_item(shopper):
    cats = category.get_list()
    cat_id = ol._display_options(cats,"Porduct Categories","category")

    prods = p.list_by_cat_id(cat_id)
    prod_id = ol._display_options(prods,"Porducts","product")

    sellers = p.list_p_sellers_by_id(prod_id)

    sellers_2_show = list(map(lambda x: (x[0], "{} ({})".format(x[2], x[1])), sellers))

    seller_id = ol._display_options(sellers_2_show,"Sellers who sell products","seller")

    qty = get_quantity()

    selected_seller = list(filter(lambda x: (x[0] == seller_id), sellers)).pop()
    product = {
        "product_id": prod_id
        ,"seller_id": seller_id
        ,"quantity": qty
        ,"price": selected_seller[1]
    }
    ret = False
    basket = b.get_by_shopper(shopper["id"])
    if len(basket) > 0:
        ret = update_basket(basket, product)
    else: 
        ret = b.create_basket(shopper["id"], product)
    
    if (ret):
        print("\nItem added to your basket\n")
    else:
        print("please try again")
    
def view_basket(shopper):
    basket = b.get_by_shopper(shopper["id"])
    if len(basket) == 0:
        print("There are no items in the basket.")
        return 
    total = 0
    for place, item in enumerate(basket):
        item_l = list(item)[0:5]
        total += item_l[4]
        item_l[4] = "£{:.2f}".format(item_l[4])
        basket[place] = item_l
    basket.append(("", "", "", "", ""))
    basket.append(("", "Basket Total", "", "", "£{:.2f}".format(total)))
    headers = (
        {"length": 70, "lable": "Product Description"}
        ,{"length": 20, "lable": "Seller Name"}
        ,{"length": 10, "lable": "Qty"}
        ,{"length": 10, "lable": "Price"}
        ,{"length": 15, "lable": "Total"}
    )
    # print(total)
    table.dinamic_table("Basket Contents", headers, basket)