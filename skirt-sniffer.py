import data_module
import email_module
import db_module
from jinja2 import Environment, FileSystemLoader
from os import path
import time
from datetime import datetime

DIR_PATH = path.dirname(path.realpath(__file__))

NEW_SKIRT_SUBJECT = r"Novinka! - {0}"
NEW_PRINT_SUBJECT = r"NOVÉ TISKY! - {0}"
DAY_INIT_SUBJECT = r"Keporkak se probouzí! - {0}"
PAGE_LIMIT = 20   # limit to read pages so we don't deadlock while mining data


def send_email(subject_base, data, **kwargs):
    email = email_module.Email()
    subject = subject_base.format(data[0]['name']);
    if len(data) > 1:
        subject += ' a další ...'

    file_loader = FileSystemLoader(path.join(DIR_PATH, 'templates'))
    env = Environment(loader=file_loader)
    template = env.get_template('email.html')

    email.set_content(template.render(title=subject, items=data))
    email.set_subject(subject)

    if 'is_print' in kwargs:
        if kwargs['is_print']:
            email.send(email_module.CONFIG_PRINT_R)  # send email to print Recipients
        else:
            email.send(email_module.CONFIG_REGULAR_R)  # send email to regular Recipients


def send_wakeup_email():
    email = email_module.Email()
    subject = DAY_INIT_SUBJECT.format(datetime.strftime(datetime.today(), '%y-%m-%d'));

    file_loader = FileSystemLoader(path.join(DIR_PATH, 'templates'))
    env = Environment(loader=file_loader)
    template = env.get_template('wakeup.html')

    email.set_content(template.render(title=subject))
    email.set_subject(subject)
    email.send(email_module.CONFIG_ADMIN_R)  # send email to Admin only


def run_base():
    page_no = 0

    conn = db_module.open_connection()
    db_module.create_database(conn, db_module.default_product_table)
    new_data = []

    while True:
        url = data_module.get_url(page_no)
        products = data_module.mine(url)

        # mine until we can, we don't know how many pages are in the e-shop
        if products and (page_no < PAGE_LIMIT):
            new_products = db_module.insert_products(conn, db_module.default_product_table, products)
            if new_products:
                for prod in new_products:
                    new_data.append(prod)
            else:
                break

            page_no += 1
        else:
            break

    db_module.close_connection(conn)

    if new_data:
        print("run_base({0}): New data found - sending email.".format(str(time.time())))
        send_email(NEW_SKIRT_SUBJECT, new_data, is_print=False)
    else:
        print("run_base({0}): No new data.".format(str(time.time())))


def run_print():
    conn = db_module.open_connection()
    db_module.create_database(conn, db_module.default_print_table)

    url = data_module.get_url_print()
    products = data_module.mine(url)

    new_data = None
    if products:
        new_data = db_module.insert_products(conn, db_module.default_print_table, products)
    db_module.close_connection(conn)

    if new_data:
        print("run_print({0}): New data found - sending email.".format(str(time.time())))
        send_email(NEW_PRINT_SUBJECT, new_data, is_print=True)
    else:
        print("run_print({0}): No new data.".format(str(time.time())))


def day_init_check():
    conn = db_module.open_connection()
    db_module.create_today_database(conn)

    if db_module.is_today_init(conn):
        db_module.insert_today(conn)
        print("day_init_check({0}): Today's first mining - sending email.".format(str(time.time())))
        send_wakeup_email()

    db_module.close_connection(conn)


if __name__ == "__main__":
    print("main({0}): Checking if server is available.".format(str(time.time())))
    if data_module.is_server_available() is False:
        print("main({0}): Unable to ping server.".format(str(time.time())))
    else:
        day_init_check()
        print("main({0}): Starting to mine data.".format(str(time.time())))
        run_base()
        run_print()
        print("main({0}): Finished mining.".format(str(time.time())))

