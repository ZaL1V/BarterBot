import json
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from create_bot import dp, bot
from text import (
    added_item_name_text, cancel_added_item_text, item_name_len_error_text,
    added_item_media_text, added_item_description_text, item_description_len_error_text
    )
from .state_groups import AddedItem
from database import (
    session, User, Item
    )
from keyboards import (
    build_cancel_added_item_keyboard,
    build_back_to_input_item_name_keyboard
)


#? --- Item Name --- ?#

async def added_item_name(message: types.Message):
    user = session.query(User).get(message.from_user.id)
    user_data = json.loads(user.data) if user.data else {}
    cancel_added_item_kb = build_cancel_added_item_keyboard(user.language)
    send_message = await bot.send_message(
        message.chat.id,
        added_item_name_text[user.language],
        reply_markup=cancel_added_item_kb
    )
    user_data['message_id'] = send_message.message_id
    user.data = json.dumps(user_data)
    session.commit()
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
    message_id = user_data.get('message_id')
    back_to_input_item_name_kb = build_back_to_input_item_name_keyboard(user.language)
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
        send_message = await bot.send_message(
            message.chat.id,
            added_item_description_text[user.language],
            reply_markup=back_to_input_item_name_kb
        )
        user_data['message_id'] = send_message.message_id
        user.data = json.dumps(user_data)
        session.commit()
        await  bot.edit_message_reply_markup(
            message.chat.id,
            message_id,
            reply_markup=None
        )
        await AddedItem.item_description.set()


#? --- Item Description --- ?#

async def input_item_description(message: types.Message):
    user = session.query(User).get(message.from_user.id)
    user_data = json.loads(user.data) if user.data else {}
    message_id = user_data.get('message_id')
    item_description = str(message.text)
    if len(item_description) > 200:
        await bot.send_message(
            message.chat.id,
            item_description_len_error_text[user.language]
        )
    else:
        user_data['item_description'] = item_description
        user.data = json.dumps(user_data)
        session.commit()
        await bot.send_message(
            message.chat.id,
            added_item_media_text[user.language]
        )
        await  bot.edit_message_reply_markup(
            message.chat.id,
            message_id,
            reply_markup=None
        )
        await AddedItem.item_media.set()


async def back_to_input_item_name(query: types.CallbackQuery):
    user = session.query(User).get(query.from_user.id)
    user_data = json.loads(user.data) if user.data else {}
    message_id = user_data.get('message_id')
    cancel_added_item_kb = build_cancel_added_item_keyboard(user.language)
    await  bot.edit_message_reply_markup(
            query.message.chat.id,
            message_id,
            reply_markup=None
        )
    send_message = await bot.send_message(
        query.message.chat.id,
        added_item_name_text[user.language],
        reply_markup=cancel_added_item_kb
    )
    user_data['message_id'] = send_message.message_id
    user.data = json.dumps(user_data)
    session.commit()
    await AddedItem.item_name.set()

#? --- Item Photo --- ?#

async def input_item_media():
    pass

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
    dp.register_message_handler(
        input_item_name,
        state=AddedItem.item_name
    )
    #* --- Item Description --- *#
    dp.register_message_handler(
        input_item_description,
        state=AddedItem.item_description
    )
    dp.register_callback_query_handler(
        back_to_input_item_name,
        Text(startswith='back_to_input_item_name'),
        state=AddedItem.item_description
    )
    #* --- Item Photo --- *#
    dp.register_message_handler(
        input_item_media,
        state=AddedItem.item_media
    )

    #* --- Item Tags --- *#