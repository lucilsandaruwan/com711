from model import shopper

def get_details(shopper_id):
    ret = {
        "exist": False
    }
    row = shopper.get_shopper_by_id(shopper_id)
    if(row):
        ret = {
            "exist": True
            ,"id": row[0]
            ,"first_name": row[1]
        }

    return ret

def login():
    while True:
        s_id = input("\nPlease enter the shopper_id to continue: ")
        s_details = get_details(s_id)
        if(s_details["exist"]):
            print("\nHi {}, you are welcome to the Orinoco shopping!".format(s_details["first_name"]))
            return s_details
        else:
            print("\nThe shopper_id you have entered is not available in our system.")