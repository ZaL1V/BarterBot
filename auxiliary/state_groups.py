from aiogram.dispatcher.filters.state import State, StatesGroup


class RegistrationState(StatesGroup):
    get_location = State()


class AddedItem(StatesGroup):
    item_name = State()
    change_item_name= State()
    item_description = State()
    change_item_description = State()
    item_media = State()
    change_item_media = State()