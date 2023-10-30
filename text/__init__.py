#=== UNIVERSAL ===#
from .user_universal_text import (
    input_required_msg_text, input_required_media_text, standart_decorational_line_text
)

#=== REGISTRATION ===#
from .user_registration_text import (
    choose_a_language_text, input_location_text, input_user_city_name_error_text,
    input_user_city_type_error_text, main_description_text
    )

from .user_registration_btn_text import (
    language_selection_btn_text, get_geo_btn_text, item_search_btn_text,
    user_profile_btn_text, add_item_btn_text
)

#=== CABINET ===#
from .user_cabinet_text import (
    user_cabinet_menu_text, user_language_text, successful_language_change_text,
    successful_city_change_text, change_city_user_cabinet_text, help_user_cabinet_text,
    cancel_change_city_text
)

from .user_cabinet_btn_text import (
    user_favorites_btn_text, my_items_btn_text, incoming_applications_btn_text,
    my_exchanges_btn_text, change_language_btn_text, change_city_btn_text,
    help_btn_text
)

#=== ADDING ITEM ===#
from .user_adding_item_text import (
    added_item_name_text, cancel_added_item_text, item_name_len_error_text,
    added_item_media_text, added_item_description_text, item_description_len_error_text,
    max_media_sent_text, invalid_media_type_text, media_count_msg_text,
    input_media_video_duration_error_text, quantity_item_media_text, media_is_not_loaded_text,
    clear_media_text, item_form_post_with_description, item_form_post_no_description,
    confirmation_create_item_post_text
)

from .user_adding_item_btn_text import (
    cancel_addition_btn_text, back_to_input_item_name_btn_text, skip_item_description_btn_text,
    save_media_btn_text, back_to_description_btn_text, reset_media_btn_text, add_tag_btn_text,
    confirme_btn_text, change_btn_text, 
)