import json
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from sqlalchemy import or_
from create_bot import dp, bot
from text import (
    user_cabinet_menu_text, user_language_text, choose_a_language_text,
    change_city_user_cabinet_text, help_user_cabinet_text, 
    cancel_change_city_text, menu_selection_my_item_posts_text,
    standart_decorational_line_text, item_post_disabled_text, item_post_enabled_text,
    confirm_delete_item_post_text, item_post_deleted_text
    )
from auxiliary import (
    get_verified_user, get_media_list, RegistrationState
)
from database import (
    session, User, Item
    )
from keyboards import (
    build_user_cabinet_menu_keyboard,
    build_choose_a_language_keyboard,
    build_get_location_keyboard,
    build_menu_selection_my_item_posts_keyboard,
    build_output_selected_post_keyboard,
    build_my_item_post_delete_menu_keyboard
)


#? --- Cabinet Menu --- ?#

async def user_cabinet_menu(message: types.Message):
    user = await get_verified_user(message.from_user.id)
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
    user = await get_verified_user(query.from_user.id)
    await bot.send_message(
        query.message.chat.id,
        '🛠У РОЗРОБЦІ⚙️'
    )

#? ---  My Items --- ?#

async def my_items_user_cabinet(query: types.CallbackQuery):
    user = await get_verified_user(query.from_user.id)
    items = session.query(Item
    ).filter(Item.user == user.telegram_id
    ).filter(or_(Item.status == 'active', Item.status == 'passive')
    ).all()
    menu_selection_my_item_posts_kb = build_menu_selection_my_item_posts_keyboard(user.language, items)
    await bot.send_message(
        query.message.chat.id,
        menu_selection_my_item_posts_text[user.language].format(len(items)),
        reply_markup=menu_selection_my_item_posts_kb
    )
    await bot.edit_message_reply_markup(
        query.message.chat.id,
        query.message.message_id,
        reply_markup=None
    )


async def change_my_item_posts_menu_page(query: types.CallbackQuery):
    user = await get_verified_user(query.from_user.id)
    current_page = int(query.data.split('#')[1])
    items = session.query(Item
    ).filter(Item.user == user.telegram_id
    ).filter(or_(Item.status == 'active', Item.status == 'disabled')
    ).all()
    menu_selection_my_item_posts_kb = build_menu_selection_my_item_posts_keyboard(user.language, items, current_page)
    await bot.edit_message_reply_markup(
        query.message.chat.id,
        query.message.message_id,
        reply_markup=menu_selection_my_item_posts_kb
    )


async def output_selected_post(query: types.CallbackQuery):
    user = await get_verified_user(query.from_user.id)
    item_id = int(query.data.split('#')[1])
    item = session.query(Item).get(item_id)
    media_list = get_media_list(user.language, item_id)
    await bot.send_media_group(chat_id=query.message.chat.id, media=media_list)
    output_selected_post_kb = build_output_selected_post_keyboard(user.language, item_id, item.status)
    await bot.send_message(
        chat_id=query.message.chat.id,
        text=standart_decorational_line_text,
        reply_markup=output_selected_post_kb
    )
    await bot.edit_message_reply_markup(
        query.message.chat.id,
        query.message.message_id,
        reply_markup=None
    )


async def change_my_item_post_status(query: types.CallbackQuery):
    user = await get_verified_user(query.from_user.id)
    item_id = int(query.data.split('#')[1])
    item = session.query(Item).get(item_id)
    if item.status == 'active':
        item.status = 'disabled'
        session.commit()
        await bot.send_message(
            query.message.chat.id,
            item_post_disabled_text[user.language]
        )
    else:
        item.status = 'active'
        session.commit()
        await bot.send_message(
            query.message.chat.id,
            item_post_enabled_text[user.language]
        )
    output_selected_post_kb = build_output_selected_post_keyboard(user.language, item_id, item.status)
    await bot.edit_message_reply_markup(
        query.message.chat.id,
        query.message.message_id,
        reply_markup=output_selected_post_kb
    )


async def my_item_post_delete_menu(query: types.CallbackQuery):
    user = await get_verified_user(query.from_user.id)
    item_id = int(query.data.split('#')[1])
    my_item_post_delete_menu_kb = build_my_item_post_delete_menu_keyboard(user.language, item_id)
    await bot.edit_message_text(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id,
        text=confirm_delete_item_post_text[user.language],
        reply_markup=my_item_post_delete_menu_kb
    )


async def delete_my_item_post(query: types.CallbackQuery):
    user = await get_verified_user(query.from_user.id)
    item_id = int(query.data.split('#')[1])
    item = session.query(Item).get(item_id)
    item.status = 'deleted'
    session.commit()
    await bot.edit_message_text(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id,
        text=item_post_deleted_text[user.language],
        reply_markup=None
    )


async def back_to_my_item_post_menu(query: types.CallbackQuery):
    user = await get_verified_user(query.from_user.id)
    item_id = int(query.data.split('#')[1])
    item = session.query(Item).get(item_id)
    output_selected_post_kb = build_output_selected_post_keyboard(user.language, item_id, item.status)
    await bot.edit_message_text(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id,
        text=standart_decorational_line_text,
        reply_markup=output_selected_post_kb
    )

#? ---  Incoming Requests --- ?#

async def incoming_requests_user_cabinet(query: types.CallbackQuery):
    user = await get_verified_user(query.from_user.id)
    await bot.send_message(
        query.message.chat.id,
        '🛠У РОЗРОБЦІ⚙️'
    )

#? ---  My Exchanges --- ?#

async def my_exchanges_user_cabinet(query: types.CallbackQuery):
    user = await get_verified_user(query.from_user.id)
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
    user = await get_verified_user(query.from_user.id)
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


# async def cancel_change_city(query: types.CallbackQuery, state: FSMContext):
#     user = await get_verified_user(query.from_user.id)
#     await state.finish()
#     await bot.send_message(
#         query.message.chat.id,
#         cancel_change_city_text[user.language].format(user.address)
#     )
#     await bot.edit_message_reply_markup(
#         query.message.chat.id,
#         query.message.message_id,
#         reply_markup=None
#     )


#? --- HELP --- ?#

async def help_user_cabinet(query: types.CallbackQuery):
    user = await get_verified_user(query.from_user.id)
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
    dp.register_callback_query_handler(
        change_my_item_posts_menu_page,
        Text(startswith='change_my_item_posts_menu_page#')
    )
    dp.register_callback_query_handler(
        output_selected_post,
        Text(startswith='manage_my_item_post#')
    )
    dp.register_callback_query_handler(
        change_my_item_post_status,
        Text(startswith='change_my_item_post_status#')
    )
    dp.register_callback_query_handler(
        my_item_post_delete_menu,
        Text(startswith='my_item_post_delete_menu#')
    )
    dp.register_callback_query_handler(
        delete_my_item_post,
        Text(startswith='delete_my_item_post#')
    )
    dp.register_callback_query_handler(
        back_to_my_item_post_menu,
        Text(startswith='back_to_my_item_post_menu#')
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
    # dp.register_callback_query_handler(
    #     cancel_change_city,
    #     Text(startswith='cancel_change_city')
    # )
    #* --- HELP --- *#
    dp.register_callback_query_handler(
        help_user_cabinet,
        Text(startswith='help_user_cabinet')
    )