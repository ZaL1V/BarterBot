from aiogram.types import (
    KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
)
from text import(
    cancel_btn_text, back_btn_text
)




def build_cancel_added_item_keyboard(language):
    cancel_btn = InlineKeyboardButton(
        text=cancel_btn_text[language],
        callback_data='cancel_added_item'
    )
    kb_cancel_added_item = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
    kb_cancel_added_item.add(
        cancel_btn
        )
    return kb_cancel_added_item


def build_back_to_input_item_name_keyboard(language):
    back_btn = InlineKeyboardButton(
        text=back_btn_text[language],
        callback_data='back_to_input_item_name'
    )
    kb_back_to_input_item_name = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
    kb_back_to_input_item_name.add(
        back_btn
        )
    return kb_back_to_input_item_name