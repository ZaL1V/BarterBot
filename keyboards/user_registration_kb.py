from aiogram.types import (
    KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
)
from text import (
    language_selection_btn_text, get_geo_btn_text, item_search_btn_text,
    user_profile_btn_text, add_item_btn_text
)


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


def build_get_location_keyboard(language):
    geo_button = KeyboardButton(get_geo_btn_text[language], request_location=True)
    geo_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    geo_kb.add(geo_button)
    return geo_kb


def build_general_menu_keyboard(language):
    search_btn = KeyboardButton(item_search_btn_text[language])
    add_item_btn = KeyboardButton(add_item_btn_text[language])
    user_profile_btn = KeyboardButton(user_profile_btn_text[language])
    general_menu_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    general_menu_kb.add(search_btn).add(user_profile_btn, add_item_btn)
    return general_menu_kb