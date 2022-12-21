from model import category
from view import options_list as ol
from model import product as p

def get_quantity():
    try:
        qty = int(input("Enter the quantity of the selected product you want to buy: "))
        return qty
    except:
        print("\nYou have entered a wrong input. Please try with an integer")
        return get_quantity()

def add_item(shopper):
    cats = category.get_list()
    cat_id = ol._display_options(cats,"Porduct Categories","category")

    prods = p.list_by_cat_id(cat_id)
    prod_id = ol._display_options(prods,"Porducts","product")

    sellers = p.list_p_sellers_by_id(prod_id)

    sellers = list(map(lambda x: (x[0], "{} ({})".format(x[2], x[1])), sellers))

    seller_id = ol._display_options(sellers,"Sellers who sell products","seller")

    qty = get_quantity()

    print(seller_id, qty)