from aiogram.types import (
    KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
)
from text import(
    cancel_btn_text
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