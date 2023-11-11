import json, asyncio
from aiogram import types, Dispatcher
from aiogram.types import ContentType
from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import InputMediaPhoto, InputMediaVideo
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from create_bot import dp, bot
from text import (
    added_item_name_text, cancel_added_item_text, item_name_len_error_text,
    added_item_media_text, added_item_description_text, item_description_len_error_text,
    input_required_msg_text, input_required_media_text, max_media_sent_text,
    invalid_media_type_text, media_count_msg_text, input_media_video_duration_error_text,
    quantity_item_media_text, media_is_not_loaded_text, clear_media_text,
    item_form_post_with_description, item_form_post_no_description, standart_decorational_line_text,
    confirmation_create_item_post_text, change_item_name_text, change_item_description_text,
    added_new_item_media_text
    )
from ignore_values import should_ignore
from user_valodation import get_verified_user
from .state_groups import AddedItem
from basic_tools import get_column_by_language
from database import (
    session, User, Item, Tag
    )
from keyboards import (
    build_general_menu_keyboard,
    build_cancel_added_item_keyboard,
    build_back_to_input_item_name_keyboard,
    build_input_item_media_keyboard,
    build_final_item_post_keyboard,
    build_change_item_post_menu_kayboard,
    build_delete_item_description_keyboard,
    build_change_item_media_keyboard
)



#? --- Item Name --- ?#

async def added_item_name(message: types.Message):
    user = await get_verified_user(message.from_user.id)
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
    user = await get_verified_user(query.from_user.id)
    general_menu_kb = build_general_menu_keyboard(user.language)
    await state.finish()
    await bot.send_message(
        query.message.chat.id,
        cancel_added_item_text[user.language],
        reply_markup=general_menu_kb
    )
    await bot.edit_message_reply_markup(
        query.message.chat.id,
        query.message.message_id,
        reply_markup=None
    )


async def input_item_name(message: types.Message, state: FSMContext):
    user = await get_verified_user(message.from_user.id)
    user_data = json.loads(user.data) if user.data else {}
    message_id = user_data.get('message_id')
    back_to_input_item_name_kb = build_back_to_input_item_name_keyboard(user.language)
    item_name = str(message.text)
    if should_ignore(item_name, user.language):
        await bot.send_message(
            message.chat.id,
            input_required_msg_text[user.language]
        )
        await bot.delete_message(
            chat_id=message.chat.id,
            message_id=message.message_id
        )
    else:
        if len(item_name) > 24:
            await bot.send_message(
                message.chat.id,
                item_name_len_error_text[user.language]
            )
        else: 
            state_ctx = FSMContext(dp.storage, user.telegram_id, dp.loop)
            current_state = await state_ctx.get_state()
            if current_state == "AddedItem:item_name":
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
            else:
                item_id = user_data.get('item_id')
                item = session.query(Item).get(item_id)
                item.name = item_name
                session.commit()
                await state.finish()
                await final_item_post(message, item_id, None)


#? --- Item Description --- ?#

async def input_item_description(message: types.Message, state:FSMContext):
    user = await get_verified_user(message.from_user.id)
    input_item_media_kb = build_input_item_media_keyboard(user.language)
    user_data = json.loads(user.data) if user.data else {}
    message_id = user_data.get('message_id')
    item_description = str(message.text)
    if should_ignore(item_description, user.language):
        await bot.send_message(
            message.chat.id,
            input_required_msg_text[user.language]
        )
        await bot.delete_message(
            chat_id=message.chat.id,
            message_id=message.message_id
        )
    else:
        if len(item_description) > 200:
            await bot.send_message(
                message.chat.id,
                item_description_len_error_text[user.language]
            )
        else:
            state_ctx = FSMContext(dp.storage, user.telegram_id, dp.loop)
            current_state = await state_ctx.get_state()
            if current_state == "AddedItem:item_description":
                user_data['item_description'] = item_description
                user.data = json.dumps(user_data)
                session.commit()
                await bot.send_message(
                    message.chat.id,
                    added_item_media_text[user.language],
                    reply_markup=input_item_media_kb
                )
                await  bot.edit_message_reply_markup(
                    message.chat.id,
                    message_id,
                    reply_markup=None
                )
                await AddedItem.item_media.set()
            else:
                item_id = user_data.get('item_id')
                item = session.query(Item).get(item_id)
                item.description = item_description
                session.commit()
                await state.finish()
                await final_item_post(message, item_id, None)


async def back_to_input_item_name(query: types.CallbackQuery):
    user = await get_verified_user(query.from_user.id)
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


