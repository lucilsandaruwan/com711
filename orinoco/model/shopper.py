# This file contains the functions related to data base queries regarding shoppers
from model import db_connector
def get_shopper_by_id(shopper_id):
    """This is to get shopper details by shopper_id given by user. The select query of this can be freely extends as it is returning
    dictionary object as return. An exception message is added as this is the first db request triggers from the app.
        Args:
            shopper_id(string): the shopper_id taken from the user
        Returns: 
            dictionary: having selected fields from the shoppers table.
    """
    try:
        con = db_connector.get_dict_connection()
        print("type is: ", type(con))
        cursor = con.cursor()
        query = "SELECT shopper_id, shopper_first_name FROM shoppers WHERE shopper_id = ?"
        cursor.execute(query, (shopper_id,))
        ret = cursor.fetchone()
        con.close()
        return ret
    except:
        print("""There is an exception with db connection. Please check whether the db file is uploaded into the correct path according to ./model/db_connector.py""")
        raise