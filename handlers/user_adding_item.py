import json
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from create_bot import dp, bot
from text import (
    added_item_name_text, cancel_added_item_text, item_name_len_error_text
    )
from .state_groups import AddedItem
from database import (
    session, User, Item
    )
from keyboards import (
    build_cancel_added_item_keyboard
)


#? --- Item Name --- ?#

async def added_item_name(message: types.Message):
    user = session.query(User).get(message.from_user.id)
    cancel_added_item_kb = build_cancel_added_item_keyboard(user.language)
    await bot.send_message(
        message.chat.id,
        added_item_name_text[user.language],
        reply_markup=cancel_added_item_kb
    )
    await message.delete()
    await AddedItem.item_name.set()


async def cancel_added_item(query: types.CallbackQuery, state: FSMContext):
    user = session.query(User).get(query.from_user.id)
    await state.finish()
    await bot.send_message(
        query.message.chat.id,
        cancel_added_item_text[user.language]
    )
    await bot.edit_message_reply_markup(
        query.message.chat.id,
        query.message.message_id,
        reply_markup=None
    )


async def input_item_name(message: types.Message, state: FSMContext):
    user = session.query(User).get(message.from_user.id)
    user_data = json.loads(user.data) if user.data else {}
    item_name = str(message.text)
    if len(item_name) > 24:
        await bot.send_message(
            message.chat.id,
            item_name_len_error_text[user.language]
        )
    else: 
        user_data['item_name'] = item_name
        user.data = json.dumps(user_data)
        session.commit()
        await bot.send_message(
            message.chat.id,
            'test'
        )
        await  bot.edit_message_reply_markup(
            message.chat.id,
            message.message_id,
            reply_markup=None
        )
        await AddedItem.item_media.set()


#? --- Item Description --- ?#


#? --- Item Photo --- ?#


#? --- Item Tags --- ?#



def registr_handlers_user_adding_item(dp: Dispatcher):
    #* --- Item Name --- *#
    dp.register_message_handler(
        added_item_name,
        Text(equals=[
            "➕ Додати предмет",
            "➕ Add item",
            "➕ Dodaj przedmiot",
            "➕ Добавить предмет",
            ]
            )
        )
    dp.register_callback_query_handler(
        cancel_added_item,
        Text(startswith='cancel_added_item'),
        state=AddedItem.item_name
    )
    #* --- Item Description --- *#


    #* --- Item Photo --- *#


    #* --- Item Tags --- *#