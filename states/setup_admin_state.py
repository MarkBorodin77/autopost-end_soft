from aiogram.dispatcher.filters.state import State, StatesGroup

class AdminSetupState(StatesGroup):
    DELETE_ADMIN = State()
    ADD_ADMIN = State()