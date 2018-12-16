import data_module
import email_module
import db_module

NEW_SKIRT_SUBJECT = r"Novinka! - {0}"

if __name__ == "__main__":
    page_no = 0

    conn = db_module.open_connection()
    new_data = []
    while True:
        url = data_module.get_url(page_no)
        products = data_module.mine(url)

        # mine until we can, we don't know how many pages are in the e-shop
        if products:
            new_products = db_module.insert_products(conn, products)
            if new_products:
                new_data.append(new_products)

            page_no += 1
        else:  # there is no data anymore so we can break
            break
    db_module.close_connection(conn)

    if new_data:
        email = email_module.Email()

        email.set_subject(NEW_SKIRT_SUBJECT.format())
        # TODO: template
        email.set_content(r"")
        email.send()
