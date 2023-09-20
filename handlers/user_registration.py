import json
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from functools import partial

from create_bot import dp, bot
from .user_variables_text import (
    choose_a_language_text, input_location_text
    )
from database import (
    session, User
    )
from keyboards import (
    build_choose_a_language_keyboard
)


async def command_start(message: types.Message):
    user = session.query(User).filter(
        User.telegram_id == message.from_user.id
        ).first()
    if not user:
        choose_a_language_kb = build_choose_a_language_keyboard()
        await bot.send_message(
            message.chat.id,
            choose_a_language_text,
            reply_markup=choose_a_language_kb
        )
        rating = [5, 5, 5]
        rating_json = json.dumps(rating)
        chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)
        username = chat_member.user.username
        user = User(
            telegram_id=message.from_user.id,
            username=username,
            language=None,
            status='not_verified',
            data={},
            rating=rating_json,
            address='',
            long_itude=None,
            lat_itude=None
        )
        session.add(user)
        session.commit()
        print('Created User:', user.telegram_id)


async def choose_a_language(query: types.CallbackQuery):
    user = session.query(User).get(query.from_user.id)
    language_key = query.data.split('#')[1]
    user.language = language_key
    session.commit()
    
    await bot.edit_message_reply_markup(
        query.message.chat.id,
        query.message.message_id,
        reply_markup=None
    )
    await bot.send_message(
        query.message.chat.id,
        input_location_text[user.language],
        
    )


def registr_handlers_user_registration(dp: Dispatcher):
    dp.register_message_handler(
        command_start,
        commands=['start']
        )
    dp.register_callback_query_handler(
        choose_a_language,
        Text(startswith='choose_language#')
    )