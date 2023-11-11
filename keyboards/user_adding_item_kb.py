from aiogram.types import (
    KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
)
from text import(
    cancel_addition_btn_text, back_to_input_item_name_btn_text, skip_item_description_btn_text,
    save_media_btn_text, back_to_description_btn_text, reset_media_btn_text, add_tag_btn_text,
    confirme_btn_text, change_btn_text, back_btn_text, change_item_name_btn_text,
    change_item_description_btn_text, change_item_media_btn_text, delete_description_btn_text,
    delete_btn_text
)




def build_cancel_added_item_keyboard(language):
    cancel_btn = InlineKeyboardButton(
        text=cancel_addition_btn_text[language],
        callback_data='cancel_added_item'
    )
    kb_cancel_added_item = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
    kb_cancel_added_item.add(
        cancel_btn
        )
    return kb_cancel_added_item


def build_back_to_input_item_name_keyboard(language):
    back_btn = InlineKeyboardButton(
        text=back_to_input_item_name_btn_text[language],
        callback_data='back_to_input_item_name'
    )
    skip_btn = InlineKeyboardButton(
        text=skip_item_description_btn_text[language],
        callback_data='skip_item_description'
    )
    cancel_btn = InlineKeyboardButton(
        text=cancel_addition_btn_text[language],
        callback_data='cancel_added_item'
    )
    kb_back_to_input_item_name = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb_back_to_input_item_name.add(back_btn, skip_btn).add(cancel_btn)
    return kb_back_to_input_item_name


def build_input_item_media_keyboard(language):
    save_btn = KeyboardButton(save_media_btn_text[language])
    back_btn = KeyboardButton(back_to_description_btn_text[language])
    clear_btn = KeyboardButton(reset_media_btn_text[language])
    input_item_media_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    input_item_media_kb.add(save_btn).add(back_btn, clear_btn)
    return input_item_media_kb

def build_change_item_media_keyboard(language):
    save_btn = KeyboardButton(save_media_btn_text[language])
    clear_btn = KeyboardButton(reset_media_btn_text[language])
    input_item_media_kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    input_item_media_kb.add(save_btn, clear_btn)
    return input_item_media_kb


def build_final_item_post_keyboard(language, item_id):
    confirme_btn = InlineKeyboardButton(
        text=confirme_btn_text[language],
        callback_data=f'confirme_item_post#{item_id}'
    )
    edit_btn = InlineKeyboardButton(
        text=change_btn_text[language],
        callback_data=f'edit_created_item_post#{item_id}'
    )
    tag_btn = InlineKeyboardButton(
        text=delete_btn_text[language],
        callback_data=f'delete_item_post#{item_id}'
    )
    kb_final_item_post = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb_final_item_post.add(confirme_btn).add(edit_btn, tag_btn)
    return kb_final_item_post


def build_change_item_post_menu_kayboard(language, item_id):
    edit_item_name_btn = InlineKeyboardButton(
        text=change_item_name_btn_text[language],
        callback_data=f'edit_item_name#{item_id}'
    )
    edit_item_description_btn = InlineKeyboardButton(
        text=change_item_description_btn_text[language],
        callback_data=f'edit_item_description#{item_id}'
    )
    edit_item_media_btn = InlineKeyboardButton(
        text=change_item_media_btn_text[language],
        callback_data=f'edit_item_media#{item_id}'
    )
    back_btn = InlineKeyboardButton(
        text=back_btn_text[language],
        callback_data=f'back_to_confirmation_menu#{item_id}'
    )
    kb_change_item_post_menu = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb_change_item_post_menu.add(
        edit_item_name_btn, edit_item_description_btn).add(edit_item_media_btn).add(back_btn)
    return kb_change_item_post_menu


def build_delete_item_description_keyboard(language, item_id):
    delete_description_btn = InlineKeyboardButton(
        text=delete_description_btn_text[language],
        callback_data=f'delete_description#{item_id}'
    )
    kb_delete_item_description = InlineKeyboardMarkup(resize_keyboard=True)
    kb_delete_item_description.add(delete_description_btn)
    return kb_delete_item_description