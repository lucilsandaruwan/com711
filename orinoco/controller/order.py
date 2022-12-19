from model import order as o_mdl
from view import table

def order_history(shopper):
    print("HI shopper", shopper)
    orders = o_mdl.get_by_shopper_id(shopper["id"])

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
    table.dinamic_table(headers, orders)