from bs4 import BeautifulSoup
import requests
from os import popen

DIV_NAME = r"productTitleContent"
BASE_URL = r"https://www.blackmountain.cz"


def is_server_available():
    out = str(popen('curl -s -w "%{http_code}" -L ' + BASE_URL + ' -o /dev/null').read())
    if out == "200":  # HTTP request success
        return True
    else:
        return False


def get_url(page):
    return BASE_URL + r'/request.php?request_uri=/sukne&action=Get_products&pages[0]=blackmountain&' \
            'pages[1]=eshop&pages[2]=1-1-Sukne&pages[3]=0&pages[4]=42&sort=42&man=9&page={0}'.format(page)


def get_url_print():
    return BASE_URL + r'/tisky'


def get_div_elements(url, class_name):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    if class_name is not None:
        divs = soup.find_all("div", class_=class_name)
    else:
        divs = soup.find_all("div")
    return divs


def mine(url, class_name=DIV_NAME):
    products = {}
    for elem in get_div_elements(url, class_name):
        href = elem.a['href']
        url_split = href.split("/")  # e.g. /blackmountain/eshop/1-1-Sukne/0/5/13000-Baletka-47cm
        try:
            ident_split = url_split[6].split("-")  # e.g. 13000-Baletka-47cm
            pid = ident_split[0]
            name = elem.text
            if id not in products:
                products[pid] = {'name': name, 'url': BASE_URL + href}
        except IndexError: # there can be one other type of url e.g. /lesnipohadkadopasu-34
            try:
                ident_split = url_split[1].split("-")
                pid = ident_split[1]
                name = elem.text
                if id not in products:
                    products[pid] = {'name': name, 'url': BASE_URL + href}
            except IndexError: # skip errors in case string for some reason doesn't match expected pattern
                pass

    return products
