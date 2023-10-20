import asyncio
from json import loads

import aiohttp
from aiogram import F, Router

BACKEND_URL = 'http://parser-backend:8000/api/v1/products/'
# BACKEND_URL = 'http://127.0.0.1:8000/api/v1/products/'

router = Router()


async def get_products():
    async with aiohttp.ClientSession() as session:
        async with session.get(BACKEND_URL) as resp:
            text = await resp.text()
            return loads(text)


def make_products_message(products):
    return '\n'.join(
        f'{product["name"]} - {product["url"]}' for product in products
    )


@router.message(F.text == 'Список товаров')
async def list_products_handler(message):
    response = await get_products()
    text = make_products_message(response)
    await message.answer(text)


async def main():
    response = await get_products()
    text = make_products_message(response)
    print(text)


if __name__ == '__main__':
    asyncio.run(main())
