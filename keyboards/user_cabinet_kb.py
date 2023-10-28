from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton
)
from text import(
    user_favorites_btn_text, my_items_btn_text, incoming_applications_btn_text,
    my_exchanges_btn_text, change_language_btn_text, change_city_btn_text,
    help_btn_text
)


def build_user_cabinet_menu_keyboard(language):
    favorites_btn = InlineKeyboardButton(
        text=user_favorites_btn_text[language],
        callback_data='my_favorites_user_cabinet'
        )
    items_btn = InlineKeyboardButton(
        text=my_items_btn_text[language],
        callback_data='my_items_user_cabinet'
        )
    incoming_applications_btn = InlineKeyboardButton(
        text=incoming_applications_btn_text[language],
        callback_data='incoming_applications_user_cabinet'
        )
    exchangess_btn = InlineKeyboardButton(
        text=my_exchanges_btn_text[language],
        callback_data='my_exchanges_user_cabinet'
        )
    change_language_btn = InlineKeyboardButton(
        text=change_language_btn_text[language],
        callback_data='change_language_user_cabinet'
        )
    change_city_btn = InlineKeyboardButton(
        text=change_city_btn_text[language],
        callback_data='change_city_user_cabinet'
        )
    help_btn = InlineKeyboardButton(
        text=help_btn_text[language],
        callback_data='help_user_cabinet'
        )
    kb_choose_a_language = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb_choose_a_language.add(
        favorites_btn
            ).add(items_btn
                ).add(incoming_applications_btn
                    ).add(exchangess_btn
                        ).add(change_language_btn, change_city_btn
                            ).add(help_btn)

    return kb_choose_a_language