import sqlite3


def get_db():
    connect=sqlite3.connect("mydatabase.sqlite", detect_types=sqlite3.PARSE_DECLTYPES)
    connect.row_factory = sqlite3.Row
    return connect