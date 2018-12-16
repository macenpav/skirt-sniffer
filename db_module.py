import sqlite3

database_name = r"blackmountain.db"

sql_create_product_table = r"CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, product_name text, url text)"
sql_select_product = r"SELECT 1 FROM products WHERE id=?"
sql_insert_product = r"INSERT INTO products VALUES (?, ?, ?)"


def open_connection():
    sqlite3.connect(database_name)


def close_connection(connection):
    connection.close()


def insert_products(connection, products):
    #  products is a dictionary - product ID (key), name (value)
    inserted = False
    for pid in products:
        if insert_product(connection, pid, products[pid].get(r"name"), products[pid].get(r"url")):
            inserted = True
    return inserted


def insert_product(connection, pid, name, url):
    c = connection.cursor()
    c.execute(sql_select_product, (pid,))
    exists = c.fetchone()
    # TODO: we may move this select to SQL
    if not exists:
        c.execute(sql_insert_product, (pid, name, url))
        connection.commit()
        return True
    return False


def create_database(connection):
    c = connection.cursor()
    c.execute(sql_create_product_table)
    connection.commit()

