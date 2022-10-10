import database

def create_tables():
    con=database.get_db()
    with open ('tables.sql', 'r') as tables:
      con.executescript(tables.read())
    con.close()
    return True


if __name__=="__main__":
    create_tables()