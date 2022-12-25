import sqlite3
DB_PATH = "db/orinoco.db"
def get_connection():
    return sqlite3.connect(DB_PATH)

def get_dict_connection():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = dict_factory
    return con
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d