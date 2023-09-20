from aiogram.types import (
    KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, WebAppData
)
from .user_registration_btn_text import language_selection_btn_text


def build_choose_a_language_keyboard():
    uk_btn = InlineKeyboardButton(
        text=language_selection_btn_text['uk'],
        callback_data='choose_language#uk'
        )
    en_btn = InlineKeyboardButton(
        text=language_selection_btn_text['en'],
        callback_data='choose_language#en'
        )
    pl_btn = InlineKeyboardButton(
        text=language_selection_btn_text['pl'],
        callback_data='choose_language#pl'
        )
    ru_btn = InlineKeyboardButton(
        text=language_selection_btn_text['ru'],
        callback_data='choose_language#ru'
        )
    kb_choose_a_language = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
    kb_choose_a_language.add(
        uk_btn, en_btn, pl_btn, ru_btn
        )
    return kb_choose_a_language