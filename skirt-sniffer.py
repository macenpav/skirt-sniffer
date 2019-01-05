import data_module
import email_module
import db_module
from jinja2 import Environment, FileSystemLoader
from os import path

DIR_PATH = path.dirname(path.realpath(__file__))

NEW_SKIRT_SUBJECT = r"Novinka! - {0}"
NEW_PRINT_SUBJECT = r"NOVÉ TISKY! - {0}"


def send_email(subject_base, data):
    email = email_module.Email()
    subject = subject_base.format(data[0]['name']);
    if len(data) > 1:
        subject += ' a další ...'

    file_loader = FileSystemLoader(path.join(DIR_PATH, 'templates'))
    env = Environment(loader=file_loader)
    template = env.get_template('email.html')

    email.set_content(template.render(title=subject, items=data))
    email.set_subject(subject)
    email.send()


def run_base():
    table_name = r"products"

    page_no = 0

    conn = db_module.open_connection()
    db_module.create_database(conn, table_name)
    new_data = []
    while True:
        url = data_module.get_url(page_no)
        products = data_module.mine(url)

        # mine until we can, we don't know how many pages are in the e-shop
        if products:
            new_products = db_module.insert_products(conn, table_name, products)
            if new_products:
                for prod in new_products:
                    new_data.append(prod)
            else:
                break

            page_no += 1
    db_module.close_connection(conn)

    if new_data:
        send_email(NEW_SKIRT_SUBJECT, new_data)


def run_print():
    table_name = "prints"

    conn = db_module.open_connection()
    db_module.create_database(conn, table_name)

    url = data_module.get_url_print()
    products = data_module.mine(url)

    new_data = None
    if products:
        new_data = db_module.insert_products(conn, table_name, products)
    db_module.close_connection(conn)

    if new_data is not None:
        send_email(NEW_PRINT_SUBJECT, new_data)


if __name__ == "__main__":
    run_base()
    run_print()
