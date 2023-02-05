from aiogram.dispatcher.filters.state import State, StatesGroup

class AddAccountState(StatesGroup):
    GET_NAME_ACCOUNT = State()
    GET_API_ID_ACCOUNT = State()
    GET_PHONE_ACCOUNT = State()
    GET_CODE_ACCOUNT = State()
    GET_2FA_ACCOUNT = State()