from aiogram.utils import executor
from create_bot import dp

from handlers import user_registration


async def bot_activate(_):
    print('bot is activate')


user_registration.registr_handlers_user_registration(dp)


executor.start_polling(dp, skip_updates=True, on_startup=bot_activate)