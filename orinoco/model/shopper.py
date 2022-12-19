from model import db_connector
def get_shopper_by_id(shopper_id):
    con = db_connector.get_connection()
    cursor = con.cursor()
    query = "SELECT shopper_id, shopper_first_name FROM shoppers WHERE shopper_id = ?"
    cursor.execute(query, (shopper_id,))
    ret = cursor.fetchone()
    con.close()
    return ret