import sqlite3
from os import path
from datetime import datetime
DIR_PATH = path.dirname(path.realpath(__file__))

database_name = r"blackmountain.db"

default_today_table = r"today_entry"
default_print_table = r"prints"
default_product_table = r"products"

sql_create_product_table = r"CREATE TABLE IF NOT EXISTS {0} (id INTEGER PRIMARY KEY, product_name text, url text)"
sql_create_today_table = r"CREATE TABLE IF NOT EXISTS {0} (date text PRIMARY KEY)"
sql_select_product = r"SELECT 1 FROM {0} WHERE id=?"
sql_insert_product = r"INSERT INTO {0} VALUES (?, ?, ?)"
sql_today_entry_exists = r"SELECT 1 FROM {0} WHERE date=?"
sql_insert_today = r"INSERT INTO {0} VALUES (?)"


def open_connection():
    return sqlite3.connect(path.join(DIR_PATH, database_name))


def close_connection(connection):
    connection.close()


def insert_products(connection, table_name, products):
    #  products is a dictionary - product ID (key), name (value)
    added_products = []
    for pid in products:
        if insert_product(connection, table_name, pid, products[pid].get(r"name"), products[pid].get(r"url")):
            added_products.append(products[pid])
    return added_products


def insert_product(connection, table_name, pid, name, url):
    c = connection.cursor()
    c.execute(sql_select_product.format(table_name), (pid,))
    exists = c.fetchone()
    # TODO: we may move this select to SQL
    if exists is None:
        c.execute(sql_insert_product.format(table_name), (pid, name, url))
        connection.commit()
        return True
    return False


def create_database(connection, table_name):
    c = connection.cursor()
    c.execute(sql_create_product_table.format(table_name))
    connection.commit()


def create_today_database(connection):
    c = connection.cursor()
    c.execute(sql_create_today_table.format(default_today_table))
    connection.commit()


def is_today_init(connection, table_name=default_today_table):
    c = connection.cursor()
    today = datetime.strftime(datetime.today(), '%y-%m-%d')
    c.execute(sql_today_entry_exists.format(table_name), (today,))
    exists = c.fetchone()
    if exists is None:
        return True
    else:
        return False


def insert_today(connection, table_name=default_today_table):
    c = connection.cursor()
    today = datetime.strftime(datetime.today(), '%y-%m-%d')
    c.execute(sql_insert_today.format(table_name), (today,))
    connection.commit()

