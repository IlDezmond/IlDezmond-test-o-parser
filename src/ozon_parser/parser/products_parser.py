import time

import requests
from bs4 import BeautifulSoup
from celery import shared_task

from products.models import Product
from parser.tg_notification import send_notification

OZON_URL = 'https://www.ozon.ru'
URL_FOR_PARSE = 'https://www.ozon.ru/seller/1/products/'


def get_page(url):
    post_body = {
        'cmd': 'request.get',
        'url': url,
        'maxTimeout': 60000
    }

    response = requests.post(
        'http://ozon-flaresolverr:8191/v1',
        # 'http://localhost:8191/v1',
        headers={'Content-Type': 'application/json'},
        json=post_body
    )
    if response.status_code == 200:
        return response.json()['solution']['response']
    else:
        raise requests.exceptions.ConnectionError(
            'Ошибка прокси'
        )


def parse_page(url, product_count, current_page: int):
    response = get_page(url)
    time.sleep(5)
    soup = BeautifulSoup(response, 'lxml')

    cards = (soup.find('div', {'data-widget': 'searchResultsV2'}).find('div').
    find_all(
        'div', recursive=False
    )
    )
    products = []
    count = product_count

    for card in cards:
        if len(products) >= product_count:
            return products, None
        name = card.find('span', {'class': 'tsBody500Medium'}).text
        price = card.find('span', {'class': 'tsHeadline500Medium'}).text
        formatted_price = int(price.replace('\u2009', '').replace('₽', ''))
        image_url = card.find('img')['src']
        discount = card.find_all(
            'span',
            {'class': 'tsBodyControl400Small'}
        )[1].text
        formatted_discount = int(
            discount.replace('\u2009', '').replace('%', '').replace('−', '')
        )

        url = card.find('a', {'class': 'tile-hover-target'})['href']
        url = url.split('/?')[0]
        product_response = get_page(f'{OZON_URL}{url}')
        time.sleep(5)
        product_soup = BeautifulSoup(product_response, 'lxml')
        try:
            description = (product_soup.find(
                'div',
                {'id': 'section-description'}
            ).text.replace('\n', ' ').
                           replace('Описание', '')).replace(
                '\xa0',
                ' '
            ).strip()
        except AttributeError:
            description = 'Отсутствует'

        count -= 1
        products.append(
            {
                'name': name,
                'price': formatted_price,
                'image_url': image_url,
                'discount': formatted_discount,
                'description': description,
                'url': f'{OZON_URL}{url}'
            }
        )
        print(products[-1])
    next_url = soup.find_all('a', {'class': 'e6p'})[current_page]
    next_url = f'{OZON_URL}{next_url["href"]}'
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

    return results


def save_products(products):
    Product.objects.all().delete()
    for product in products:
        Product.objects.get_or_create(
            name=product['name'],
            price=product['price'],
            image_url=product['image_url'],
            discount=product['discount'],
            description=product['description'],
            url=product['url']
        )


@shared_task
def parse_task(product_count):
    products = parse_pages(
        URL_FOR_PARSE,
        product_count
    )
    save_products(products)
    send_notification(len(products))


# parse_pages('https://www.ozon.ru/seller/1/products/', 10)
