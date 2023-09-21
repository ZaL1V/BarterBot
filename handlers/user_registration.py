import json
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from functools import partial

from create_bot import dp, bot
from .user_variables_text import (
    choose_a_language_text, input_location_text, input_user_city_name_error_text,
    input_user_city_type_error_text,
    )
from .state_groups import MainState
from database import (
    session, User
    )
from keyboards import (
    build_choose_a_language_keyboard,
    build_get_location_keyboard
)
from get_location import get_location_by_city, get_location_by_coordinates


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
    get_location_kb = build_get_location_keyboard(user.language)
    await bot.send_message(
        query.message.chat.id,
        input_location_text[user.language],
        reply_markup=get_location_kb
    )
    await MainState.get_location.set()


async def input_user_city_location(message: types.Message, state: FSMContext):
    user = session.query(User).get(message.from_user.id)
    city = str(message.text)
    if city.replace(" ", "").isalpha():
        latitude, longitude = get_location_by_city(city)
        
        if latitude and longitude:
            user.address = city
            user.lat_itude = latitude
            user.long_itude = longitude
            user.status = 'active'
            session.commit()
            await state.finish()
            await bot.send_message(
                message.chat.id,
                'test'
                )
            
        else:
            await bot.send_message(
                message.chat.id,
                input_user_city_name_error_text[user.language]
            )
    else:
        await bot.send_message(
            message.chat.id,
            input_user_city_type_error_text[user.language]
        )


async def input_user_coordinates_location(message: types.Message):
    user = session.query(User).get(message.from_user.id)
    latitude = message.location.latitude
    longitude = message.location.longitude
    city = get_location_by_coordinates(latitude, longitude, user.language)
    user.address = city
    user.lat_itude = latitude
    user.long_itude = longitude
    user.status = 'active'
    session.commit()
    await bot.send_message(
        message.chat.id,
        'test'
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
    dp.register_message_handler(
        input_user_city_location,
        state=MainState.get_location
        )
    dp.register_message_handler(
        input_user_coordinates_location,
        content_types=['location'],
        state=MainState.get_location
        )
    