# this is the shopper controller file, it contains all the handlers relevent to shoppers.
# sample possible handlers (login,view shopper profile, edit shopper profile)

from model import shopper
from view import str_format as sf

def login():
    """"To take the shopper_id from the user and check if it is available in the database.
        This will return shopper details if the given shopper_id is exist otherwise, it will keep asking
        for a correct shopper_id
            Returns:
                s_details(dictionary/ False): A dictionary having selected fields from the shoppers table as keys or False-
                if user enter "e" as shopper_id to exit from the app
    """
    # Used this loop to get shopper id in a never ending loop untill user enter a correct shopper id.
    while True:
        s_id = input("\nPlease enter the shopper_id to continue or {} to exit: ".format(sf.blue("e")))
        if(s_id == "e"):
            return False
        s_details = shopper.get_shopper_by_id(s_id)
        if s_details:
            print(sf.sucess("\nHi {}, you are welcome to the Orinoco shopping!".format(s_details["shopper_first_name"])))
            return s_details
        else:
            print(sf.warning("\nThe shopper_id you have entered is not available in our system."))