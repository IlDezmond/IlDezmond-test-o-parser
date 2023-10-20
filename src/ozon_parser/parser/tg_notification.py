from aiogram import Dispatcher, Bot
import os
import asyncio
from dotenv import load_dotenv


load_dotenv()


TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
USER_ID = os.getenv('TELEGRAM_USER_ID')

dp = Dispatcher()
bot = Bot(token=TOKEN)


async def send_simple_message(text):
    await bot.send_message(chat_id=USER_ID, text=text)
    await bot.session.close()


def send_notification(product_count):
    text = f'Завершён парсинг {product_count} продуктов'
    asyncio.run(send_simple_message(text))
