from model import db_connector
def get_shopper_by_id(shopper_id):
    try:
        con = db_connector.get_dict_connection()
        cursor = con.cursor()
        query = "SELECT shopper_id, shopper_first_name FROM shoppers WHERE shopper_id = ?"
        cursor.execute(query, (shopper_id,))
        ret = cursor.fetchone()
        con.close()
        return ret
    except:
        print("""There is an exception with db connection. Please check whether the db file is uploaded into the correct path according to ./model/db_connector.py""")
        raise