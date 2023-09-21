from aiogram.dispatcher.filters.state import State, StatesGroup


class MainState(StatesGroup):
    get_location = State()