async def skip_item_description(query: types.CallbackQuery):
    user = await get_verified_user(query.from_user.id)
    input_item_media_kb = build_input_item_media_keyboard(user.language)
    user_data = json.loads(user.data) if user.data else {}
    message_id = user_data.get('message_id')
    user_data['item_description'] = None
    user.data = json.dumps(user_data)
    session.commit()
    await bot.send_message(
        query.message.chat.id,
        added_item_media_text[user.language],
        reply_markup=input_item_media_kb
    )
    await  bot.edit_message_reply_markup(
        query.message.chat.id,
        message_id,
        reply_markup=None
    )
    await AddedItem.item_media.set()

#? --- Item Photo --- ?#

async def input_item_media(message: types.Message, state: FSMContext):
    user = await get_verified_user(message.from_user.id)
    state_ctx = FSMContext(dp.storage, user.telegram_id, dp.loop)
    current_state = await state_ctx.get_state()
    if current_state == "AddedItem:item_media":
        input_item_media_kb = build_input_item_media_keyboard(user.language)
    else:
        input_item_media_kb = build_change_item_media_keyboard(user.language)
    async with state.proxy() as data:
        if 'media' not in data:
            data['media'] = {"photos": [], "videos": []}
    
        total_media = len(data['media']['photos']) + len(data['media']['videos'])
        if total_media >= 3:
            await bot.send_message(
                message.chat.id,
                max_media_sent_text[user.language],
                reply_markup=input_item_media_kb
                )
            await bot.delete_message(
                chat_id=message.chat.id,
                message_id=message.message_id
            )
            return
        if message.photo:
            data['media']['photos'].append(message.photo[-1].file_id)
        elif message.video:
            video = message.video
            if video.duration > 15:
                await bot.send_message(
                    message.chat.id,
                    input_media_video_duration_error_text[user.language],
                    reply_markup=input_item_media_kb
                    )
                return
            else:
                data['media']['videos'].append(message.video.file_id)
        await state.update_data(data)
        total_media = len(data['media']['photos']) + len(data['media']['videos'])
        await bot.send_message(
            message.chat.id,
            media_count_msg_text[user.language].format(total_media),
            reply_markup=input_item_media_kb
            )


async def back_to_description(message: types.Message):
    user = await get_verified_user(message.from_user.id)
    user_data = json.loads(user.data) if user.data else {}
    back_to_input_item_name_kb = build_back_to_input_item_name_keyboard(user.language)
    send_message = await bot.send_message(
        message.chat.id,
        added_item_description_text[user.language],
        reply_markup=back_to_input_item_name_kb
    )
    user_data['message_id'] = send_message.message_id
    user.data = json.dumps(user_data)
    session.commit()
    await AddedItem.item_description.set()


async def clear_media(message: types.Message, state: FSMContext):
    user = await get_verified_user(message.from_user.id)
    state_ctx = FSMContext(dp.storage, user.telegram_id, dp.loop)
    current_state = await state_ctx.get_state()
    if current_state == "AddedItem:item_media":
        input_item_media_kb = build_input_item_media_keyboard(user.language)
    else:
        input_item_media_kb = build_change_item_media_keyboard(user.language)
    async with state.proxy() as data:
        data['media'] = {"photos": [], "videos": []}
    await bot.send_message(
        message.chat.id,
        clear_media_text[user.language],
        reply_markup=input_item_media_kb
    )


async def save_item_media(message: types.Message, state: FSMContext):
    user = await get_verified_user(message.from_user.id)
    general_menu_kb = build_general_menu_keyboard(user.language)
    user_data = json.loads(user.data) if user.data else {}
    async with state.proxy() as data:
        media = data.get('media', None)
        if media is not None:
            total_media = len(data['media']['photos']) + len(data['media']['videos'])
            if total_media < 1:
                await bot.send_message(
                message.from_user.id,
                media_is_not_loaded_text[user.language]
            )
            else:
                state_ctx = FSMContext(dp.storage, user.telegram_id, dp.loop)
                current_state = await state_ctx.get_state()
                if current_state == "AddedItem:item_media":
                    item_name = user_data.get('item_name')
                    item_description = user_data.get('item_description')
                    item = Item(
                        user=user.telegram_id,
                        name=item_name,
                        media=media,
                        description=item_description,
                        status='not_confirmed'
                    )
                    session.add(item)
                    session.commit()
                    await state.finish()
                    await bot.send_message(
                        message.from_user.id,
                        quantity_item_media_text[user.language].format(total_media),
                        reply_markup=general_menu_kb
                    )
                    await final_item_post(message, item.id, None) 
                else:
                    item_id = user_data.get('item_id')
                    item = session.query(Item).get(item_id)
                    item.media = media
                    session.commit()
                    await state.finish()
                    await bot.send_message(
                        message.from_user.id,
                        quantity_item_media_text[user.language].format(total_media),
                        reply_markup=general_menu_kb
                    )
                    await final_item_post(message, item.id, None)
        else:
            await bot.send_message(
                message.from_user.id,
                media_is_not_loaded_text[user.language]
            )


