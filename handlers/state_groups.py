from aiogram.dispatcher.filters.state import State, StatesGroup


class RegistrationState(StatesGroup):
    get_location = State()