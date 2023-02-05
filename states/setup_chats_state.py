from aiogram.dispatcher.filters.state import State, StatesGroup

class SetupChatsState(StatesGroup):
    EDIT_TEXT = State()
    EDIT_TIME = State()
    ADD_PHOTO = State()
    DELETE_PHOTO = State()