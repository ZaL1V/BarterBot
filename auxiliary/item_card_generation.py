from aiogram.types import InputMediaPhoto, InputMediaVideo
from database import session, Item
from text import item_form_post_with_description, item_form_post_no_description



def get_media_list(language, item_id):
    item = session.query(Item).get(item_id)
    item_name = item.name
    item_description = item.description
    media = item.media
    media_list = []
    all_media = media["photos"] + media["videos"]
    for i, media_id in enumerate(all_media):
        if i == len(all_media) - 1:
            if item_description is not None:
                caption_text = item_form_post_with_description[language].format(
                    item_name, item_description
                    )
            else:
                caption_text = item_form_post_no_description[language].format(item_name)
        else:
            caption_text = None

        if media_id in media["photos"]:
            media_list.append(InputMediaPhoto(media=media_id, caption=caption_text))
        else:
            media_list.append(InputMediaVideo(media=media_id, caption=caption_text))
    return media_list