async def text_validation_when_entering_media(message:types.Message, state: FSMContext):
    user = await get_verified_user(message.from_user.id)
    state_ctx = FSMContext(dp.storage, user.telegram_id, dp.loop)
    current_state = await state_ctx.get_state()
    if current_state == "AddedItem:item_media":
        input_item_media_kb = build_input_item_media_keyboard(user.language)
    else:
        input_item_media_kb = build_change_item_media_keyboard(user.language)
    if should_ignore(message.text, user.language):
        await bot.send_message(
            message.chat.id,
            input_required_msg_text[user.language]
        )
        await bot.delete_message(
            chat_id=message.chat.id,
            message_id=message.message_id
        )
    else:
        await bot.send_message(
            message.chat.id,
            invalid_media_type_text[user.language],
            reply_markup=input_item_media_kb
        )
        await bot.delete_message(
            chat_id=message.chat.id,
            message_id=message.message_id
        )


#! --- Item Post Confirmation --- !#

async def final_item_post(message: types.Message, item_id, query:types.CallbackQuery):
    if message == None:
        message = query.message 
        user = await get_verified_user(query.from_user.id)
    else:
        user = await get_verified_user(message.from_user.id)
    item = session.query(Item).get(item_id)
    item_name = item.name
    column_name = get_column_by_language(user.language)
    final_item_post_kb = build_final_item_post_keyboard(user.language, item_id)
    item_description = item.description
    media = item.media
    media_list = []
    all_media = media["photos"] + media["videos"]
    default_tag_obj = session.query(Tag).filter(Tag.status == 'default').first()
    default_tag = getattr(default_tag_obj, column_name, None)
    for i, media_id in enumerate(all_media):
        if i == len(all_media) - 1:
            if item_description is not None:
                caption_text = item_form_post_with_description[user.language].format(
                    item_name, item_description, default_tag
                    )
            else:
                caption_text = item_form_post_no_description[user.language].format(item_name, default_tag)
        else:
            caption_text = None

        if media_id in media["photos"]:
            media_list.append(InputMediaPhoto(media=media_id, caption=caption_text))
        else:
            media_list.append(InputMediaVideo(media=media_id, caption=caption_text))
        
    await bot.send_media_group(chat_id=message.chat.id, media=media_list)
    await bot.send_message(
        chat_id=message.chat.id,
        text=standart_decorational_line_text,
        reply_markup=final_item_post_kb
    )

#? --- Change Item Post --- ?#

async def change_item_post_menu(query:types.CallbackQuery):
    user = await get_verified_user(query.from_user.id)
    item_id = query.data.split('#')[1]
    change_item_post_menu_kb = build_change_item_post_menu_kayboard(user.language, item_id)
    await bot.edit_message_reply_markup(
        query.message.chat.id,
        query.message.message_id,
        reply_markup=change_item_post_menu_kb
    )


async def change_item_name(query: types.CallbackQuery):
    user = await get_verified_user(query.from_user.id)
    item_id = query.data.split('#')[1]
    user_data = json.loads(user.data) if user.data else {}
    await bot.send_message(
        query.message.chat.id,
        change_item_name_text[user.language]
    )
    await bot.edit_message_reply_markup(
        query.message.chat.id,
        query.message.message_id,
        reply_markup=None
    )
    user_data['item_id'] = item_id
    user.data = json.dumps(user_data)
    session.commit()
    await AddedItem.change_item_name.set()


async def change_item_description(query: types.CallbackQuery):
    user = await get_verified_user(query.from_user.id)
    item_id = query.data.split('#')[1]
    user_data = json.loads(user.data) if user.data else {}
    delete_item_description_kb = build_delete_item_description_keyboard(user.language, item_id)
    item = session.query(Item).get(item_id)
    if item.description == None:
        delete_item_description_kb = None
    await bot.send_message(
        query.message.chat.id,
        change_item_description_text[user.language],
        reply_markup=delete_item_description_kb
    )
    await bot.edit_message_reply_markup(
        query.message.chat.id,
        query.message.message_id,
        reply_markup=None
    )
    user_data['item_id'] = item_id
    user.data = json.dumps(user_data)
    session.commit()
    await AddedItem.change_item_description.set()


async def change_item_delete_description(query: types.CallbackQuery, state: FSMContext):
    item_id = query.data.split('#')[1]
    item = session.query(Item).get(item_id)
    item.description = None
    session.commit()
    await state.finish()
    await final_item_post(None, item_id, query)


