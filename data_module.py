from bs4 import BeautifulSoup
import requests


div_name = r"productTitleContent"
base_url = r"https://www.blackmountain.cz/"


def get_url(page):
    return base_url + r'request.php?request_uri=/sukne&action=Get_products&pages[0]=blackmountain&' \
            'pages[1]=eshop&pages[2]=1-1-Sukne&pages[3]=0&pages[4]=42&sort=42&man=9&page={0}'.format(page)


def get_div_elements(url, class_name):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    if class_name is not None:
        divs = soup.find_all("div", class_=class_name)
    else:
        divs = soup.find_all("div")
    return divs


def mine(url, class_name=div_name):
    products = {}
    for elem in get_div_elements(url, class_name):
        href = elem.a['href']
        url_split = href.split("/")  # e.g. /blackmountain/eshop/1-1-Sukne/0/5/13000-Baletka-47cm
        try:
            ident_split = url_split[6].split("-")  # e.g. 13000-Baletka-47cm
            pid = ident_split[0]
            name = elem.text
            if id not in products:
                products[pid] = {'name': name, 'url': base_url + href}
        except ValueError:  # skip errors in case string for some reason doesn't match expected pattern
            pass
    return products
