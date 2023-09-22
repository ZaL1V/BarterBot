import json
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from create_bot import dp, bot
from text import (
    user_cabinet_menu_text, user_language_text, choose_a_language_text,
    change_city_user_cabinet_text, help_user_cabinet_text
    )
from .state_groups import RegistrationState
from database import (
    session, User
    )
from keyboards import (
    build_user_cabinet_menu_keyboard,
    build_choose_a_language_keyboard,
    build_get_location_keyboard
)


#? --- Cabinet Menu --- ?#

async def user_cabinet_menu(message: types.Message):
    user = session.query(User).get(message.from_user.id)
    user_cabinet_menu_kb = build_user_cabinet_menu_keyboard(user.language)
    telegram_id = f'<code>{user.telegram_id}</code>'
    address = user.address
    language = user_language_text[user.language]
    if isinstance(user.rating, str):
        user_rating_json = json.loads(user.rating)
    else:
        user_rating_json = user.rating
    rating = sum(user_rating_json)/len(user_rating_json)
    await bot.send_message(
        message.chat.id,
        user_cabinet_menu_text[user.language].format(
            telegram_id, address, language, rating
            ),
        reply_markup=user_cabinet_menu_kb,
        parse_mode='HTML'
    )
    
    await message.delete()


#? --- Favorites --- ?#

async def favorites_user_cabinet(query: types.CallbackQuery):
    user = session.query(User).get(query.from_user.id)
    await bot.send_message(
        query.message.chat.id,
        '🛠У РОЗРОБЦІ⚙️'
    )

#? ---  My Items --- ?#

async def my_items_user_cabinet(query: types.CallbackQuery):
    user = session.query(User).get(query.from_user.id)
    await bot.send_message(
        query.message.chat.id,
        '🛠У РОЗРОБЦІ⚙️'
    )

#? ---  Incoming Requests --- ?#

async def incoming_requests_user_cabinet(query: types.CallbackQuery):
    user = session.query(User).get(query.from_user.id)
    await bot.send_message(
        query.message.chat.id,
        '🛠У РОЗРОБЦІ⚙️'
    )

#? ---  My Exchanges --- ?#

async def my_exchanges_user_cabinet(query: types.CallbackQuery):
    user = session.query(User).get(query.from_user.id)
    await bot.send_message(
        query.message.chat.id,
        '🛠У РОЗРОБЦІ⚙️'
    )

#? --- Change Language --- ?#

async def change_language_user_cabinet(query: types.CallbackQuery):
    choose_a_language_kb = build_choose_a_language_keyboard()
    await bot.send_message(
        query.message.chat.id,
        choose_a_language_text,
        reply_markup=choose_a_language_kb
    )
    await bot.edit_message_reply_markup(
        query.message.chat.id,
        query.message.message_id,
        reply_markup=None
    )

#? --- Change City --- ?#

async def change_city_user_cabinet(query: types.CallbackQuery):
    user = session.query(User).get(query.from_user.id)
    get_location_kb = build_get_location_keyboard(user.language)
    await bot.send_message(
        query.message.chat.id,
        change_city_user_cabinet_text[user.language],
        reply_markup=get_location_kb
    )
    await bot.edit_message_reply_markup(
        query.message.chat.id,
        query.message.message_id,
        reply_markup=None
    )
    await RegistrationState.get_location.set()

#? --- HELP --- ?#

async def help_user_cabinet(query: types.CallbackQuery):
    user = session.query(User).get(query.from_user.id)
    help_url = '@ZalevSkyiM'
    await bot.send_message(
        query.message.chat.id,
        help_user_cabinet_text[user.language].format(help_url)
    )
    await bot.edit_message_reply_markup(
        query.message.chat.id,
        query.message.message_id,
        reply_markup=None
    )


def registr_handlers_user_cabinet(dp: Dispatcher):
    #* --- Cabinet Menu --- *#
    dp.register_message_handler(
        user_cabinet_menu,
        Text(equals=[
            "🧔 Мій профіль",
            "🧔 My Profile",
            "🧔 Mój profil",
            "🧔 Мой профиль",
            ]
            )
        )
    #* --- Favorites --- *#
    dp.register_callback_query_handler(
        favorites_user_cabinet,
        Text(startswith='my_favorites_user_cabinet')
    )
    #* --- My Items --- *#
    dp.register_callback_query_handler(
        my_items_user_cabinet,
        Text(startswith='my_items_user_cabinet')
    )
    #* --- Incoming Requests --- *#
    dp.register_callback_query_handler(
        incoming_requests_user_cabinet,
        Text(startswith='incoming_applications_user_cabinet')
    )
    #* --- My Exchanges --- *#
    dp.register_callback_query_handler(
        my_exchanges_user_cabinet,
        Text(startswith='my_exchanges_user_cabinet')
    )
    #* --- Change Language --- *#
    dp.register_callback_query_handler(
        change_language_user_cabinet,
        Text(startswith='change_language_user_cabinet')
    )
    #* --- Change City --- *#
    dp.register_callback_query_handler(
        change_city_user_cabinet,
        Text(startswith='change_city_user_cabinet')
    )
    #* --- HELP --- *#
    dp.register_callback_query_handler(
        help_user_cabinet,
        Text(startswith='help_user_cabinet')
    )