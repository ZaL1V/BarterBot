from aiogram.utils import executor
from create_bot import dp

from handlers import (
    user_registration, user_cabinet, user_adding_item
)


async def bot_activate(_):
    print('bot is activate')


user_registration.registr_handlers_user_registration(dp)
user_cabinet.registr_handlers_user_cabinet(dp)
user_adding_item.registr_handlers_user_adding_item(dp)


executor.start_polling(dp, skip_updates=True, on_startup=bot_activate)