import os


from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from .handlers.handler import router_base


bot = Bot(os.getenv('BOT_API'))
dp = Dispatcher()



dp.include_router(router_base)

