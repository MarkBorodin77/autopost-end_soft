from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.inline import menu_keyboard
from loader import dp


@dp.message_handler(CommandStart(), state="*")
async def bot_start(msg: types.Message, state: FSMContext):
    await state.reset_state(with_data=False)

    state_data = await state.get_data()

    if "account_name" in state_data:
        account_name = state_data["account_name"]
        await msg.answer(
            f"🤟 Привет, <b>{msg.from_user.full_name}</b>! Жмакай на кнопки чтобы настроить функционал.\n\n<b>Выбранный аккаунт:</b> {account_name}",
            reply_markup=menu_keyboard)

    else:
        await msg.answer(
            f"🤟 Привет, <b>{msg.from_user.full_name}</b>! Жмакай на кнопки чтобы настроить функционал. На данный момент у тебя не выбран никакой аккаунт.",
            reply_markup=menu_keyboard)