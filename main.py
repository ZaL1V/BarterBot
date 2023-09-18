from aiogram.utils import executor
from create_bot import dp


async def bot_activate(_):
    print('bot is activate')




executor.start_polling(dp, skip_updates=True, on_startup=bot_activate)