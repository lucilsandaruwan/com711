from model import db_connector
def get_list():
    con = db_connector.get_connection()
    cursor = con.cursor()
    query = "SELECT category_id, category_description FROM categories ORDER BY category_description"
    cursor.execute(query)
    ret = cursor.fetchall()
    con.close()
    return ret