async def change_item_media(query: types.CallbackQuery):
    user = await get_verified_user(query.from_user.id)
    item_id = query.data.split('#')[1]
    change_item_media_kb = build_change_item_media_keyboard(user.language)
    user_data = json.loads(user.data) if user.data else {}
    await bot.send_message(
        query.message.chat.id,
        added_new_item_media_text[user.language],
        reply_markup=change_item_media_kb
    )
    await  bot.edit_message_reply_markup(
        query.message.chat.id,
        query.message.message_id,
        reply_markup=None
    )
    user_data['item_id'] = item_id
    user.data = json.dumps(user_data)
    session.commit()
    await AddedItem.change_item_media.set()


async def back_to_confirmation_menu(query:types.CallbackQuery):
    user = await get_verified_user(query.from_user.id)
    item_id = query.data.split('#')[1]
    final_item_post_kb = build_final_item_post_keyboard(user.language, item_id)
    await bot.edit_message_reply_markup(
        query.message.chat.id,
        query.message.message_id,
        reply_markup=final_item_post_kb
    )


#? --- Item Tags --- ?#


#? --- FINISH --- ?#

async def confirmation_create_item_post(query: types.CallbackQuery):
    user = await get_verified_user(query.from_user.id)
    item_id = query.data.split('#')[1]
    item = session.query(Item).get(item_id)
    item.status = 'active'
    session.commit()
    general_menu_kb = build_general_menu_keyboard(user.language)
    await bot.edit_message_reply_markup(
        query.message.chat.id,
        query.message.message_id,
        reply_markup=None
    )
    await bot.send_message(
        query.message.chat.id,
        confirmation_create_item_post_text[user.language],
        reply_markup=general_menu_kb
    )



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
        state=[
            AddedItem.item_name,
            AddedItem.item_description
            ]
    )
    dp.register_message_handler(
        input_item_name,
        state=[
            AddedItem.item_name,
            AddedItem.change_item_name]
    )
    #* --- Item Description --- *#
    dp.register_message_handler(
        input_item_description,
        state=[
            AddedItem.item_description,
            AddedItem.change_item_description]
    )
    dp.register_callback_query_handler(
        back_to_input_item_name,
        Text(startswith='back_to_input_item_name'),
        state=AddedItem.item_description
    )
    dp.register_callback_query_handler(
        skip_item_description,
        Text(startswith='skip_item_description'),
        state=AddedItem.item_description
    )
    #* --- Item Photo --- *#
    dp.register_message_handler(
        input_item_media,
        state=[
            AddedItem.item_media,
            AddedItem.change_item_media],
        content_types=[ContentType.PHOTO, ContentType.VIDEO]
    )
    dp.register_message_handler(
        back_to_description,
        Text(equals=[
            '⬅️ Назад до опису',
            '⬅️ Back to description',
            '⬅️ Wróć do opisu',
            '⬅️ Назад к описанию'
            ]),
        state=AddedItem.item_media,
    )
    dp.register_message_handler(
        clear_media,
        Text(equals=[
            '🔄 Ввести медіа знову',
            '🔄 Enter media again',
            '🔄 Wprowadź media ponownie',
            '🔄 Ввести медиа заново'
            ]),
        state=[
            AddedItem.item_media,
            AddedItem.change_item_media]
    )
    dp.register_message_handler(
        save_item_media,
        Text(equals=[
            '💾 Зберегти медіа',
            '💾 Save media',
            '💾 Zapisz media',
            '💾 Сохранить медиа'
            ]),
        state=[
            AddedItem.item_media,
            AddedItem.change_item_media],
    )
    dp.register_message_handler(
        text_validation_when_entering_media,
        lambda message: message.content_type not in ['photo', 'video'], 
        state=[
            AddedItem.item_media,
            AddedItem.change_item_media],
    )
    #* --- Change Item Post --- *#
    dp.register_callback_query_handler(
        change_item_post_menu,
        Text(startswith='edit_created_item_post#'),
    )
    dp.register_callback_query_handler(
        change_item_name,
        Text(startswith='edit_item_name#'),
    )
    dp.register_callback_query_handler(
        change_item_description,
        Text(startswith='edit_item_description#'),
    )
    dp.register_callback_query_handler(
        back_to_confirmation_menu,
        Text(startswith='back_to_confirmation_menu#'),
    )
    dp.register_callback_query_handler(
        change_item_delete_description,
        Text(startswith='delete_description#'),
        state=AddedItem.change_item_description
    )
    dp.register_callback_query_handler(
        change_item_media,
        Text(startswith='edit_item_media#'),
    )
    
    #* --- Item Tags --- *#
    
    #* --- FINISH --- *#
    dp.register_callback_query_handler(
        confirmation_create_item_post,
        Text(startswith='confirme_item_post#'),
    )