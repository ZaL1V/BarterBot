import json

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


storage = MemoryStorage()


with open('keys.json', 'r') as file:
    json_data = json.load(file)

bot = Bot(token=json_data['TOKEN'])
dp = Dispatcher(bot, storage=storage)
