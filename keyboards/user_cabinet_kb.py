from math import ceil
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton
)
from text import(
    user_favorites_btn_text, my_items_btn_text, incoming_applications_btn_text,
    my_exchanges_btn_text, change_language_btn_text, change_city_btn_text,
    help_btn_text, back_btn_text, next_btn_text, page_btn_text, delete_btn_text,
    disable_item_post_btn_text, enable_item_post_btn_text, confirme_btn_text
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


def build_menu_selection_my_item_posts_keyboard(language, items, current_page=1, items_per_page=6):
    kb_menu_selection_my_item_posts = InlineKeyboardMarkup(resize_keyboard=True)
    
    start_index = (current_page - 1) * items_per_page
    end_index = start_index + items_per_page
    current_items = items[start_index:end_index]

    for item in current_items:
        item_name_btn = InlineKeyboardButton(
            text=item.name,
            callback_data=f'manage_my_item_post#{item.id}'
        )
        kb_menu_selection_my_item_posts.add(item_name_btn)

    total_pages = ceil(len(items) / items_per_page)
    pagination_buttons = build_pagination_buttons(language, current_page, total_pages)
    kb_menu_selection_my_item_posts.add(*pagination_buttons)

    return kb_menu_selection_my_item_posts

def build_pagination_buttons(language, current_page, total_pages):
    pagination_buttons = []

    if current_page > 1:
        prev_button = InlineKeyboardButton(
            text=back_btn_text[language],
            callback_data=f'change_my_item_posts_menu_page#{current_page - 1}'
        )
        pagination_buttons.append(prev_button)

    page_button = InlineKeyboardButton(
        text=page_btn_text[language].format(current_page, total_pages),
        callback_data='do_nothing'
    )
    pagination_buttons.append(page_button)

    if current_page < total_pages:
        next_button = InlineKeyboardButton(
            text=next_btn_text[language],
            callback_data=f'change_my_item_posts_menu_page#{current_page + 1}'
        )
        pagination_buttons.append(next_button)

    return pagination_buttons


def build_output_selected_post_keyboard(language, item_id, status):
    if status == 'active':
        item_status = disable_item_post_btn_text[language]
    else:
        item_status = enable_item_post_btn_text[language]
    delete_btn = InlineKeyboardButton(
        text=delete_btn_text[language],
        callback_data=f'my_item_post_delete_menu#{item_id}'
        )
    change_status_btn = InlineKeyboardButton(
        text=item_status,
        callback_data=f'change_my_item_post_status#{item_id}'
        )
    kb_output_selected_post = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
    kb_output_selected_post.add(delete_btn, change_status_btn)
    return kb_output_selected_post


def build_my_item_post_delete_menu_keyboard(language, item_id):
    back_btn = InlineKeyboardButton(
        text=back_btn_text[language],
        callback_data=f'back_to_my_item_post_menu#{item_id}'
        )
    delete_item_post_btn = InlineKeyboardButton(
        text=confirme_btn_text[language],
        callback_data=f'delete_my_item_post#{item_id}'
        )
    kb_output_selected_post = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
    kb_output_selected_post.add(delete_item_post_btn, back_btn)
    return kb_output_selected_post