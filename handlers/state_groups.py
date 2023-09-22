from aiogram.dispatcher.filters.state import State, StatesGroup


class RegistrationState(StatesGroup):
    get_location = State()


class AddedItem(StatesGroup):
    item_name = State()
    item_description = State()
    item_media = State()