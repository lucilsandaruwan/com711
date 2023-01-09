# This file contains the data base connection related common functions to be used in other models.
import sqlite3
DB_PATH = "db/orinoco.db"
def get_connection():
    """This returns a normal connection wich gives rows in results for select quaries are as arrays.
        Returns:
            sqlite3.Connection
    """
    return sqlite3.connect(DB_PATH)

def get_dict_connection():
    """This returns a connection wich gives rows in results for select quaries are as dictionaries.
        Returns:
            sqlite3.Connection
    """
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

def get_sequence_number(table_name):
    """This is to get the next possible primary key of a table
        Args:
            table_name(string): The name of the considering table
        Returns:
            integer: the possible value of the next primary key
    """
    con = get_connection()
    cursor = con.cursor()
    query = "SELECT IFNULL((SELECT seq + 1 FROM sqlite_sequence WHERE name = \"{}\"  ), 1)".format(table_name)
    cursor.execute(query)
    ret = cursor.fetchone()
    con.close()
    return ret[0]
