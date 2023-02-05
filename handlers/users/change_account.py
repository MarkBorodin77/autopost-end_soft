from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline import change_account_menu_keyboard, menu_keyboard
from loader import dp


@dp.callback_query_handler(lambda c: c.data == "change_account_menu")
async def _(query: types.CallbackQuery):
    await query.message.edit_text("<b>🎩 Меню аккаунтов</b>\n\nТы зашел в меню аккаунтов. Здесь ты можешь выбрать аккаунт или добавить новый.", reply_markup=change_account_menu_keyboard)


@dp.callback_query_handler(lambda c: c.data == "cancel_action", state="*")
async def _(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_text("Действие успешно <b>отменено</b>.", reply_markup='')
    await state.reset_state(with_data=False)


@dp.callback_query_handler(lambda c: c.data == "return_menu", state="*")
async def _(query: types.CallbackQuery, state: FSMContext):
    await state.reset_state(with_data=False)

    state_data = await state.get_data()

    if "account_name" in state_data:
        account_name = state_data["account_name"]
        await query.message.edit_text(
            f"🤟 Привет, <b>{query.from_user.full_name}</b>! Жмакай на кнопки чтобы настроить функционал.\n\n<b>Выбранный аккаунт:</b> {account_name}",
            reply_markup=menu_keyboard)

    else:
        await query.message.edit_text(
            f"🤟 Привет, <b>{query.from_user.full_name}</b>! Жмакай на кнопки чтобы настроить функционал. На данный момент у тебя не выбран никакой аккаунт.",
            reply_markup=menu_keyboard)
