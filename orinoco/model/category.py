# This model is creared to do data base functions regarding to categories.
# there is only one function in this model as there is no any requirement to update or get details of categories.
from model import db_connector
def get_list():
    """This function is to get category_id and category_description as a list. This can be extended to add more fields in future requirements
    Note: the first two fields(category_id, category_description) should be in the same possition (0, 1) when adding new fields
        Returns:
            list: it returns list of arrays.
    """
    con = db_connector.get_connection()
    cursor = con.cursor()
    query = "SELECT category_id, category_description FROM categories ORDER BY category_description"
    cursor.execute(query)
    ret = cursor.fetchall()
    con.close()
    return ret