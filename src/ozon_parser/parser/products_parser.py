import time
import requests
from bs4 import BeautifulSoup


def get_page(url):
    post_body = {
        'cmd': 'request.get',
        'url': url,
        'maxTimeout': 60000
    }

    response = requests.post(
        'http://localhost:8191/v1',
        headers={'Content-Type': 'application/json'},
        json=post_body
    )
    if response.status_code == 200:
        return response.json()['solution']['response']
    else:
        raise requests.exceptions.ConnectionError(
            f'Ошибка прокси'
        )


def parse_page(url, product_count, current_page: int):
    response = get_page(url)
    time.sleep(5)
    soup = BeautifulSoup(response, 'lxml')

    cards = soup.find_all('div', {'class': 'u0i ui1'})
    products = []
    count = product_count

    for card in cards:
        if len(products) >= product_count:
            return products, None
        name = card.find('a', {'class': 'tile-hover-target ir2 r2i'}).text
        price = card.find('span', {'class': 'c3117-a1'}).text
        image_url = card.find('img')['src']
        discount = card.find('span', {'class': 'c3117-a2'}).text

        url = card.find('a', {'class': 'ir8'})['href']
        product_response = get_page(f'https://www.ozon.ru{url}')
        time.sleep(5)
        product_soup = BeautifulSoup(product_response, 'lxml')
        try:
            description = product_soup.find('div', {'class': 'ra-a1'}).text
        except AttributeError:
            description = 'Отсутствует'

        print(name, '  ', price, '  ', image_url, '  ', discount)
        print(description)
        print(f'продукт номер {count}')
        count -= 1
        products.append(
            {
                'name': name,
                'price': price,
                'image_url': image_url,
                'discount': discount,
                'description': description
            }
        )
    next_url = soup.find_all('a', {'class': 'e6p'})[current_page]
    next_url = f'https://www.ozon.ru{next_url["href"]}'
    print(next_url)
    return products, next_url


def parse_pages(url, count_products):
    results = []
    current_page = 1
    while len(results) < count_products:
        products, next_url = parse_page(url, count_products, current_page)
        results.extend(products)
        if next_url:
            count_products -= len(products)
            url = next_url
            current_page += 1
    print('Всё готово')

    return results


# parse_page('https://www.ozon.ru/seller/1/products/', 45, 1)

parse_pages('https://www.ozon.ru/seller/1/products/', 45)
